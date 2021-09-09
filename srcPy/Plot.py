import itertools
import numpy as np
import matplotlib.pyplot as plt

def plot_signal(time, signal):
    plt.figure()
    plt.plot(time, signal, 'b')
    plt.xlabel('Time [s]'), plt.ylabel('Amplitude'), plt.title('Input Signal')

def plot_audio_waveform(no_frames, min_values, max_values):
    plt.figure()
    plt.plot(no_frames, min_values, 'b')
    plt.plot(no_frames, max_values, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Audio Waveform')

def plot_audio_power(no_frames, audio_power):
    plt.figure()
    plt.plot(no_frames, audio_power, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Audio Power')

def plot_FFT(no_frames, frequency, FFT):
    plt.figure()
    plt.imshow(FFT.transpose(), origin='lower', extent=[no_frames[0],no_frames[-1],frequency[0],frequency[-1]], aspect='auto')
    plt.colorbar().ax.set_ylabel('Amplitude', rotation=0, position=(0,1))
    plt.xlabel('Frame Number'), plt.ylabel('Frequency [Hz]'), plt.title('FFT')

def plot_power_spectrum(no_frames, frequency, power_spectrum):
    plt.figure()
    plt.imshow(power_spectrum.transpose(), origin='lower', extent=[no_frames[0],no_frames[-1],frequency[0],frequency[-1]], aspect='auto')
    plt.colorbar().ax.set_ylabel('Amplitude', rotation=0, position=(0,1))
    plt.xlabel('Frame Number'), plt.ylabel('Frequency [Hz]'), plt.title('Power Spectrum')
    
def plot_audio_spectrum_envelope(no_frames, bands, audio_spectrum_envelope):
    plt.figure()
    plt.imshow(np.array(audio_spectrum_envelope).transpose(), origin='lower', extent=[no_frames[0],no_frames[-1],bands[0],bands[-1]+1], aspect='auto')
    plt.colorbar().ax.set_ylabel('Amplitude', rotation=0, position=(0,1))
    plt.xlabel('Frame Number'), plt.ylabel('Bands'), plt.title('Audio Spectrum Envelope')
    
def plot_audio_spectrum_centroid(no_frames, audio_spectrum_centroid):
    plt.figure()
    plt.plot(no_frames, audio_spectrum_centroid, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Audio Spectrum Centroid')

def plot_audio_spectrum_spread(no_frames, audio_spectrum_spread):
    plt.figure()
    plt.plot(no_frames, audio_spectrum_spread, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Audio Spectrum Spread')
    
def plot_audio_spectrum_flatness(no_frames, bands, audio_spectrum_flatness):
    plt.figure()
    plt.imshow(np.array(audio_spectrum_flatness).transpose(), origin='lower', extent=[no_frames[0],no_frames[-1],bands[0],bands[-1]+1], aspect='auto')
    plt.colorbar().ax.set_ylabel('Amplitude', rotation=0, position=(0,1))
    plt.xlabel('Frame Number'), plt.ylabel('Bands'), plt.title('Audio Spectrum Flatness')
    
def plot_harmonic_ratio(no_frames, harmonic_ratio):
    plt.figure()
    plt.plot(no_frames, harmonic_ratio, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Harmonic Ratio')
    
def plot_pitch(no_frames, pitch):
    plt.figure()
    plt.plot(no_frames, pitch, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Pitch')
    
def plot_spectral_flux(no_frames, spectral_flux):
    plt.figure()
    plt.plot(no_frames, spectral_flux, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Spectral Flux')
    
def plot_spectral_rolloff(no_frames, spectral_rolloff):
    plt.figure()
    plt.plot(no_frames, spectral_rolloff, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Spectral Rolloff')
    
def plot_zero_crossing_rate(no_frames, zero_crossing_rate):
    plt.figure()
    plt.plot(no_frames, zero_crossing_rate, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Zero Crossing Rate')
    
def plot_energy_entropy(no_frames, energy_entropy):
    plt.figure()
    plt.plot(no_frames, energy_entropy, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Energy Entropy')
    
def plot_energy(no_frames, energy):
    plt.figure()
    plt.plot(no_frames, energy, 'b')
    plt.xlabel('Frame Number'), plt.ylabel('Amplitude'), plt.title('Energy')
    
def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True sound')
    plt.xlabel('Predicted sound')
