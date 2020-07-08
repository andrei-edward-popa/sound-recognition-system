import numpy as np
from scipy.fftpack import fft, dct
from scipy.io import wavfile as wf

class FeatureExtractor:
    """
    A class used to extract MPEG7 low level descriptors.
    When initialize an object, all features will be extracted.
    Features available are: Spectral Centroid (SC), Spread Spread (SS), Zero Crossing Rate (ZCR), Spectral Flux (SF), Spectral Rolloff (SR), Harmonic Ratio (HR), Pitch (P), Energy (E), Energy Entropy (EE)
    
    Attributes
    ----------
    
    m_audioSignal : numpy-array
        A 1D numpy array containing the input samples of audio signal. 
    m_sampleRate : int > 0
        The sample rate of the audio signal (in samples/sec).
    m_signalLength : int > 0
        The number of samples of audio signal.
    m_timeHopSize : float > 0
        Time interval between two successive time frames (in seconds).
    m_hopSize : int > 0
        The integer number of time samples corresponding to m_timeHopSize.
    m_timeFrameLength : float > 0
        Length of a time frame (in seconds).
    m_frameLength : int > 0
        The integer number of time samples corresponding to m_timeFrameLength.
    m_noFrames : int > 0
        Total number of time frames in audio signal.
    m_fftPoints : int > 0
         Total number of FFT coefficients to compute.
    m_frames : numpy-array (shape : m_noFrames x m_frameLength)
        A 2D numpy array containing all frames.
    m_FFT : numpy-array (shape : m_noFrames x m_fftPoints)
        A 2D numpy array containing FFT coefficients of all frames.
    m_spectralCentroid : numpy-array
        A 1D numpy array containing Spectral Centroid (SC) values for all frames.
    m_spectralSpread : numpy-array
        A 1D numpy array containing Spectral Spread (SS) values for all frames.
    m_ZCR : numpy-array : numpy-array
        A 1D numpy array containing Zero Crossing Rate (ZCR) values for all frames.
    m_spectralFlux : numpy-array
        A 1D numpy array containing Spectral Flux (SF) values for all frames.
    m_spectralRolloff : numpy-array
        A 1D numpy array containing Spectral Rolloff (SR) values for all frames.
    m_harmonicRatio : numpy-array
        A 1D numpy array containing Harmonic Ratio (HR) values for all frames.
    m_pitch : numpy-array
        A 1D numpy array containing Pitch (P) values for all frames.
    m_energy : numpy-array
        A 1D numpy array containing Energy (E) values for all frames.
    m_energyEntropy : numpy-array
        A 1D numpy array containing Energy Entropy (EE) values for all frames.
    m_delta : float, constant - 0.0000000001 
        A constant defined in order to avoid 0 division.
    
    Methods
    -------
    
    normalize_signal()
        Normalize the input audio signal.
    computeFrames()
        Divide the audio signal into individual frames.
    computeFFT()
        Compute Fast Fourier Transform (FFT) for all individual frames.
    computeSpectralCentroidAndSpread()
        Compute Spectral Centroid (SC) and Spectral Spread (SS) for all individual frames.
    computeZCR()
        Compute Zero Crossing Rate (ZCR) for all individual frames.
    computeSpectralFlux()
        Compute Spectral Flux (SF) for all individual frames.
    computeSpectralRolloff(ratio=0.5)
        Compute Spectral Rolloff (SR) for all individual frames.
    computeHarmonicRatioAndPitch(expectedPeriod=0.04)
        Compute Harmonic Ratio (HR) and Pitch (P) for all individual frames.
    computeEnergy()
        Compute Energy (E) for all individual frames.
    computeEnergyEntropy(cut=20)
        Compute Energy Entropy (EE) for all individual frames.
    ZCR() : @staticmethod
        A static method for compute Zero Crossing Rate (ZCR) for a given array.
    """
    
    def __init__(self, audioSignalFileName, fbank=None, timeHopSize=0.03, timeFrameLength=0.03, fftPoints=512, normalized=False, computeLLD=False):
        """
        Parameters
        ----------
        
        audioSignalFileName : str
            The name of the audio signal file (it need to specify the whole path).
        timeHopSize : float > 0, optional (default : 0.01)
            Time interval between two successive time frames (in seconds).
        timeFrameLength : float > 0, optional (default : 0.03)
            Length of a time frame (in seconds).
        fftPoints : int > 0, optional (default : 1024)
            Total number of FFT coefficients to compute.
        normalized : boolean, optional (default : False)
            If normalized is set to False, the samples of the audio signal will be divided by 2**15.
        computeLLD : boolean, optional (default : False)
            If computeLLD is set to False, features won't be computed.
        """
        
        self.m_sampleRate, self.m_audioSignal = wf.read(audioSignalFileName)
        self.m_audioSignal = np.array(self.m_audioSignal)
        if normalized == False:
            self.m_audioSignal /= 2**15
        self.m_signalLength = len(self.m_audioSignal)
        self.m_timeHopSize = timeHopSize
        self.m_hopSize = int(self.m_sampleRate * self.m_timeHopSize)
        self.m_timeFrameLength = timeFrameLength
        self.m_frameLength = int(self.m_sampleRate * self.m_timeFrameLength)
        self.m_noFrames = int((self.m_signalLength - self.m_frameLength) / self.m_hopSize + 1)
        self.m_fftPoints = fftPoints
        self.m_frames = np.array([])
        self.m_FFT = np.array([])
        self.m_powerSpectrum = np.array([])
        self.m_spectralCentroid = np.array([])
        self.m_spectralSpread = np.array([])
        self.m_ZCR = np.array([])
        self.m_spectralFlux = np.array([])
        self.m_spectralRolloff = np.array([])
        self.m_harmonicRatio = np.array([])
        self.m_pitch = np.array([])
        self.m_energy = np.array([])
        self.m_energyEntropy = np.array([])
        self.m_MFCC = np.array([])
        self.m_DMFCC = np.array([])
        self.m_DDMFCC = np.array([])
        self.m_fbank = fbank
        self.m_delta = 0.0000000001
        self.computeFrames()
        self.computeFFT()
        self.computePowerSpectrum()
        if computeLLD == True:
            self.computeHarmonicRatioAndPitch()
            self.computeSpectralCentroidAndSpread()
            self.computeSpectralFlux()
            self.computeEnergyEntropy()
            self.computeZCR()
            if fbank != None:
                self.computeMFCC()
                
    @staticmethod    
    def normalize_signal(signal):
        """
        Normalize an audio signal.
        Bring the audio signal to 0 mean and divide all samples by the rms value of the audio signal. 
        The results are written back in m_audioSignal.
        
        Parameters
        ----------
        
        signal : numpy-array
            A 1D array with integer or fractional values.
            
        Returns
        -------
        
        norm_signal : numpy-array
            Resulted 1D array after normalizing process.
        """

        signal_mean = signal.mean()
        signal_rms = np.sqrt(np.mean(signal ** 2))
        norm_signal = (signal - signal_mean) / signal_rms
        return norm_signal
        
    def computeFrames(self):
        """
        Divide the audio signal into individual frames.
        The results are written in m_frames.
        
        Parameters
        ----------
        
        None
        """
        window = np.hamming(self.m_frameLength)
        frame = FeatureExtractor.normalize_signal(self.m_audioSignal[0:self.m_frameLength])
        self.m_frames = np.hstack((self.m_frames, window * frame))
        currentFrame = 1
        while currentFrame < self.m_noFrames:
            frame = FeatureExtractor.normalize_signal(self.m_audioSignal[currentFrame * self.m_hopSize:currentFrame * self.m_hopSize + self.m_frameLength])
            self.m_frames = np.vstack((self.m_frames, window * frame))
            currentFrame += 1
                   
    def computeFFT(self):
        """
        Compute Fast Fourier Transform (FFT) for all individual frames.
        The results are written in m_FFT.
        
        Parameters
        ----------
        
        None
        """
        
        halfFFT = int(self.m_fftPoints / 2)
        FFT = np.abs(fft(self.m_frames[0], n=self.m_fftPoints))
        FFT = FFT[0:halfFFT]
        FFT = FFT / self.m_fftPoints
        self.m_FFT = np.hstack((self.m_FFT, FFT))
        currentFrame = 1
        while currentFrame < self.m_noFrames:
            FFT = np.abs(fft(self.m_frames[currentFrame], n=self.m_fftPoints))
            FFT = FFT[0:halfFFT]
            FFT = FFT / self.m_fftPoints
            self.m_FFT = np.vstack((self.m_FFT, FFT))
            currentFrame += 1
            
    def computePowerSpectrum(self):
        halfFFT = int(self.m_fftPoints / 2)
        powerSpectrum = ((self.m_FFT[0] * halfFFT) ** 2) / halfFFT
        self.m_powerSpectrum = np.hstack((self.m_powerSpectrum, powerSpectrum))
        currentFrame = 1
        while currentFrame < self.m_noFrames:
            powerSpectrum = ((self.m_FFT[currentFrame] * halfFFT) ** 2) / halfFFT
            self.m_powerSpectrum = np.vstack((self.m_powerSpectrum, powerSpectrum))
            currentFrame += 1
                      
    def computeSpectralCentroidAndSpread(self):
        """
        Compute Spectral Centroid (SC) and Spectral Spread (SS) for all individual frames.
        The results are written in m_spectralCentroid and m_spectralSpread.
        
        Parameters
        ----------
        
        None
        """
        
        halfFFT = int(self.m_fftPoints / 2)
        frequencies = np.array(range(1, halfFFT + 1)) * self.m_sampleRate / self.m_fftPoints
        currentFrame = 0
        while currentFrame < self.m_noFrames:
            fftSum = (np.sum(self.m_FFT[currentFrame]) + self.m_delta)
            spectralCentroid = np.sum(frequencies * self.m_FFT[currentFrame]) / (fftSum + self.m_delta)
            spectralCentroid = 2 * spectralCentroid / self.m_sampleRate
            spectralSpread = np.sqrt(np.sum(((frequencies - spectralCentroid) ** 2) * self.m_FFT[currentFrame]) / fftSum)
            spectralSpread = 2 * spectralSpread / self.m_sampleRate
            self.m_spectralCentroid = np.append(self.m_spectralCentroid, spectralCentroid)
            self.m_spectralSpread = np.append(self.m_spectralSpread, spectralSpread)
            currentFrame += 1

    def computeZCR(self):
        """
        Compute Zero Crossing Rate (ZCR) for all individual frames.
        The results are written in m_ZCR.
        
        Parameters
        ----------
        
        None
        """
        
        currentFrame = 0
        while currentFrame < self.m_noFrames:
            zeros = np.sum(np.abs(np.diff(np.sign(self.m_frames[currentFrame])))) / 2
            ZCR = zeros / (self.m_frameLength - 1)
            self.m_ZCR = np.append(self.m_ZCR, ZCR)
            currentFrame += 1
                      
    def computeSpectralFlux(self):
        """
        Compute Spectral Flux (SF) for all individual frames.
        The results are written in m_spectralFlux.
        
        Parameters
        ----------
        
        None
        """
        
        currentFrame = 1
        while currentFrame < self.m_noFrames:
            spectralFlux = np.sum((self.m_FFT[currentFrame] - self.m_FFT[currentFrame - 1]) ** 2)
            self.m_spectralFlux = np.append(self.m_spectralFlux, spectralFlux)
            currentFrame += 1
                
    def computeSpectralRolloff(self, ratio=0.85):
        """
        Compute Spectral Rolloff (SR) for all individual frames.
        The results are written in m_spectralRolloff.
        
        Parameters
        ----------
        
        ratio : float > 0, optional (default : 0.85)
            A value used to find where 'ratio' accumulated magnitude of the spectrum is concentrated (between 0 and 1).
        """
        
        currentFrame = 0
        while currentFrame < self.m_noFrames:
            spectrumEnergy = np.sum(self.m_FFT[currentFrame] ** 2)
            threshold = ratio * spectrumEnergy
            cumsum = np.cumsum(self.m_FFT[currentFrame] ** 2)
            check = np.nonzero(cumsum > threshold)[0]
            if len(check) > 0:
                spectralRolloff = 2 * check[0] / self.m_fftPoints
            else:
                spectralRolloff = 0.0
            self.m_spectralRolloff = np.append(self.m_spectralRolloff, spectralRolloff)
            currentFrame += 1
                
    def computeHarmonicRatioAndPitch(self, expectedPeriod=0.04):
        """
        Compute Harmonic Ratio (HR) and Pitch (P) for all individual frames.
        The results are written in m_harmonicRatio and m_pitch.
        
        Parameters
        ----------
        
        expectedPeriod : float > 0, optional (default : 0.04)
            The maximum fundamental period (in seconds).
        """
        
        M = np.round(expectedPeriod * self.m_sampleRate) - 1
        currentFrame = 0
        while currentFrame < self.m_noFrames:
            frame = self.m_frames[currentFrame]
            autocorr = np.correlate(frame, frame, mode='full')
            gain = autocorr[len(frame) - 1]
            autocorr = autocorr[len(frame):-1]
            [nonZeros, ] = np.nonzero(np.diff(np.sign(autocorr)))
            if len(nonZeros) == 0:
                M0 = len(autocorr) - 1
            else:
                M0 = nonZeros[0]
            if M > len(autocorr):
                M = len(autocorr) - 1
            gamma = np.zeros(M)
            cumulative_sum = np.cumsum(frame ** 2)
            gamma[M0:M] = autocorr[M0:M] / (np.sqrt((cumulative_sum[M:M0:-1] * gain)) + self.m_delta)
            zcr = FeatureExtractor.ZCR(gamma)
            if zcr > 0.5:
                self.m_harmonicRatio = np.append(self.m_harmonicRatio, 0)
                self.m_pitch = np.append(self.m_pitch, 0)
            else:
                if len(gamma) == 0:
                    harmonicRatio = 1
                    pitchIndex = 0
                else:
                    harmonicRatio = np.max(gamma)
                    pitchIndex = np.argmax(gamma)
                pitch = self.m_sampleRate / (pitchIndex + self.m_delta)
                if pitch >= self.m_sampleRate / 2:
                    pitch = 0
                self.m_harmonicRatio = np.append(self.m_harmonicRatio, harmonicRatio)
                self.m_pitch = np.append(self.m_pitch, pitch)
            currentFrame += 1
            
    def computeEnergy(self):
        """
        Compute Energy (E) for all individual frames.
        The results are written in m_energy.
        
        Parameters
        ----------
        
        None
        """
        
        currentFrame = 0
        while currentFrame < self.m_noFrames:
            self.m_energy = np.append(self.m_energy, np.sum(self.m_frames[currentFrame] ** 2) / self.m_frameLength)
            currentFrame += 1

    def computeEnergyEntropy(self, cut=20):
        """
        Compute Energy Entropy (EE) for all individual frames.
        The results are written in m_energyEntropy.
        
        Parameters
        ----------
        
        cut : int > 0, optional (default : 20)
            Divide an audio signal frame into 'cut' subframes, in order to compute Energy Entropy (EE) on subframes.
        """
        
        currentFrame = 0
        while currentFrame < self.m_noFrames:
            energyFrame = np.sum(self.m_frames[currentFrame] ** 2)
            subFramesLength = int(self.m_frameLength / cut)
            subFrames = self.m_frames[currentFrame].reshape(subFramesLength, cut, order='F').copy()
            prob = np.sum(subFrames ** 2, axis=0) / (energyFrame + self.m_delta)
            entropyFrame = -np.sum(prob * np.log2(prob + self.m_delta))
            self.m_energyEntropy = np.append(self.m_energyEntropy, entropyFrame)
            currentFrame += 1
            
    def computeMFCC(self, n_ceps=13, cep_lifter=22):
        filter_banks = np.dot(self.m_powerSpectrum, self.m_fbank.T) + self.m_delta
        filter_banks = 10 * np.log10(filter_banks)
        self.m_MFCC = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1:(n_ceps + 1)]
        n = np.arange(n_ceps)
        lift = 1 + (cep_lifter / 2) * np.sin(np.pi * n / cep_lifter)
        self.m_MFCC *= lift
        
    def computeDMFCC(self, n_ceps=13):
        FDC1 = np.array([1/280, -4/105, 1/5, -4/5, 0, 4/5, -1/5, 4/105, -1/280])
        for i in range(len(self.m_MFCC)):
            for j in range(n_ceps):
                first_deriv = 0
                for k in range(-4,5):
                    if j + k >= 0 and j + k < n_ceps:
                        first_deriv += FDC1[k + 4] * self.m_MFCC[i][j + k]
                self.m_DMFCC = np.append(self.m_DMFCC, first_deriv)
        self.m_DMFCC = self.m_DMFCC.reshape(len(self.m_MFCC), n_ceps)
        
    def computeDDMFCC(self, n_ceps=13):
        FDC2 = np.array([-1/560, 8/315, -1/5, 8/5, -205/72, 8/5, -1/5, 8/315, -1/560])
        for i in range(len(self.m_MFCC)):
            for j in range(n_ceps):
                second_deriv = 0
                for k in range(-4,5):
                    if j + k >= 0 and j + k < n_ceps:
                        second_deriv += FDC2[k + 4] * self.m_MFCC[i][j + k]
                self.m_DDMFCC = np.append(self.m_DDMFCC, second_deriv)
        self.m_DDMFCC = self.m_DDMFCC.reshape(len(self.m_MFCC), n_ceps)
                
    @staticmethod        
    def ZCR(arr):
        """
        A static method for compute Zero Crossing Rate (ZCR) for a given array.
        
        Parameters
        ----------
        
        arr : numpy-array
            A 1D numpy array with integer or fractional values.
            
        Returns
        -------
        
        ZCR : float
            The value of zero crossing rate (between 0 and 1).
        """
        
        zeros = np.sum(np.abs(np.diff(np.sign(arr)))) / 2
        ZCR = zeros / (len(arr) - 1)
        return ZCR
            