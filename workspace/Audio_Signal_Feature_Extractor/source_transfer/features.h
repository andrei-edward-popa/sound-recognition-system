#ifndef FEATURES_H_
#define FEATURES_H_

#include <arm_math.h>
#include <stdlib.h>
#include "structures.h"

s32 leftmost_bit(u32);
q31_t div32_taylor(q31_t, q31_t, u16);
void compute_RealFastFourierTransformMagnitude_f32(arm_rfft_instance_f32*, float32_t*, u32, float32_t*, float32_t*);
void compute_SpectralCentroidSpread_f32(float32_t*, float32_t*, u32, float32_t*, float32_t*);
void compute_ZeroCrossingRate_f32(float32_t*, u32, float32_t*);
void compute_SpectralFlux_f32(float32_t*, float32_t*, u32, float32_t*);
void compute_SpectralRolloff_f32(float32_t*, float32_t, u32, float32_t*);
void compute_EnergyEntropy_f32(float32_t*, u32, u32, float32_t*);
void NormalizeSignal_f32(float32_t*, u32, float32_t*);
void compute_Energy_f32(float32_t*, u32, float32_t*);
void compute_FilterBank_f32(float32_t**, u32, u32, u32);
void compute_MFCC_f32(float32_t*, float32_t**, u32, u32, u32, float32_t*);
void compute_Pitch_f32(float32_t*, float32_t, u32, u32, float32_t*);
float32_t compute_sum_f32(float32_t*, u32);

#endif
