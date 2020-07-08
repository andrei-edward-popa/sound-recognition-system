################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../component/uart/uart_adapter.c 

OBJS += \
./component/uart/uart_adapter.o 

C_DEPS += \
./component/uart/uart_adapter.d 


# Each subdirectory must supply rules for building sources it contributes
component/uart/%.o: ../component/uart/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -std=gnu99 -D__REDLIB__ -DDIG_MIC -DCPU_MK66FN2M0VMD18 -DCPU_MK66FN2M0VMD18_cm4 -DFRDM_K66F -DFREEDOM -DSDK_I2C_BASED_COMPONENT_USED=1 -DBOARD_USE_CODEC=1 -DCODEC_DA7212_ENABLE -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -DCR_INTEGER_PRINTF -DPRINTF_FLOAT_ENABLE=0 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/board" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/source" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/drivers" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/device" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/CMSIS" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/codec" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/component/i2c" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/utilities" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/component/serial_manager" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/component/lists" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_interrupt_record_playback/component/uart" -O0 -fno-common -g3 -Wall -Wextra -c  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin -fmerge-constants -fmacro-prefix-map="../$(@D)/"=. -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


