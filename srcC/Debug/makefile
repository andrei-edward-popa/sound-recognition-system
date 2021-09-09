################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include utilities/subdir.mk
-include startup/subdir.mk
-include source_transfer/subdir.mk
-include source/subdir.mk
-include drivers/subdir.mk
-include device/subdir.mk
-include component/uart/subdir.mk
-include component/serial_manager/subdir.mk
-include component/lists/subdir.mk
-include component/i2c/subdir.mk
-include codec/subdir.mk
-include board/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: Audio_Signal_Feature_Extractor_Test.axf

# Tool invocations
Audio_Signal_Feature_Extractor_Test.axf: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: MCU Linker'
	arm-none-eabi-gcc -nostdlib -L"/usr/local/mcuxpressoide-11.1.1_3241/SDK_2.7.0_FRDM-K66F/CMSIS/DSP/Lib/GCC" -Xlinker -Map="Audio_Signal_Feature_Extractor_Test.map" -Xlinker --gc-sections -Xlinker -print-memory-usage -Xlinker --sort-section=alignment -Xlinker --cref -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -T Audio_Signal_Feature_Extractor_Test_Debug.ld -o "Audio_Signal_Feature_Extractor_Test.axf" $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '
	$(MAKE) --no-print-directory post-build

# Other Targets
clean:
	-$(RM) $(EXECUTABLES)$(OBJS)$(C_DEPS) Audio_Signal_Feature_Extractor_Test.axf
	-@echo ' '

post-build:
	-@echo 'Performing post-build steps'
	-arm-none-eabi-size "Audio_Signal_Feature_Extractor_Test.axf"; # arm-none-eabi-objcopy -v -O binary "Audio_Signal_Feature_Extractor_Test.axf" "Audio_Signal_Feature_Extractor_Test.bin" ; # checksum -p MK66FN2M0xxx18 -d "Audio_Signal_Feature_Extractor_Test.bin";
	-@echo ' '

.PHONY: all clean dependents post-build

-include ../makefile.targets
