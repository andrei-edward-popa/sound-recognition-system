import threading
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedShuffleSplit
import os

os.chdir('/home/apopa/Facultate/Licenta/srcPy')

class Constants:
    m_testSize = 0.15
    m_neighbors = 5
    m_neighbors_mi = 3
    m_neighbors_sp = 5
    m_estimators = 5
    m_estimators_mi = 25
    m_estimators_sp = 3
    
def music(x):
    if x <= 4:
        return 0
    return 1

path_to_dataset = '../dataset/'
dataset_fname = 'dataset.csv'

df = pd.read_csv(path_to_dataset + dataset_fname)

all_labels = np.array(list(df.label_1st))
mi_labels = np.array(list(df.loc[df['label_1st'] == 'musical_instruments', 'label_2rd']))
sp_labels = np.array(list(df.loc[df['label_1st'] == 'speech', 'label_2rd']))

all_classes = np.unique(all_labels)
mi_classes = np.unique(mi_labels)
sp_classes = np.unique(sp_labels) 
        
all_labelencoder = LabelEncoder()
all_labelencoder.fit(all_labels)
all_classes_num = all_labelencoder.transform(all_labels)
mi_labelencoder = LabelEncoder()
mi_labelencoder.fit(mi_labels)
mi_classes_num = mi_labelencoder.transform(mi_labels)
sp_labelencoder = LabelEncoder()
sp_labelencoder.fit(sp_labels)
sp_classes_num = sp_labelencoder.transform(sp_labels)

feature_vectors = np.array([])
feature_vectors = np.hstack((feature_vectors, np.arange(len(df.index))))
for feature in df.columns[3:10]: 
    feature_vectors = np.column_stack((feature_vectors, df[feature].to_numpy()))
feature_vectors = np.delete(feature_vectors, 0, 1)

mi_mfcc_vectors = np.array([])
mi_mfcc_vectors = np.hstack((mi_mfcc_vectors, np.arange(len(mi_labels))))
sp_mfcc_vectors = np.array([])
sp_mfcc_vectors = np.hstack((sp_mfcc_vectors, np.arange(len(sp_labels))))
for feature in df.columns[11:19]:
    mfcc = df[feature].to_numpy()
    mi_mfcc_vectors = np.column_stack((mi_mfcc_vectors, mfcc[:len(mi_labels)]))
for feature in df.columns[9:17]:
    mfcc = df[feature].to_numpy()
    sp_mfcc_vectors = np.column_stack((sp_mfcc_vectors, mfcc[len(mi_labels):]))
mi_mfcc_vectors = np.delete(mi_mfcc_vectors, 0, 1)
sp_mfcc_vectors = np.delete(sp_mfcc_vectors, 0, 1)


splitter = StratifiedShuffleSplit(n_splits=5, test_size=Constants.m_testSize, random_state=1)
splits = splitter.split(feature_vectors, all_classes_num)
for train_index, test_index in splits:
    train_set = feature_vectors[train_index]
    test_set = feature_vectors[test_index]
    train_classes = all_classes_num[train_index]
    test_classes = all_classes_num[test_index]

model_knn = KNeighborsClassifier(n_neighbors=Constants.m_neighbors)
model_knn.fit(train_set, train_classes)

model_rf = RandomForestRegressor(n_estimators=Constants.m_estimators)
model_rf.fit(train_set, train_classes)

splitter = StratifiedShuffleSplit(n_splits=5, test_size=Constants.m_testSize, random_state=1)
splits = splitter.split(mi_mfcc_vectors, mi_classes_num)
for train_index, test_index in splits:
    train_set_mi = mi_mfcc_vectors[train_index]
    test_set_mi = mi_mfcc_vectors[test_index]
    train_classes_mi = mi_classes_num[train_index]
    test_classes_mi = mi_classes_num[test_index]

model_knn_mi = KNeighborsClassifier(n_neighbors=Constants.m_neighbors_mi)
model_knn_mi.fit(train_set_mi, train_classes_mi)

model_rf_mi = RandomForestRegressor(n_estimators=Constants.m_estimators_mi)
model_rf_mi.fit(train_set_mi, train_classes_mi)


splitter = StratifiedShuffleSplit(n_splits=5, test_size=Constants.m_testSize, random_state=1)
splits = splitter.split(sp_mfcc_vectors, sp_classes_num)
for train_index, test_index in splits:
    train_set_sp = sp_mfcc_vectors[train_index]
    test_set_sp = sp_mfcc_vectors[test_index]
    train_classes_sp = sp_classes_num[train_index]
    test_classes_sp = sp_classes_num[test_index]

model_knn_sp = KNeighborsClassifier(n_neighbors=Constants.m_neighbors_sp)
model_knn_sp.fit(train_set_sp, train_classes_sp)

model_rf_sp = RandomForestRegressor(n_estimators=Constants.m_estimators_sp)
model_rf_sp.fit(train_set_sp, train_classes_sp)
    
thr = None
result = "Wait for start recognition"
m_MAD = []
m_SAD = []
m_EE = []
m_F0 = []

def getData(classifier='kNN'):
    if classifier == 'kNN':
        global model_knn
        global model_knn_mi
        global model_knn_sp
    elif classifier == 'RF':
        global model_rf
        global model_rf_mi
        global model_rf_sp
    global thr
    global result
    arr = np.array([])
    thr = threading.Timer(0.48, getData, [classifier])
    thr.start()
    f = open('/home/apopa/Desktop/test', 'r+')
#    try:
    for line in f:
        line = line[:-1]
        if len(line) != 0:
            a = np.array(line.split(' '), dtype='float')
            arr = np.append(arr, a)
    arr = np.array([arr])
    m_MAD.append(arr[0][-2])
    m_SAD.append(arr[0][-1])
    m_EE.append(arr[0][6])
    m_F0.append(arr[0][7])
    if len(arr[0]) == 23:
        if classifier == 'kNN':
            prediction = model_knn.predict([arr[0][0:7]])[0]
        elif classifier == 'RF':
            prediction = int(round(model_rf.predict([arr[0][0:7]])[0]))
        SCR = arr[0][-1]
        MCR = arr[0][-2]
        if SCR == 0:
            result = 'silence'
        elif music(MCR) + prediction == 0:
            if classifier == 'kNN':
                pred = model_knn_mi.predict([arr[0][8:16]])[0]
            elif classifier == 'RF':
                pred = int(round(model_rf_mi.predict([arr[0][8:16]])[0]))
            result = 'musical_instruments' + ' ' + mi_classes[pred]
        elif music(MCR) + prediction == 2:
            if classifier == 'kNN':
                pred = model_knn_sp.predict([arr[0][6:14]])[0]
            elif classifier == 'RF':
                pred = int(round(model_rf_sp.predict([arr[0][6:14]])[0]))
            result = 'speech' + ' ' + sp_classes[pred]
        elif music(MCR) + prediction == 1:
            result = 'unknown'
    f.truncate(0)
    f.close()
#    except:
#        result = 'A synchronization error occured...'
#        f.truncate(0)
#        f.close()
