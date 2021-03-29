import os
import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm
import soundfile as sf
from pydub import AudioSegment
from scipy.io import wavfile as wf
from MPEG7Features import computeFilterBank
from FeatureExtractor import FeatureExtractor

class Constants:
    """
    A storage for constants.
     
    Attributes
    ----------
    
    m_fftPoints : int > 0
        Total number of FFT coefficients to compute.
    m_sampleRate : int > 0
        Sample rate of signals.
    m_nfilt : int > 0
        Number of filters from MFCC filter bank.
        
    Methods
    -------
    
    None
    """
    m_fftPoints = 512
    m_sampleRate = 16000
    m_nfilt = 40

def mp3_to_wav(path):
    """
    Convert mp3 files to wav files.
    The directory specified by the path must contain directories with audio segments.
    Files that are not mp3 will be ignored and mp3 files will be removed and replaced by wav files.
    
    Parameters
    ----------
    
    path : str
        Path to a directory which contains directories with audio segments.
    """
    
    for root, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            for root_mi, dirnames_mi, filenames_mi in os.walk(root + '/' + dirname + '/'):
                for mp3_file in tqdm(filenames_mi):
                    if mp3_file.split('.')[1] == 'mp3':
                        path_to_mp3_file = path + dirname + '/' + mp3_file
                        path_to_wav_file = path + dirname + '/' + mp3_file.split('.')[0] + '.wav'
                        sound = AudioSegment.from_mp3(path_to_mp3_file)
                        sound.export(path_to_wav_file, format='wav')
                        os.remove(path_to_mp3_file)     
              
def flac_to_wav(path):
    """
    Convert flac files to wav files.
    The directory specified by the path must contain directories with audio segments.
    Files that are not flac will be ignored and flac files will be removed and replaced by wav files.
    
    Parameters
    ----------
    
    path : str
        Path to a directory which contains directories with audio segments.
    """
    
    for root, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            for root_mi, dirnames_mi, filenames_mi in os.walk(root + '/' + dirname + '/'):
                for flac_file in tqdm(filenames_mi):
                    if flac_file.split('.')[1] == 'flac':
                        path_to_flac_file = path + dirname + '/' + flac_file
                        path_to_wav_file = path + dirname + '/' + flac_file.split('.')[0] + '.wav'
                        sound, rate = sf.read(path_to_flac_file)
                        wf.write(filename=path_to_wav_file, rate=rate, data=sound)
                        os.remove(path_to_flac_file)

def create_csv(path, classes, csv_name):
    """
    Create a csv file with name of the audio segments (fname) and his class (label).
    The directory specified by the path must contain directories with audio segments.
    The fname column will be the index of the csv file.
    
    Parameters
    ----------
    
    path : str
        Path to a directory which contains directories with audio segments.
    classes : array-like
        An array of strings which represents classes that are present in directory (path). 
        Strings that are found in array must have the name of the subdirectories.
    csv_name : str
        The name of the csv file to be created (can be a path togheter with csv filename).
    """
    
    data_frame = pd.DataFrame([], columns = ['fname' , 'label'])
    for cl in sorted(classes):
        for root, dirnames, filenames in os.walk(path + cl):
                for dirname in sorted(dirnames):
                    for root_mi, dirnames_mi, filenames_mi in os.walk(root + '/' + dirname + '/'):
                        for file in tqdm(sorted(filenames_mi)):       
                            data_frame = data_frame.append({'fname' : file, 'label' : cl} , ignore_index=True)
    data_frame.set_index('fname',inplace=True)
    data_frame.to_csv(csv_name)

def move_files(old_path, new_path, search):
    """
    Move files from a directory to another if the filename contains at least one string from 'search'.
    
    Parameters
    ----------
    
    old_path : str
        Path to a directory which contains directories with files.
    new_path : str
        Path to the directory where you want to move the files.
    search : array-like
        An array of strings which represents the patters you want to contain filenames for moving it. 
    """
    
    for root, dirnames, filenames in os.walk(old_path):
        for dirname in dirnames:
            for root_mi, dirnames_mi, filenames_mi in os.walk(root + '/' + dirname + '/'):
                for file in tqdm(filenames_mi):
                    for item in search:
                        if item in file:
                            os.rename(old_path + dirname + '/' + file, new_path + file)

def remove_low_power(signal, sr=16000, window=1600, threshold=0.0005):
    """
    Create a mask for removing low power zones.
    
    Parameters
    ----------
    signal : numpy-array
        A 1D numpy array which represents the input signal.
    sr : int > 0, optional (default : 16000)
        The sample rate (in samples/sec).
    window : int > 0, optional (default : 1600)
        Frame length, in order to compute the power for the specific frame.
    threshold : float > 0, optional (default : 0.0005)
        If frame power is less than threshold value, the frame needs to be removed.
        
    Returns
    -------
    mask : numpy-array
        A 1D numpy array with boolean values, where False means that the sample needs to be removed.
    """
    
    mask = np.array([], dtype=bool)
    signal = pd.Series(signal).apply(np.abs);
    signal_mean = signal.rolling(window=window, min_periods=1, center=True).mean()
    for mean in signal_mean:
        if mean > threshold:
            mask = np.append(mask, True)
        else:
            mask = np.append(mask, False)
    return mask

def clean_audio(old_path, new_path, sr=16000, threshold=0.0005):
    """
    Change sample rate of wav files to 'sr' and remove portions of the audio segments where power is lower than 'threshold'.
    For power check, a frame is defined by (sr/10).
    
    Parameters
    ----------
    
    old_path : str
        Path to a directory which contains directories with wav files only.
    new_path : str
        Path to a directory which contains same directories with 'old_path'. Clean files will be written in new path's directories.
    sr : int > 0, optional (default : 16000)
        The sample rate (in samples/sec).
    threshold : float > 0, optional (default : 0.0005)
        If frame power is less than threshold value, the frame needs to be removed.
    """
    
    for root, dirnames, filenames in os.walk(old_path):
        for dirname in dirnames:
            for root_mi, dirnames_mi, filenames_mi in os.walk(root + '/' + dirname + '/'):
                for file in tqdm(filenames_mi):
                    if file.split('.')[1] == 'wav':
                        signal, rate = librosa.load(old_path + dirname + '/' + file, sr=sr)
                        mask = remove_low_power(signal=signal, sr=rate, window=int(rate/10), threshold=threshold)
                        wf.write(filename=new_path + dirname + '/' + file, rate=rate, data=signal[mask])
                        

def create_csv_features_labels(path_to_dataset, csv_name):
    """
    Create a csv file with name of the audio segments, his classes and values of mean and variance for descriptors defined in FeatureExtractor class.
    The directory specified by the path_to_dataset must contain directories with audio segments.
    The fname column (audio signal name) will be the index of the csv file.
    
    Parameters
    ----------
    
    path_to_dataset : str
        Path to a directory which contains directories with audio segments.
    csv_name : str
        The name of the csv file to be created (can be a path togheter with csv filename).
    """
    
    fbank = computeFilterBank(Constants.m_fftPoints, Constants.m_sampleRate, Constants.m_nfilt)
    classes = list(os.walk(path_to_dataset))[0][1]
    
    data_frame = pd.DataFrame([], columns = ['fname', 'label_1st', 'label_2rd', 'mean_sc', 'var_sc', 'mean_ss', 'var_ss', 'mean_sf', 'var_sf', 'mean_ee', 'f0',
                                             'mfcc1', 'mfcc2', 'mfcc3', 'mfcc4', 'mfcc5', 'mfcc6', 'mfcc7', 'mfcc8', 'mfcc9', 'mfcc10', 'mfcc11', 'mfcc12', 'mfcc13'
                                             ])
    
    for cl in sorted(classes):            
        for root, dirnames, filenames in os.walk(path_to_dataset + cl):
            for dirname in sorted(dirnames):
                for root_mi, dirnames_mi, filenames_mi in os.walk(root + '/' + dirname + '/'):
                    for file in tqdm(sorted(filenames_mi)):
                        audio_features = FeatureExtractor(root_mi + file, fbank=fbank, fftPoints=512, normalized=True, computeLLD=True)
                        for i in range(0, len(audio_features.m_spectralFlux), 16):
                            mean_sc = np.mean(audio_features.m_spectralCentroid[i:i+16])
                            mean_ss = np.mean(audio_features.m_spectralSpread[i:i+16])
                            mean_ee = np.mean(audio_features.m_energyEntropy[i:i+16])
                            mean_sf = np.mean(audio_features.m_spectralFlux[i:i+16])
                            var_sc = np.var(audio_features.m_spectralCentroid[i:i+16])
                            var_ss = np.var(audio_features.m_spectralSpread[i:i+16])
                            var_sf = np.var(audio_features.m_spectralFlux[i:i+16])
                            mfcc = np.mean(audio_features.m_MFCC[i:i+16],axis=0)
                            f0 = np.array([el for el in audio_features.m_pitch[i:i+16] if el >= 50 and el <= 300])
                            if len(f0) == 0:
                                f0 = 0
                            else:
                                f0 = np.mean(f0)
                            data_frame = data_frame.append({'fname': file, 'label_1st': cl, 'label_2rd': dirname,
                                                            'mean_sc': mean_sc, 'var_sc': var_sc,
                                                            'mean_ss': mean_ss, 'var_ss': var_ss, 
                                                            'mean_sf': mean_sf, 'var_sf': var_sf, 
                                                            'mean_ee': mean_ee,
                                                            'f0': f0,
                                                            'mfcc1': mfcc[0], 'mfcc2': mfcc[1], 'mfcc3': mfcc[2], 'mfcc4': mfcc[3],
                                                            'mfcc5': mfcc[4], 'mfcc6': mfcc[5], 'mfcc7': mfcc[6], 'mfcc8': mfcc[7],
                                                            'mfcc9': mfcc[8], 'mfcc10': mfcc[9], 'mfcc11': mfcc[10], 'mfcc12': mfcc[11],
                                                            'mfcc13': mfcc[12]
                                                            }, ignore_index=True)
        
    data_frame.set_index('fname',inplace=True)
    data_frame.to_csv(csv_name)

                        