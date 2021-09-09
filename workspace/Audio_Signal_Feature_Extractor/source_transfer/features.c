#include "features.h"
#include <stdio.h>

extern const float32_t MFCC_Lifter[];

s32 leftmost_bit(u32 number)
{
	/**
	* @brief This function finds the index of the most left set bit of a positive integer
	* param[in] a positive integer
	* return the index of the most left set bit
	*/

	s32 i = 0;

	if (number == 0) {
		return -1;
	}
	if (number & 0xFFFF0000) {
		number &= 0xFFFF0000;
		i += 16;
	}
	if (number & 0xFF00FF00) {
		number &= 0xFF00FF00;
		i += 8;
	}
	if (number & 0xF0F0F0F0) {
		number &= 0xF0F0F0F0;
		i += 4;
	}
	if (number & 0xCCCCCCCC) {
		number &= 0xCCCCCCCC;
		i += 2;
	}
	if (number & 0xAAAAAAAA) {
		number &= 0xAAAAAAAA;
		i += 1;
	}
	return i;
}

q31_t div32_taylor(q31_t num, q31_t den, u16 nr_terms)
{
	  /**
	* @brief This function performes the division of 2 numbers using Taylor series
	* param[in] the numerator of the fraction
	* param[in] the denominator of the fraction
	* param[in] number of iterations
	* return the result of the division
	*/

	q31_t powers[nr_terms];
	memset(powers, 0, sizeof(q31_t));
	powers[0] = 0x7fffffff;
	q63_t result = 0;
	q31_t sh;
	register uint16_t i = 0;

	if(den < 0) {
		num = -num;
		den = -den;
	}

	if(num == 0) {
		result = 0;
	}
	else if(abs(num) > abs(den)) {
		if(num > 0 && den > 0) {
		  result = 0x7fffffff;
		} else {
		  result = 0x80000000;
		}
	} else {
		sh = leftmost_bit(den);
		den = den << (30 - sh);
		num = num << (30 - sh);

		den = 0x7fffffff - den;

		for(i = 1; i < nr_terms; i++) {
		  powers[i] = (q31_t)(((q63_t)powers[i - 1] * (q63_t)den) >> 31);
		}

		for(i = 0; i < nr_terms; i++) {
		  result  = result + (q63_t) powers[i];
		}

		result = ((result * (q63_t)num) >> 31);
	}
	return (q31_t) result;
}

void compute_RealFastFourierTransformMagnitude_f32(arm_rfft_instance_f32* rfft_instance, float32_t* input_signal, u32 fft_len, float32_t* magnitude, float32_t* power_spectrum) {
	arm_rfft_f32(rfft_instance, input_signal, magnitude);
	arm_cmplx_mag_squared_f32(magnitude, power_spectrum, fft_len);
	arm_cmplx_mag_f32(magnitude, magnitude, fft_len);
	for (u32 i = 0; i < fft_len; i++) {
		magnitude[i] /= fft_len;
		power_spectrum[i] /= fft_len;
	}
}

float32_t compute_Sum_f32(float32_t* input_signal, u32 len) {
	float32_t result = 0;
	for (u32 i = 0; i < len; i++) {
		result += input_signal[i];
	}
	return result;
}

void compute_SpectralCentroidSpread_f32(float32_t* frequencies, float32_t* magnitude, u32 len, float32_t* centroid, float32_t* spread) {
	float32_t fftSum = compute_Sum_f32(magnitude, len);
	float32_t freqTfft[len];
	arm_mult_f32(frequencies, magnitude, freqTfft, len);
	*centroid = 2 * compute_Sum_f32(freqTfft, len) / ((fftSum + DELTA) * SAMPLE_RATE);
	for (u32 i = 0; i < len; i++) {
		freqTfft[i] = powf(frequencies[i] - (*centroid), 2);
	}
	arm_mult_f32(freqTfft, magnitude, freqTfft, len);
	*spread = 2 * sqrtf(compute_Sum_f32(freqTfft, len) / fftSum) / SAMPLE_RATE;
}

void compute_ZeroCrossingRate_f32(float32_t* input_signal, u32 len, float32_t* zcr) {
	s32 sign_diff[len];
	s32 zeros = 0;
	sign_diff[0] = (input_signal[0] > 0.0f) - (input_signal[0] < 0.0f);
	for (u32 i = 1; i < len; i++) {
		sign_diff[i] = (input_signal[i] > 0.0f) - (input_signal[i] < 0.0f);
		sign_diff[i - 1] = abs(sign_diff[i] - sign_diff[i - 1]);
		zeros += sign_diff[i - 1];
	}
	*zcr = (float32_t) zeros / ((len - 1) << 1);
}

void compute_SpectralFlux_f32(float32_t* magnitude, float32_t* prev_magnitude, u32 len, float32_t* flux) {
	float32_t diff[len];
	arm_sub_f32(magnitude, prev_magnitude, diff, len);
	for (u32 i = 0; i < len; i++) {
		diff[i] = powf(diff[i], 2);
	}
	*flux = compute_Sum_f32(diff, len);
}

void compute_SpectralRolloff_f32(float32_t* magnitude, float32_t ratio, u32 len, float32_t* rolloff) {
	float32_t squared_FFT = powf(magnitude[0], 2);
	float32_t spectrumEnergy = squared_FFT;
	float32_t cumsum[len];
	cumsum[0] = squared_FFT;
	for (u32 i = 1; i < len; i++) {
		squared_FFT = powf(magnitude[i], 2);
		cumsum[i] = cumsum[i - 1] + squared_FFT;
		spectrumEnergy += squared_FFT;
	}
	float32_t threshold = spectrumEnergy * ratio;
	s32 index = -1;
	for (u32 i = 0; i < len; i++) {
		if (cumsum[i] > threshold) {
			index = i;
			break;
		}
	}
	if (index != -1) {
		*rolloff = (index << 1) / (float32_t) len;
	} else {
		*rolloff = 0.0f;
	}
}

void compute_EnergyEntropy_f32(float32_t* input_signal, u32 cut, u32 len, float32_t* entropy) {
	*entropy = 0;
	u32 subFramesLength = len / cut;
	float32_t subFrames[subFramesLength][cut];
	float32_t prob[cut];
	float32_t energyFrame = 0;
	for (u32 i = 0; i < len; i++) {
		subFrames[i % subFramesLength][i / subFramesLength] = powf(input_signal[i], 2);
	}
	for (u32 i = 0; i < cut; i++) {
		prob[i] = 0;
		for (u32 j = 0; j < subFramesLength; j++) {
			energyFrame += subFrames[j][i];
			prob[i] += subFrames[j][i];
		}
	}
	for (u32 i = 0; i < cut; i++) {
		prob[i] /= (energyFrame + DELTA);
		*entropy -= (prob[i] * log10f(prob[i] + DELTA) / LOG_10_2);
	}
}

void NormalizeSignal_f32(float32_t* input_signal, u32 len, float32_t* normalized_signal) {
	float32_t mean, rms, value;
	float32_t temp[len];
	arm_mean_f32(input_signal, len, &mean);
	for (u32 i = 0; i < len; i++) {
		temp[i] = powf(input_signal[i], 2);
	}
	rms = sqrtf(compute_Sum_f32(temp, len) / len);
	for (u32 i = 0; i < len; i++) {
		normalized_signal[i] = (input_signal[i] - mean) / (rms + DELTA);
	}
}

void compute_Energy_f32(float32_t* input_signal, u32 len, float32_t* energy) {
	*energy = 0;
	for (u32 i = 0; i < len; i++) {
		*energy += powf(input_signal[i], 2);
	}
	*energy /= len;
}

void compute_FilterBank_f32(float32_t** fbank, u32 fft_len, u32 sample_rate, u32 n_filt) {
	float32_t low_freq_mel = 0.0f;
	float32_t high_freq_mel = 2595 * log10f(1.0f + (sample_rate / 2) / (float32_t)700);
	float32_t freq_mel_points[n_filt + 2], freq_hz_points[n_filt + 2];
	u32 bins[n_filt + 2];
	float32_t step = (high_freq_mel - low_freq_mel) / (n_filt + 1);
	for (u32 i = 0; i < n_filt + 2; i++) {
		freq_mel_points[i] = low_freq_mel + i * step;
		freq_hz_points[i] = 700 * (powf(10, freq_mel_points[i] / 2595) - 1);
		bins[i] = (u32)(fft_len * freq_hz_points[i] / sample_rate);
	}
	u32 f_left, f_current, f_right;
	for (u32 i = 1; i < n_filt + 1; i++) {
		f_left = bins[i - 1];
		f_current = bins[i];
		f_right = bins[i + 1];
		for (u32 j = f_left; j < f_current; j++) {
			fbank[i - 1][j] = (float32_t)(j - bins[i - 1]) / (bins[i] - bins[i - 1]);
		}
		for (u32 j = f_current; j < f_right; j++) {
			fbank[i - 1][j] = (float32_t)(bins[i + 1] - j) / (bins[i + 1] - bins[i]);
		}
	}
	for (u32 i = 0; i < n_filt; i++) {
		float32_t temp = 2.0f / (freq_hz_points[i + 2] - freq_hz_points[i]);
		for (u32 j = 0; j < fft_len / 2; j++) {
			fbank[i][j] *= temp;
		}
	}
}

void compute_MFCC_f32(float32_t* power_spectrum, float32_t** fbank, u32 fft_len, u32 n_filt, u32 n_ceps, float32_t* mfcc) {
	float32_t pre_mfcc[n_filt];
	for (u32 i = 0; i < n_filt; i++) {
		arm_dot_prod_f32(power_spectrum, fbank[i], fft_len, &pre_mfcc[i]);
	}
	for (u32 i = 0; i < n_filt; i++) {
		pre_mfcc[i] = 10 * log10f(pre_mfcc[i] + DELTA);
	}
	for (u32 i = 1; i <= n_ceps; i++) {
		float32_t sum = 0;
		for (u32 j = 0; j < n_filt; j++) {
			sum += pre_mfcc[j] * arm_cos_f32(PI * i * (2 * j + 1) / (2 * n_filt));
		}
		mfcc[i - 1] = sum * MFCC_CONSTANT2 * MFCC_Lifter[i - 1];
	}
}

void compute_Pitch_f32(float32_t* frame, float32_t expected_period, u32 sample_rate, u32 len, float32_t* pitch) {
	s32 M = (u32)(expected_period * sample_rate);
	float32_t autocorr[2 * len - 1];
	float32_t hr;
	float32_t cumsum[len];
	float32_t g;
	s32 M0 = -1;
	arm_correlate_f32(frame, len, frame, len, autocorr);
	cumsum[0] = powf(frame[0], 2);
	for (u32 i = 1; i < len; i++) {
		cumsum[i] = cumsum[i - 1] + powf(frame[i], 2);
	}
	g = autocorr[len - 1];
	for (u32 i = 0; i < len - 2; i++) {
		autocorr[i] = autocorr[len + i];
	}
	s32 sign_diff[len - 2];
	sign_diff[0] = (autocorr[0] > 0.0f) - (autocorr[0] < 0.0f);
	for (u32 i = 1; i < len - 2; i++) {
		sign_diff[i] = (autocorr[i] > 0.0f) - (autocorr[i] < 0.0f);
		sign_diff[i - 1] = sign_diff[i] - sign_diff[i - 1];
	}
	for (u32 i = 0; i < len - 3; i++) {
		if (sign_diff[i] != 0) {
			M0 = i;
			break;
		}
	}
	if (M0 == -1) {
		M0 = len - 3;
	}
	if (M > (s32)(len - 2)) {
		M = len - 3;
	}
	float32_t gamm[M];
	for (s32 i = 0; i < M; i++) {
		gamm[i] = 0;
	}
	if (M == 0) {
		*pitch = 0.0f;
	} else {
		for (s32 i = M0; i < M; i++) {
			gamm[i] = autocorr[i] / (sqrtf(g * cumsum[M + M0 - i]) + DELTA);
		}
		float32_t zcr;
		compute_ZeroCrossingRate_f32(gamm, M, &zcr);
		if (zcr > 0.5f) {
			*pitch = 0;
		} else {
			u32 pitch_index;
			arm_max_f32(gamm, M, &hr, &pitch_index);
			*pitch = (float32_t) sample_rate / (pitch_index + DELTA);
			if (*pitch > (float32_t) sample_rate / 2) {
				*pitch = 0;
			}
		}
	}
}
