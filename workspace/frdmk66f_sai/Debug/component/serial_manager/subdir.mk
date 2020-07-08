################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../component/serial_manager/serial_manager.c \
../component/serial_manager/serial_port_uart.c 

OBJS += \
./component/serial_manager/serial_manager.o \
./component/serial_manager/serial_port_uart.o 

C_DEPS += \
./component/serial_manager/serial_manager.d \
./component/serial_manager/serial_port_uart.d 


# Each subdirectory must supply rules for building sources it contributes
component/serial_manager/%.o: ../component/serial_manager/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -std=gnu99 -D__REDLIB__ -DCPU_MK66FN2M0VMD18 -DCPU_MK66FN2M0VMD18_cm4 -DARM_MATH_CM4 -DPRINTF_FLOAT_ENABLE=1 -DFRDM_K66F -DFREEDOM -DSDK_I2C_BASED_COMPONENT_USED=1 -DBOARD_USE_CODEC=1 -DCODEC_DA7212_ENABLE -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/board" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/source" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/drivers" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/device" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/CMSIS" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/codec" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/component/i2c" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/fatfs/source" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/fatfs/source/fsl_ram_disk" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/fatfs/source/fsl_sd_disk" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/sdmmc/inc" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/utilities" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/component/serial_manager" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/component/lists" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/component/uart" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai/sdmmc/port" -O1 -fno-common -g3 -Wall -c  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin -fmacro-prefix-map="../$(@D)/"=. -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


