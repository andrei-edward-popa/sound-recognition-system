import librosa
import numpy as np
from math import floor
from scipy.fftpack import fft

def computeFilterBank(fftPoints=512, sampleRate=16000, nfilt=40):
    low_freq_mel = 0
    high_freq_mel = (2595 * np.log10(1 + (sampleRate / 2) / 700))
    freq_mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)
    freq_hz_points = (700 * (10**(freq_mel_points / 2595) - 1))
    bins = np.floor(fftPoints * freq_hz_points / sampleRate)
    
    fbank = np.zeros((nfilt, int(np.floor(fftPoints / 2))))
    for i in range(1, nfilt + 1):
        f_left = int(bins[i - 1])
        f_current = int(bins[i])
        f_right = int(bins[i + 1])
    
        for j in range(f_left, f_current):
            fbank[i - 1, j] = (j - bins[i - 1]) / (bins[i] - bins[i - 1])
        for j in range(f_current, f_right):
            fbank[i - 1, j] = (bins[i + 1] - j) / (bins[i + 1] - bins[i])
    enorm = 2.0 / (freq_hz_points[2:nfilt+2] - freq_hz_points[:nfilt])
    fbank *= enorm[:, np.newaxis]
    return fbank

def mfcc_and_deltas(signal, sr=16000, n_mels=128, n_mfcc=13, width=13):
    """
    Extract MFCC, Delta MFCC and Delta Delta MFCC Coefficients.
    
    Parameters
    ----------
    signal : numpy-array
        A 1D numpy array which represents the input signal.
    sr : int > 0, optional (default : 16000)
        The sample rate (in samples/sec).
    n_mels : int > 0, optional (default : 128)
        Number of mel coefficients per frame.
    n_mfcc : int > 0, optional (default : 13)
        Number of MFCC, Delta MFCC and Delta Delta MFCC coefficients to return.
    width : int > 0, optional (default : 13)
        Number of frames over which to compute the delta features.
        
    Returns
    -------
    mfcc : numpy-array
        A 1D numpy array which contains the MFCC coefficients.
    mfcc_delta : numpy-array
        A 1D numpy array which contains the Delta MFCC coefficients.
    mfcc_delta_delta : numpy-array
        A 1D numpy array which contains the Delta Delta MFCC coefficients.
    """
    
    S = librosa.feature.melspectrogram(signal, sr=sr, n_mels=n_mels)
    mfcc = librosa.feature.mfcc(S=librosa.power_to_db(S), n_mfcc=n_mfcc)
    mfcc_delta = np.mean(librosa.feature.delta(mfcc, width=width), 1)
    mfcc_delta_delta = np.mean(librosa.feature.delta(mfcc, width=width, order=2), 1)
    mfcc = np.mean(mfcc, 1)
    return mfcc, mfcc_delta, mfcc_delta_delta


def min_max_and_energy_frame(frame):
    """
    Minimum, maximum and energy value of the given frame.
    
    Parameters
    ----------
    frame : numpy-array
        A 1D numpy array which represents the input signal.
        
    Returns
    -------
    min : float
        Minimum value found in frame.
    max : float
        Maximum value found in frame.
    energy : float
        Total energy of the frame.
    """
    
    return np.min(frame), np.max(frame), np.sum(frame ** 2)


def audio_waveform_and_power(signal, sr=16000, hop_size=0.01):
    """
    (Audio Waveform) and (Audio Power) low level descriptors (LLD).
    
    Parameters
    ----------
    signal : numpy-array
        A 1D numpy array which represents the input signal.
    sr : int > 0, optional (default : 16000)
        The sample rate (in samples/second).
    hop_size : float > 0, optional (default : 0.01)
        Time interval between two successive time frames (in seconds).
    
    Returns
    -------
    audio_waveform_min_values : numpy-array
        A 1D numpy array containing the minumum value for every frame, corresponding to hop_size.
    audio_waveform_max_values : numpy-array
        A 1D numpy array containing the maximum value for every frame, corresponding to hop_size.
    audio_power : numpy-array
        A 1D numpy array containing the audio power value for every frame, corresponding to hop_size.
    """
    
    N_hop = int(sr * hop_size)
    N_sig = len(signal);
    no_frames = int(N_sig / N_hop);
    audio_waveform_min_values = np.array([])
    audio_waveform_max_values = np.array([])
    audio_power = np.array([])
    for i in range(no_frames):
        frame = np.array(signal[i * N_hop : (i + 1) * N_hop])
        min_value, max_value, audio_power_value = min_max_and_energy_frame(frame)
        audio_power_value = audio_power_value / N_hop
        audio_waveform_min_values = np.append(audio_waveform_min_values, min_value)
        audio_waveform_max_values = np.append(audio_waveform_max_values, max_value)
        audio_power = np.append(audio_power, audio_power_value)      
    return audio_waveform_min_values, audio_waveform_max_values, audio_power


def power_spectrum_frame(frame, N_fft=1024):
    """
    Power Spectrum of the given frame.
    
    Parameters
    ----------
    frame : numpy-array
        A 1D numpy array which represents the input signal.
    N_fft : int > 0, optional (default : 1024)
        Number of power spectrum coefficients to compute.    
    
    Returns
    -------
    power_spectrum : numpy-array
        A 1D numpy array containing (N_fft / 2) points of power spectrum.
    """
    N_w = len(frame)
    arr = np.zeros(N_fft)
    arr[:N_w] = frame
    frame = arr
    fft_magnitude = np.abs(fft(frame))[0:int(N_fft/2+1)]
    power_spectrum = np.array(fft_magnitude / (N_fft * N_w))
    power_spectrum[0] *= 2
    power_spectrum[int(N_fft/2)] *= 2
    return power_spectrum


def power_spectrum(signal, sr=16000, hop_size=0.01, L_w=0.03, N_fft=1024):
    """
    (Frequency Axis) and (Power Spectrum) low level descriptor (LLD).
    
    Parameters
    ----------
    signal : numpy-array
        A 1D numpy array which represents the input signal.
    sr : int > 0, optional (default : 16000)
        The sample rate (in samples/second).
    hop_size : float > 0, optional (default : 0.01)
        Time interval between two successive time frames (in seconds).
    L_w : float > 0, optional (default : 0.03)
        Length of a time frame (in seconds).    
    N_fft : int > 0, optional (default : 1024)
        Total number of power spectrum coefficients to compute. 
    
    Returns
    -------
    frequency : numpy-array
        A 1D numpy array containing frequency axis values, from 0 to (sr/2).
    power_spectrum : numpy-array
        A 2D numpy-array containing power spectrum for every frame of the input signal.
    """
    
    N_w = int(L_w * sr);
    N_hop = int(sr * hop_size)
    N_sig = len(signal);
    no_frames = int(N_sig / N_hop);
    power_spectrum_signal = np.array([])
    frame = np.array(signal[0:N_w])
    power_spectrum_fr = power_spectrum_frame(frame, N_fft)
    power_spectrum_signal = np.hstack((power_spectrum_signal, power_spectrum_fr))
    frequency = np.array(range(0,int(N_fft/2+1))) * sr / N_fft
    for i in range(1, no_frames):
        frame = np.array(signal[i * N_hop : i * N_hop + N_w])
        power_spectrum_fr = power_spectrum_frame(frame, N_fft)
        power_spectrum_signal = np.vstack((power_spectrum_signal, power_spectrum_fr))
    return frequency, power_spectrum_signal


def audio_spectrum_envelope_frame(frame, sr, N_fft, r, n):
    lo_edge = 1000 * (2 ** (-r * n))
    hi_edge = 1000 * (2 ** (r * n))
    b_in = int(8 / r)
    power_spectrum = power_spectrum_frame(frame, N_fft)
    ASE = []
    resolution = 0.5
    ASE.append(sum(power_spectrum[0:round(lo_edge * N_fft / sr + resolution) + 1]))
    for b in range(b_in):
        lo_Fb = lo_edge * 2 ** (r * b)
        hi_Fb = lo_edge * 2 ** (r * (b + 1))
        lo_Kb = round(lo_Fb * N_fft / sr - resolution);
        hi_Kb = round(hi_Fb * N_fft / sr + resolution);
        band_sum = sum(power_spectrum[lo_Kb:hi_Kb + 1])
        ASE.append(band_sum)
    ASE.append(sum(power_spectrum[round(hi_edge * N_fft / sr - resolution):int(N_fft / 2 + 1)]))
    return ASE


def audio_spectrum_envelope(signal, sr, hop_size, L_w, N_fft, r, n):
    N_w = int(L_w * sr);
    N_hop = int(sr * hop_size)
    N_sig = len(signal);
    no_frames = int(N_sig / N_hop);
    ASE = []
    b_in = int(8 / r)
    bands = list(range(b_in + 2))
    for i in range(no_frames):
        frame = np.array(signal[i * N_hop : i * N_hop + N_w])
        ASE_fr = audio_spectrum_envelope_frame(frame, sr, N_fft, r, n)
        ASE.append(ASE_fr)
    return bands, ASE


def modified_power_spectrum(frame, sr, N_fft, r, n):
    lo_edge = 1000 * (2 ** (-r * n))
    K_low = floor(lo_edge * N_fft / sr)
    power_spectrum = power_spectrum_frame(frame, N_fft)
    modified_power_spectrum = []
    modified_frequency = []
    modified_power_spectrum.append(sum(power_spectrum[0:K_low+1]))
    modified_frequency.append(lo_edge / 2)
    f = np.array(range(0,int(N_fft/2+1))) * sr / N_fft
    for i in range(1,int(N_fft/2-K_low + 1)):
        modified_power_spectrum.append(power_spectrum[i + K_low]);
        modified_frequency.append(f[i + K_low])
    return modified_frequency, modified_power_spectrum


def audio_spectrum_centroid_frame(frame, sr, N_fft, r, n):
    mf, mps = modified_power_spectrum(frame, sr, N_fft, r, n)
    ASC = np.sum(np.log2(np.array(mf) / 1000) * np.array(mps)) / np.sum(np.array(mps))
    return ASC


def audio_spectrum_centroid(signal, sr, hop_size, L_w, N_fft, r, n):
    N_w = int(L_w * sr);
    N_hop = int(sr * hop_size)
    N_sig = len(signal);
    no_frames = int(N_sig / N_hop);
    ASC = []
    for i in range(no_frames):
        frame = np.array(signal[i * N_hop : i * N_hop + N_w])
        ASC_fr = audio_spectrum_centroid_frame(frame, sr, N_fft, r, n)
        ASC.append(ASC_fr)
    return ASC


def audio_spectrum_spread_frame(frame, sr, N_fft, r, n):
    mf, mps = modified_power_spectrum(frame, sr, N_fft, r, n)
    ASC = audio_spectrum_centroid_frame(frame, sr, N_fft, r, n)
    ASS = np.sqrt(np.sum(((np.log2(np.array(mf) / 1000) - ASC) ** 2) * np.array(mps)) / np.sum(np.array(mps)))
    return ASS
    

def audio_spectrum_spread(signal, sr, hop_size, L_w, N_fft, r, n):
    N_w = int(L_w * sr);
    N_hop = int(sr * hop_size)
    N_sig = len(signal);
    no_frames = int(N_sig / N_hop);
    ASS = []
    for i in range(no_frames):
        frame = np.array(signal[i * N_hop : i * N_hop + N_w])
        ASS_fr = audio_spectrum_spread_frame(frame, sr, N_fft, r, n)
        ASS.append(ASS_fr)
    return ASS


def audio_spectrum_flatness_frame(frame, sr, N_fft, n, B):
    lo_edge = 1000 * 2**(n / 4)
    power_spectrum = power_spectrum_frame(frame, N_fft)
    ASF = []
    n = 0
    for b in range(B):
        lo_Fb = lo_edge * 2**(b / 4)
        hi_Fb = lo_edge * 2**((b + 1)/4)
        lo_Kb = round(lo_Fb * N_fft / sr)
        hi_Kb = round(hi_Fb * N_fft / sr)
        group_power_spectrum = []
        if (hi_Fb <= 1000):
            group_power_spectrum = power_spectrum[lo_Kb:hi_Kb]
            length = len(group_power_spectrum)
            ASF_b = (np.prod(np.array(group_power_spectrum)) ** (1/length)) / (np.sum(np.array(group_power_spectrum)) / length)
            ASF.append(ASF_b)
        else:
            if not (lo_Fb >= 1000 * 2**n and hi_Fb <= 1000 * 2**(n+1)):
                n += 1
            if lo_Fb >= 1000 * 2**n and hi_Fb <= 1000 * 2**(n+1):
                for i in range(lo_Kb, hi_Kb, 2**(n+1)):
                    if hi_Kb - i >= 2**n:
                        ps = power_spectrum[i:i+2**(n+1)]
                    else:
                        continue
                    if len(ps > 0) :
                        group_power_spectrum.append(np.sum(ps) / len(ps))
                    else:
                        group_power_spectrum.append(0)
            ASF_b = 0
            length = len(group_power_spectrum)
            num = (np.prod(np.array(group_power_spectrum)) ** (1/length))
            den = (np.sum(np.array(group_power_spectrum)) / length)
            if length != 0 and den != 0:
                ASF_b = num / den
            ASF.append(ASF_b)  
    return ASF


def audio_spectrum_flatness(signal, sr, hop_size, L_w, N_fft, n, B):
    N_w = int(L_w * sr);
    N_hop = int(sr * hop_size)
    N_sig = len(signal);
    no_frames = int(N_sig / N_hop);
    ASF = []
    for i in range(no_frames):
        frame = np.array(signal[i * N_hop : i * N_hop + N_w])
        ASF_fr = audio_spectrum_flatness_frame(frame, sr, N_fft, n, B)
        ASF.append(ASF_fr)
    return ASF


def zero_crossing_rate(frame):
    length = len(frame)
    count_zeros = np.sum(np.abs(np.diff(np.sign(frame)))) / 2
    return count_zeros / (length - 1)


def harmonic_ratio_and_pitch_frame(frame, sr, eps):
    M = np.round(0.04 * sr) - 1
    r = np.correlate(frame, frame, mode='full')
    g = r[len(frame) - 1]
    r = r[len(frame):-1]
    [a, ] = np.nonzero(np.diff(np.sign(r)))
    if len(a) == 0:
        M0 = len(r) - 1
    else:
        M0 = a[0]
    if M > len(r):
        M = len(r) - 1
    gamma = np.zeros(M)
    cumulative_sum = np.cumsum(frame ** 2)
    gamma[M0:M] = r[M0:M] / (np.sqrt((g * cumulative_sum[M:M0:-1])) + eps)
    zcr = zero_crossing_rate(gamma)
    if zcr > 0.5:
        harmonic_ratio = 0.0
        pitch = 0.0
    else:
        if len(gamma) == 0:
            harmonic_ratio = 1.0
            pitch_index = 0.0
            gamma = np.zeros((M), dtype=np.float64)
        else:
            harmonic_ratio = np.max(gamma)
            pitch_index = np.argmax(gamma)
        pitch = sr / (pitch_index + eps)
        if pitch > sr / 2:
            pitch = 0.0
        if harmonic_ratio < 0.1:
            pitch = 0.0
    return harmonic_ratio, pitch


def harmonic_ratio_and_pitch(signal, sr, hop_size, L_w):
    N_w = int(L_w * sr);
    N_hop = int(sr * hop_size)
    N_sig = len(signal);
    no_frames = int(N_sig / N_hop);
    harmonic_ratios = []
    pitches = []
    for i in range(no_frames):
        frame = np.array(signal[i * N_hop : i * N_hop + N_w])
        harmonic_ratio, pitch = harmonic_ratio_and_pitch_frame(frame, sr, 0.00001)
        harmonic_ratios.append(harmonic_ratio)
        pitches.append(pitch)
    return harmonic_ratios, pitches


def spectral_flux_frame(current_frame, previous_frame, N_fft):
    current_frame_power_spectrum = power_spectrum_frame(current_frame, N_fft)
    previous_frame_power_spectrum = power_spectrum_frame(previous_frame, N_fft)
    spectral_flux = np.sum((current_frame_power_spectrum - previous_frame_power_spectrum) ** 2)
    return spectral_flux


def spectral_flux(signal, sr, hop_size, L_w, N_fft):
    N_w = int(L_w * sr);
    N_hop = int(sr * hop_size)
    N_sig = len(signal);
    no_frames = int(N_sig / N_hop);
    spectral_flux = []
    for i in range(int(N_w/N_hop), no_frames):
        current_frame = np.array(signal[i * N_hop - N_w: i * N_hop])
        previous_frame = np.array(signal[i * N_hop : i * N_hop + N_w])
        spectral_flux_fr = spectral_flux_frame(current_frame, previous_frame, N_fft)
        spectral_flux.append(spectral_flux_fr)
    return spectral_flux


def spectral_rolloff_frame(frame, N_fft, ratio):
    power_spectrum = power_spectrum_frame(frame, N_fft)
    energy = np.sum(power_spectrum ** 2)
    threshold = ratio * energy
    cumsum = np.cumsum(power_spectrum ** 2)
    check = np.nonzero(cumsum > threshold)[0]
    if len(check) > 0:
        spectral_rolloff = check[0] / N_fft
    else:
        spectral_rolloff = 0.0
    return spectral_rolloff


def spectral_rolloff(signal, sr, hop_size, L_w, N_fft, ratio=0.85):
    N_w = int(L_w * sr);
    N_hop = int(sr * hop_size)
    N_sig = len(signal);
    no_frames = int(N_sig / N_hop);
    spectral_rolloff = []
    for i in range(no_frames):
        frame = np.array(signal[i * N_hop : i * N_hop + N_w])
        spectral_rolloff_fr = spectral_rolloff_frame(frame, N_fft, ratio)
        spectral_rolloff.append(spectral_rolloff_fr)
    return spectral_rolloff