################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../device/system_MK66F18.c 

OBJS += \
./device/system_MK66F18.o 

C_DEPS += \
./device/system_MK66F18.d 


# Each subdirectory must supply rules for building sources it contributes
device/%.o: ../device/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -std=gnu99 -DARM_MATH_CM4=1 -DDIG_MIC -DCPU_MK66FN2M0VMD18 -DCPU_MK66FN2M0VMD18_cm4 -DFRDM_K66F -DFREEDOM -DSDK_I2C_BASED_COMPONENT_USED=1 -DBOARD_USE_CODEC=1 -DCODEC_DA7212_ENABLE -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -DPRINTF_FLOAT_ENABLE=1 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -D__REDLIB__ -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/board" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/source" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/drivers" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/device" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/CMSIS" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/codec" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/component/i2c" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/utilities" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/component/serial_manager" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/component/lists" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/Audio_Signal_Feature_Extractor/component/uart" -O0 -fno-common -g3 -Wextra -c  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin -fmerge-constants -fmacro-prefix-map="../$(@D)/"=. -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


