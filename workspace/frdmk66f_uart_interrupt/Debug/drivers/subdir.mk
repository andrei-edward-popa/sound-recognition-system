################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../drivers/fsl_clock.c \
../drivers/fsl_common.c \
../drivers/fsl_ftfx_cache.c \
../drivers/fsl_ftfx_controller.c \
../drivers/fsl_ftfx_flash.c \
../drivers/fsl_ftfx_flexnvm.c \
../drivers/fsl_gpio.c \
../drivers/fsl_lpuart.c \
../drivers/fsl_smc.c \
../drivers/fsl_uart.c 

OBJS += \
./drivers/fsl_clock.o \
./drivers/fsl_common.o \
./drivers/fsl_ftfx_cache.o \
./drivers/fsl_ftfx_controller.o \
./drivers/fsl_ftfx_flash.o \
./drivers/fsl_ftfx_flexnvm.o \
./drivers/fsl_gpio.o \
./drivers/fsl_lpuart.o \
./drivers/fsl_smc.o \
./drivers/fsl_uart.o 

C_DEPS += \
./drivers/fsl_clock.d \
./drivers/fsl_common.d \
./drivers/fsl_ftfx_cache.d \
./drivers/fsl_ftfx_controller.d \
./drivers/fsl_ftfx_flash.d \
./drivers/fsl_ftfx_flexnvm.d \
./drivers/fsl_gpio.d \
./drivers/fsl_lpuart.d \
./drivers/fsl_smc.d \
./drivers/fsl_uart.d 


# Each subdirectory must supply rules for building sources it contributes
drivers/%.o: ../drivers/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -std=gnu99 -D__REDLIB__ -DCPU_MK66FN2M0VMD18 -DCPU_MK66FN2M0VMD18_cm4 -DFRDM_K66F -DFREEDOM -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -DCR_INTEGER_PRINTF -DPRINTF_FLOAT_ENABLE=0 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt/board" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt/source" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt/drivers" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt/device" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt/CMSIS" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt/utilities" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt/component/serial_manager" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt/component/lists" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_uart_interrupt/component/uart" -O0 -fno-common -g3 -Wall -c  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin -fmerge-constants -fmacro-prefix-map="../$(@D)/"=. -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


