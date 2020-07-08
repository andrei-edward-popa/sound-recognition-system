for cl in classes:            
    for root, dirnames, filenames in os.walk(path + cl):
            for dirname in dirnames:
                for root_mi, dirnames_mi, filenames_mi in os.walk(root + '/' + dirname + '/'):
                    for file in tqdm(filenames_mi):
                        audio_features = FeatureExtractor(root_mi + file, normalized=True)
                        if audio_features.m_noFrames - 6 >= 10:
                            portion_len = int((audio_features.m_noFrames - 5) / samples)
                            sc = np.array([])
                            ss = np.array([])
                            zcr = np.array([])
                            sf = np.array([])
                            sro = np.array([])
                            hr = np.array([])
                            pit = np.array([])
#                            en = np.array([])
                            ee = np.array([])
#                            for i in range(samples):
#                                sc = np.append(sc, np.mean(audio_features.m_spectralCentroid[i * portion_len : (i + 1) * portion_len]))
#                                ss = np.append(ss, np.mean(audio_features.m_spectralSpread[i * portion_len : (i + 1) * portion_len]))
#                                zcr = np.append(zcr, np.mean(audio_features.m_ZCR[i * portion_len : (i + 1) * portion_len]))
#                                sf = np.append(sf, np.mean(audio_features.m_spectralFlux[i * portion_len : (i + 1) * portion_len]))
#                                sro = np.append(sro, np.mean(audio_features.m_spectralRolloff[i * portion_len : (i + 1) * portion_len]))
#                                hr = np.append(hr, np.mean(audio_features.m_harmonicRatio[i * portion_len : (i + 1) * portion_len]))
#                                pit = np.append(pit, np.mean(audio_features.m_pitch[i * portion_len : (i + 1) * portion_len]))
##                                en = np.append(en, np.mean(audio_features.m_energy[i * portion_len : (i + 1) * portion_len]))
#                                ee = np.append(ee, np.mean(audio_features.m_energyEntropy[i * portion_len : (i + 1) * portion_len]))
                            sc = np.append(sc, np.mean(audio_features.m_spectralCentroid))
                            ss = np.append(ss, np.mean(audio_features.m_spectralSpread))
                            zcr = np.append(zcr, np.mean(audio_features.m_ZCR))
                            sf = np.append(sf, np.mean(audio_features.m_spectralFlux))
                            sro = np.append(sro, np.mean(audio_features.m_spectralRolloff))
                            hr = np.append(hr, np.mean(audio_features.m_harmonicRatio))
                            pit = np.append(pit, np.mean(audio_features.m_pitch))
#                                en = np.append(en, np.mean(audio_features.m_energy[i * portion_len : (i + 1) * portion_len]))
                            ee = np.append(ee, np.mean(audio_features.m_energyEntropy))
                            sc = np.append(sc, np.var(audio_features.m_spectralCentroid))
                            ss = np.append(ss, np.var(audio_features.m_spectralSpread))
                            zcr = np.append(zcr, np.var(audio_features.m_ZCR))
                            sf = np.append(sf, np.var(audio_features.m_spectralFlux))
                            sro = np.append(sro, np.var(audio_features.m_spectralRolloff))
                            hr = np.append(hr, np.var(audio_features.m_harmonicRatio))
                            pit = np.append(pit, np.var(audio_features.m_pitch))
#                                en = np.append(en, np.mean(audio_features.m_energy[i * portion_len : (i + 1) * portion_len]))
                            ee = np.append(ee, np.var(audio_features.m_energyEntropy))
                            spectral_centroid_vector = np.vstack((spectral_centroid_vector, sc))
                            spectral_spread_vector = np.vstack((spectral_spread_vector, ss)) 
                            zero_crossing_rate_vector = np.vstack((zero_crossing_rate_vector, zcr)) 
                            spectral_flux_vector = np.vstack((spectral_flux_vector, sf)) 
                            spectral_rolloff_vector = np.vstack((spectral_rolloff_vector, sro)) 
                            harmonic_ratio_vector = np.vstack((harmonic_ratio_vector, hr)) 
                            pitch_vector = np.vstack((pitch_vector, pit)) 
#                            energy_vector = np.vstack((energy_vector, en)) 
                            energy_entropy_vector = np.vstack((energy_entropy_vector, ee)) 

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from Plot import plot_confusion_matrix
from FeatureExtractor import FeatureExtractor
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import recall_score, precision_score, accuracy_score

# /home/apopa/Desktop/sine.wav
# /home/apopa/Desktop/Clip-2.wav
# /home/apopa/Desktop/speech1.wav

path = '/home/apopa/Facultate/Licenta/dataset/'
classes = ['animals/', 'musical_instruments/', 'noises/', 'speech/']

hop_size = 10 * 10**(-3)
L_w = 30 * 10**(-3)
N_fft = 1024
spectralRolloffRatio = 0.5
audioFile = path + classes[0] + 'cello/cello_As4_05_pianissimo_arco-normal.wav'
samples = 10

testset_size = 0.25
n_neighbors = 1

df = pd.read_csv('./dataset/dataset.csv')
df.set_index('fname',inplace=True)

classes = list(np.unique(df.label))
labels = list(df.label)
        
labelencoder = LabelEncoder()
labelencoder.fit(labels)
classes_num = labelencoder.transform(labels)


#features = FeatureExtractor(audioFile, normalized=True)
#spectral_centroid = features.m_spectralCentroid
#spectral_spread = features.m_spectralSpread
#zero_crossing_rate = features.m_ZCR
#spectral_flux = features.m_spectralFlux
#spectral_rolloff = features.m_spectralRolloff
#harmonic_ratio = features.m_harmonicRatio
#pitch = features.m_pitch
#energy = features.m_energy
#energy_entropy = features.m_energyEntropy
#frames = features.m_frames
#signal = features.m_audioSignal;
#fft_magnitude = features.m_FFT

spectral_centroid_vector = np.array([])
spectral_centroid_vector = np.hstack((spectral_centroid_vector, np.arange(2)))
spectral_spread_vector = np.array([])
spectral_spread_vector = np.hstack((spectral_spread_vector, np.arange(2)))
zero_crossing_rate_vector = np.array([])
zero_crossing_rate_vector = np.hstack((zero_crossing_rate_vector, np.arange(2)))
spectral_flux_vector = np.array([])
spectral_flux_vector = np.hstack((spectral_flux_vector, np.arange(2)))
spectral_rolloff_vector = np.array([])
spectral_rolloff_vector = np.hstack((spectral_rolloff_vector, np.arange(2)))
harmonic_ratio_vector = np.array([])
harmonic_ratio_vector = np.hstack((harmonic_ratio_vector, np.arange(2)))
pitch_vector = np.array([])
pitch_vector = np.hstack((pitch_vector, np.arange(2)))
energy_entropy_vector = np.array([])
energy_entropy_vector = np.hstack((energy_entropy_vector, np.arange(2)))

for cl in classes:            
    for root, dirnames, filenames in os.walk(path + cl):
            for dirname in dirnames:
                for root_mi, dirnames_mi, filenames_mi in os.walk(root + '/' + dirname + '/'):
                    for file in tqdm(filenames_mi):
                        audio_features = FeatureExtractor(root_mi + file, normalized=True)
                        portion_len = int((audio_features.m_noFrames - 5) / samples)
                        sc = np.array([])
                        ss = np.array([])
                        zcr = np.array([])
                        sf = np.array([])
                        sro = np.array([])
                        hr = np.array([])
                        pit = np.array([])
                        ee = np.array([])
                        sc = np.append(sc, np.mean(audio_features.m_spectralCentroid))
                        ss = np.append(ss, np.mean(audio_features.m_spectralSpread))
                        zcr = np.append(zcr, np.mean(audio_features.m_ZCR))
                        sf = np.append(sf, np.mean(audio_features.m_spectralFlux))
                        sro = np.append(sro, np.mean(audio_features.m_spectralRolloff))
                        hr = np.append(hr, np.mean(audio_features.m_harmonicRatio))
                        pit = np.append(pit, np.mean(audio_features.m_pitch))
                        ee = np.append(ee, np.mean(audio_features.m_energyEntropy))
                        sc = np.append(sc, np.var(audio_features.m_spectralCentroid))
                        ss = np.append(ss, np.var(audio_features.m_spectralSpread))
                        zcr = np.append(zcr, np.var(audio_features.m_ZCR))
                        sf = np.append(sf, np.var(audio_features.m_spectralFlux))
                        sro = np.append(sro, np.var(audio_features.m_spectralRolloff))
                        hr = np.append(hr, np.var(audio_features.m_harmonicRatio))
                        pit = np.append(pit, np.var(audio_features.m_pitch))
                        ee = np.append(ee, np.var(audio_features.m_energyEntropy))
                        spectral_centroid_vector = np.vstack((spectral_centroid_vector, sc))
                        spectral_spread_vector = np.vstack((spectral_spread_vector, ss)) 
                        zero_crossing_rate_vector = np.vstack((zero_crossing_rate_vector, zcr)) 
                        spectral_flux_vector = np.vstack((spectral_flux_vector, sf)) 
                        spectral_rolloff_vector = np.vstack((spectral_rolloff_vector, sro)) 
                        harmonic_ratio_vector = np.vstack((harmonic_ratio_vector, hr)) 
                        pitch_vector = np.vstack((pitch_vector, pit)) 
                        energy_entropy_vector = np.vstack((energy_entropy_vector, ee)) 
                        
                        
scaler = StandardScaler()
scaled_spectral_centroid_vector = scaler.fit_transform(spectral_centroid_vector[1:])
scaled_spectral_spread_vector = scaler.fit_transform(spectral_spread_vector[1:])
scaled_zero_crossing_rate_vector = scaler.fit_transform(zero_crossing_rate_vector[1:])
scaled_spectral_flux_vector = scaler.fit_transform(spectral_flux_vector[1:])
scaled_spectral_rolloff_vector = scaler.fit_transform(spectral_rolloff_vector[1:])
scaled_harmonic_ratio_vector = scaler.fit_transform(harmonic_ratio_vector[1:])
scaled_pitch_vector = scaler.fit_transform(pitch_vector[1:])
scaled_energy_entropy_vector = scaler.fit_transform(energy_entropy_vector[1:])
scaled_feature_vectors = scaled_spectral_centroid_vector
scaled_feature_vectors = np.append(scaled_feature_vectors, scaled_spectral_spread_vector, 1)
scaled_feature_vectors = np.append(scaled_feature_vectors, scaled_zero_crossing_rate_vector, 1)
scaled_feature_vectors = np.append(scaled_feature_vectors, scaled_spectral_flux_vector, 1)
scaled_feature_vectors = np.append(scaled_feature_vectors, scaled_spectral_rolloff_vector, 1)
scaled_feature_vectors = np.append(scaled_feature_vectors, scaled_harmonic_ratio_vector, 1)
scaled_feature_vectors = np.append(scaled_feature_vectors, scaled_pitch_vector, 1)
scaled_feature_vectors = np.append(scaled_feature_vectors, scaled_energy_entropy_vector, 1)


splitter = StratifiedShuffleSplit(n_splits=1, test_size=testset_size, random_state=1)
splits = splitter.split(scaled_feature_vectors, classes_num)
for train_index, test_index in splits:
    train_set = scaled_feature_vectors[train_index]
    test_set = scaled_feature_vectors[test_index]
    train_classes = classes_num[train_index]
    test_classes = classes_num[test_index]

model_knn = KNeighborsClassifier(n_neighbors=n_neighbors)
model_knn.fit(train_set, train_classes)
predicted_labels = model_knn.predict(test_set)

print("Recall: ", recall_score(test_classes, predicted_labels,average=None))
print("Precision: ", precision_score(test_classes, predicted_labels,average=None))
print("F1-Score: ", f1_score(test_classes, predicted_labels, average=None))
print("Accuracy: %.2f," % accuracy_score(test_classes, predicted_labels,normalize=True), accuracy_score(test_classes, predicted_labels,normalize=False) )
print("Number of samples:",test_classes.shape[0])

cnf_matrix = confusion_matrix(test_classes, predicted_labels)
np.set_printoptions(precision=2)

plt.close('all')    
plt.figure(1, figsize=(5,5))
plot_confusion_matrix(cnf_matrix, classes=labelencoder.classes_,
                      title='Confusion matrix, without normalization')


                        
#
#plt.close('all')
#
#l = list(range(features.m_noFrames - 5))
#f = np.array(range(0,int(features.m_fftPoints/2+1))) * features.m_sampleRate / features.m_fftPoints
#plt.figure(1)
#plt.imshow(np.array(fft_magnitude).transpose(), origin='lower', extent=[l[0],l[-1],f[0],f[-1]], aspect='auto')
#plt.colorbar()
#
#plt.figure(2)
#plt.plot(l, spectral_centroid, 'b')
#plt.title('Spectral Centroid')
#
#plt.figure(3)
#plt.plot(l, spectral_spread, 'b')
#plt.title('Spectral Spread')
#
#plt.figure(4)
#plt.plot(l, zero_crossing_rate, 'b')
#plt.title('Zero Crossing Rate')
#
#plt.figure(5)
#plt.plot(l[0:len(l)-1], spectral_flux, 'b')
#plt.title('Spectral Flux')
#
#plt.figure(6)
#plt.plot(l, spectral_rolloff * features.m_sampleRate, 'b')
#plt.title('Spectral Rolloff')
#
#plt.figure(7)
#plt.plot(l, harmonic_ratio, 'b')
#plt.title('Harmonic Ratio')
#
#plt.figure(8)
#plt.plot(l, pitch, 'b')
#plt.title('Pitch')
#
#plt.figure(9)
#plt.plot(l, energy, 'b')
#plt.title('Energy')
#
#plt.figure(10)
#plt.plot(l, energy_entropy, 'b')
#plt.title('Energy Entropy')
#
#plt.figure(11)
#plt.plot(features.m_audioSignal, 'b')
#plt.title('Signal')


