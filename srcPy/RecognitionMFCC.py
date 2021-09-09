import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy.io import wavfile as wf
from Plot import plot_confusion_matrix 
from MPEG7Features import mfcc_and_deltas 
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import recall_score, precision_score, accuracy_score

class Constants:
    m_delta = 0.0000000001   
    m_testSize = 0.25
    m_neighbors = 1
    m_mels = 128
    m_mfcc = 13
    m_width = 7

path_to_dataset = '../dataset/'
dataset_fname = 'dataset.csv'

df = pd.read_csv(path_to_dataset + dataset_fname)

classes = list(np.unique(df.label))
labels = list(df.label)
        
labelencoder = LabelEncoder()
labelencoder.fit(labels)
classes_num = labelencoder.transform(labels)

mfcc_vectors = np.array([])
mfcc_vectors = np.hstack((mfcc_vectors, np.arange(Constants.m_mfcc)))
mfcc_delta_vectors = np.array([])
mfcc_delta_vectors = np.hstack((mfcc_delta_vectors, np.arange(Constants.m_mfcc)))
mfcc_delta2_vectors = np.array([])
mfcc_delta2_vectors = np.hstack((mfcc_delta2_vectors, np.arange(Constants.m_mfcc)))

for cl in classes:            
    for root, dirnames, filenames in os.walk(path_to_dataset + cl):
            for dirname in dirnames:
                for root_mi, dirnames_mi, filenames_mi in os.walk(root + '/' + dirname + '/'):
                    for file in tqdm(filenames_mi):
                        sr, signal = wf.read(root_mi + file)
                        signal_mean = signal.mean()
                        signal_max = (np.abs(signal)).max()
                        signal = (signal - signal_mean) / (signal_max + Constants.m_delta)
                        mfcc, mfcc_delta, mfcc_delta2 = mfcc_and_deltas(signal=signal, sr=sr, n_mels=Constants.m_mels, n_mfcc=Constants.m_mfcc, width=Constants.m_width)
                        mfcc_vectors = np.vstack((mfcc_vectors, mfcc))
                        mfcc_delta_vectors = np.vstack((mfcc_delta_vectors, mfcc_delta))
                        mfcc_delta2_vectors = np.vstack((mfcc_delta2_vectors, mfcc_delta2))
    
scaler = StandardScaler()
scaled_mfcc_vectors = scaler.fit_transform(mfcc_vectors[1:])
scaled_mfcc_delta_vectors = scaler.fit_transform(mfcc_delta_vectors[1:])
scaled_mfcc_delta2_vectors = scaler.fit_transform(mfcc_delta2_vectors[1:])
scaled_feature_vectors = scaled_mfcc_vectors
scaled_feature_vectors = np.append(scaled_feature_vectors, scaled_mfcc_delta_vectors, 1)
scaled_feature_vectors = np.append(scaled_feature_vectors, scaled_mfcc_delta2_vectors, 1)

splitter = StratifiedShuffleSplit(n_splits=1, test_size=Constants.m_testSize, random_state=0)
splits = splitter.split(scaled_feature_vectors, classes_num)
for train_index, test_index in splits:
    train_set = scaled_feature_vectors[train_index]
    test_set = scaled_feature_vectors[test_index]
    train_classes = classes_num[train_index]
    test_classes = classes_num[test_index]

model_knn = KNeighborsClassifier(n_neighbors=Constants.m_neighbors)
model_knn.fit(train_set, train_classes)
predicted_labels = model_knn.predict(test_set)

print("Recall: ", recall_score(test_classes, predicted_labels,average=None))
print("Precision: ", precision_score(test_classes, predicted_labels,average=None))
print("F1-Score: ", f1_score(test_classes, predicted_labels, average=None))
print("Accuracy: %.2f," % accuracy_score(test_classes, predicted_labels,normalize=True), 
                          accuracy_score(test_classes, predicted_labels,normalize=False))
print("Number of samples:", test_classes.shape[0])

cnf_matrix = confusion_matrix(test_classes, predicted_labels)
np.set_printoptions(precision=2)

plt.close('all')    
plt.figure(figsize=(5,5))
plot_confusion_matrix(cnf_matrix, classes=labelencoder.classes_, title='Confusion matrix, without normalization')
