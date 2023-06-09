################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../drivers/fsl_clock.c \
../drivers/fsl_common.c \
../drivers/fsl_dmamux.c \
../drivers/fsl_edma.c \
../drivers/fsl_ftfx_cache.c \
../drivers/fsl_ftfx_controller.c \
../drivers/fsl_ftfx_flash.c \
../drivers/fsl_ftfx_flexnvm.c \
../drivers/fsl_gpio.c \
../drivers/fsl_i2c.c \
../drivers/fsl_lpuart.c \
../drivers/fsl_sai.c \
../drivers/fsl_sai_edma.c \
../drivers/fsl_sdhc.c \
../drivers/fsl_smc.c \
../drivers/fsl_sysmpu.c \
../drivers/fsl_uart.c 

OBJS += \
./drivers/fsl_clock.o \
./drivers/fsl_common.o \
./drivers/fsl_dmamux.o \
./drivers/fsl_edma.o \
./drivers/fsl_ftfx_cache.o \
./drivers/fsl_ftfx_controller.o \
./drivers/fsl_ftfx_flash.o \
./drivers/fsl_ftfx_flexnvm.o \
./drivers/fsl_gpio.o \
./drivers/fsl_i2c.o \
./drivers/fsl_lpuart.o \
./drivers/fsl_sai.o \
./drivers/fsl_sai_edma.o \
./drivers/fsl_sdhc.o \
./drivers/fsl_smc.o \
./drivers/fsl_sysmpu.o \
./drivers/fsl_uart.o 

C_DEPS += \
./drivers/fsl_clock.d \
./drivers/fsl_common.d \
./drivers/fsl_dmamux.d \
./drivers/fsl_edma.d \
./drivers/fsl_ftfx_cache.d \
./drivers/fsl_ftfx_controller.d \
./drivers/fsl_ftfx_flash.d \
./drivers/fsl_ftfx_flexnvm.d \
./drivers/fsl_gpio.d \
./drivers/fsl_i2c.d \
./drivers/fsl_lpuart.d \
./drivers/fsl_sai.d \
./drivers/fsl_sai_edma.d \
./drivers/fsl_sdhc.d \
./drivers/fsl_smc.d \
./drivers/fsl_sysmpu.d \
./drivers/fsl_uart.d 


# Each subdirectory must supply rules for building sources it contributes
drivers/%.o: ../drivers/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -std=gnu99 -D__REDLIB__ -DCPU_MK66FN2M0VMD18 -DCPU_MK66FN2M0VMD18_cm4 -DARM_MATH_CM4 -DPRINTF_FLOAT_ENABLE=1 -DFRDM_K66F -DFREEDOM -DSDK_I2C_BASED_COMPONENT_USED=1 -DBOARD_USE_CODEC=1 -DCODEC_DA7212_ENABLE -DSERIAL_PORT_TYPE_UART=1 -DSDK_DEBUGCONSOLE=0 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/board" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/source" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/drivers" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/device" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/CMSIS" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/codec" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/component/i2c" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/fatfs/source" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/fatfs/source/fsl_ram_disk" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/fatfs/source/fsl_sd_disk" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/sdmmc/inc" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/utilities" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/component/serial_manager" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/component/lists" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/component/uart" -I"/home/apopa/Documents/MCUXpresso_11.1.1_3241/workspace/frdmk66f_sai_peripheral/sdmmc/port" -O1 -fno-common -g3 -Wall -c  -ffunction-sections  -fdata-sections  -ffreestanding  -fno-builtin -fmacro-prefix-map="../$(@D)/"=. -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


