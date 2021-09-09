################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../codec/fsl_codec_adapter.c \
../codec/fsl_codec_common.c \
../codec/fsl_codec_i2c.c \
../codec/fsl_dialog7212.c 

OBJS += \
./codec/fsl_codec_adapter.o \
./codec/fsl_codec_common.o \
./codec/fsl_codec_i2c.o \
./codec/fsl_dialog7212.o 

C_DEPS += \
./codec/fsl_codec_adapter.d \
./codec/fsl_codec_common.d \
./codec/fsl_codec_i2c.d \
./codec/fsl_dialog7212.d 


# Each subdirectory must supply rules for building sources it contributes
codec/%.o: ../codec/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -std=gnu99 -D__REDLIB__ -DCPU_MK66FN2M0VMD18 -DCPU_MK66FN2M0VMD18_cm4 -DARM_MATH_CM4 -DPRINTF_FLOAT_ENABLE=1 -DFRDM_K66F -DFREEDOM -DSDK_I2C_BASED_COMPONENT_USED=1 -DBOARD_USE_CODEC=1 -DCODEC_DA7212_ENABLE -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/board" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/source" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/drivers" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/device" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/CMSIS" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/codec" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/component/i2c" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/fatfs/source" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/fatfs/source/fsl_ram_disk" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/fatfs/source/fsl_sd_disk" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/sdmmc/inc" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/utilities" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/component/serial_manager" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/component/lists" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/component/uart" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/sdmmc/port" -O1 -fno-common -g3 -Wall -c  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin -fmacro-prefix-map="../$(@D)/"=. -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


