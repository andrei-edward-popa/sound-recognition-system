import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wf
from FeatureExtractor import FeatureExtractor
from MPEG7Features import audio_waveform_and_power, power_spectrum, audio_spectrum_envelope, audio_spectrum_centroid
from MPEG7Features import audio_spectrum_spread, audio_spectrum_flatness, harmonic_ratio_and_pitch, spectral_flux, spectral_rolloff
from Plot import plot_energy, plot_energy_entropy, plot_zero_crossing_rate, plot_FFT
from Plot import plot_signal, plot_audio_waveform, plot_audio_power, plot_power_spectrum, plot_audio_spectrum_envelope, plot_audio_spectrum_centroid
from Plot import plot_audio_spectrum_spread, plot_audio_spectrum_flatness, plot_harmonic_ratio, plot_pitch, plot_spectral_flux, plot_spectral_rolloff

audio_file = "" # Here add path to some wav file for testing
sr, signal = wf.read(audio_file)
signal_length = len(signal)
if signal.dtype.name == 'int16':
    signal = signal / 2**15
feature_type = 0 # 0 - MPEG7Features, 1 - FeatureExtractor

class Constants:
    m_excludedFrames = 7
    m_ratioSC = 0.5
    m_sampleRate = 16000
    m_timeHopSizeFlat = 30 * 10**(-3)
    m_timeHopSize = 10 * 10**(-3)
    m_timeFrameSize = 30 * 10**(-3)
    m_fftPoints = 1024
    m_resolution = 1 / 4
    m_integerBand = 16;
    m_lowerBandFlat = -8
    m_higherBandFlat = 24
    m_hopSize = int(m_sampleRate * m_timeHopSize)
    m_frameSize = int(m_sampleRate * m_timeFrameSize)
    m_hopSizeFlat = int(m_sampleRate * m_timeHopSizeFlat)
    m_signalLength = int(signal_length)
    m_noFrames = int(m_signalLength / m_hopSize)

bandsFlat = np.arange(Constants.m_higherBandFlat)
xFrames = np.arange(Constants.m_noFrames)
xFramesFlat = np.arange(int(Constants.m_signalLength / Constants.m_hopSizeFlat))
Tmax = Constants.m_signalLength / Constants.m_sampleRate
time = np.arange(Constants.m_signalLength) / Constants.m_sampleRate
indices = time * Constants.m_sampleRate;
frequency = np.arange(int(Constants.m_fftPoints/2+1)) * Constants.m_sampleRate / Constants.m_fftPoints

plt.close('all')
plot_signal(time, signal)

if feature_type == 0:
    min_values, max_values, audio_power_values = audio_waveform_and_power(signal, Constants.m_sampleRate, Constants.m_timeHopSize)
    freq, power_spectrum_values = power_spectrum(signal, Constants.m_sampleRate, Constants.m_timeHopSize, Constants.m_timeFrameSize, Constants.m_fftPoints)
    bands, audio_spectrum_envelope_values = audio_spectrum_envelope(signal, Constants.m_sampleRate, Constants.m_timeHopSize, Constants.m_timeFrameSize,
                                                             Constants.m_fftPoints, Constants.m_resolution, Constants.m_integerBand)
    audio_spectrum_centroid_values = audio_spectrum_centroid(signal, Constants.m_sampleRate, Constants.m_timeHopSize, Constants.m_timeFrameSize,
                                                      Constants.m_fftPoints, Constants.m_resolution, Constants.m_integerBand)
    audio_spectrum_spread_values = audio_spectrum_spread(signal, Constants.m_sampleRate, Constants.m_timeHopSize, Constants.m_timeFrameSize,
                                                  Constants.m_fftPoints, Constants.m_resolution, Constants.m_integerBand)
    audio_spectrum_flatness_values = audio_spectrum_flatness(signal, Constants.m_sampleRate, Constants.m_timeHopSizeFlat, Constants.m_timeFrameSize,
                                                      Constants.m_fftPoints, Constants.m_lowerBandFlat, Constants.m_higherBandFlat)
    harmonic_ratio_values, pitch_values = harmonic_ratio_and_pitch(signal, Constants.m_sampleRate, Constants.m_timeHopSize, Constants.m_timeFrameSize)
    spectral_flux_values = spectral_flux(signal, Constants.m_sampleRate, Constants.m_timeHopSize, Constants.m_timeFrameSize,
                                  Constants.m_fftPoints)
    spectral_rolloff_values = spectral_rolloff(signal, Constants.m_sampleRate, Constants.m_timeHopSize, Constants.m_timeFrameSize,
                                        Constants.m_fftPoints, Constants.m_ratioSC)
    
    plot_audio_waveform(xFrames, min_values, max_values)
    plot_audio_power(xFrames, audio_power_values)
    plot_power_spectrum(xFrames, freq, power_spectrum_values)
    plot_audio_spectrum_envelope(xFrames, bands, audio_spectrum_envelope_values)
    plot_audio_spectrum_centroid(xFrames, audio_spectrum_centroid_values)
    plot_audio_spectrum_spread(xFrames, audio_spectrum_spread_values)
    plot_audio_spectrum_flatness(xFramesFlat, bandsFlat, audio_spectrum_flatness_values)
    plot_harmonic_ratio(xFrames, harmonic_ratio_values)
    plot_pitch(xFrames, pitch_values)
    plot_spectral_flux(xFrames[:-int(Constants.m_frameSize/Constants.m_hopSize)], spectral_flux_values)
    plot_spectral_rolloff(xFrames, spectral_rolloff_values)
    
if feature_type == 1:
    audio_features = FeatureExtractor(audio_file, normalized=True, computeLLD=True)
    spectral_centroid_values = audio_features.m_spectralCentroid
    spectral_spread_values = audio_features.m_spectralSpread
    zero_crossing_rate_values = audio_features.m_ZCR
    spectral_flux_values = audio_features.m_spectralFlux
    spectral_rolloff_values = audio_features.m_spectralRolloff
    harmonic_ratio_values = audio_features.m_harmonicRatio
    pitch_values = audio_features.m_pitch
    energy_values = audio_features.m_energy
    energy_entropy_values = audio_features.m_energyEntropy
    
    xFrames = xFrames[0:Constants.m_noFrames - Constants.m_excludedFrames]
    
    plot_FFT(xFrames, frequency, power_spectrum_values)
    plot_audio_spectrum_centroid(xFrames, spectral_centroid_values)
    plot_audio_spectrum_spread(xFrames, spectral_spread_values)
    plot_harmonic_ratio(xFrames, harmonic_ratio_values)
    plot_pitch(xFrames, pitch_values)
    plot_spectral_flux(xFrames[:-1], spectral_flux_values)
    plot_spectral_rolloff(xFrames, spectral_rolloff_values)
    plot_zero_crossing_rate(xFrames, zero_crossing_rate_values)
    plot_energy(xFrames, energy_values)
    plot_energy_entropy(xFrames, energy_entropy_values)
