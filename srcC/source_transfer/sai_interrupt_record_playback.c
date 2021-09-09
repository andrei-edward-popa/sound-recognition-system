#include "board.h"
#include "fsl_uart.h"

#include <arm_math.h>

#include "pin_mux.h"
#include "clock_config.h"

#include "fsl_debug_console.h"
#include "fsl_sai.h"
#include "fsl_codec_common.h"

#include "fsl_dialog7212.h"
#include "fsl_gpio.h"
#include "fsl_port.h"
#include "fsl_codec_adapter.h"

#include "features.h"
#include "look_up_tables.h"

#define DEMO_UART UART0
#define DEMO_UART_CLKSRC SYS_CLK
#define DEMO_UART_CLK_FREQ CLOCK_GetFreq(SYS_CLK)
#define DEMO_UART_IRQn UART0_RX_TX_IRQn
#define DEMO_UART_IRQHandler UART0_RX_TX_IRQHandler

#define DEMO_CODEC_DA7212
#define DEMO_SAI I2S0
#define DEMO_I2C I2C1
#define DEMO_SAI_CLKSRC kCLOCK_CoreSysClk
#define DEMO_SAI_CLK_FREQ CLOCK_GetFreq(kCLOCK_CoreSysClk)
#define DEMO_I2C_CLKSRC kCLOCK_BusClk
#define DEMO_I2C_CLK_FREQ CLOCK_GetFreq(kCLOCK_BusClk)

#define I2C_RELEASE_SDA_PORT PORTC
#define I2C_RELEASE_SCL_PORT PORTC
#define I2C_RELEASE_SDA_GPIO GPIOC
#define I2C_RELEASE_SDA_PIN 11U
#define I2C_RELEASE_SCL_GPIO GPIOC
#define I2C_RELEASE_SCL_PIN 10U
#define I2C_RELEASE_BUS_COUNT 100U
#define OVER_SAMPLE_RATE (384U)
#define BUFFER_SIZE (1920U)
#define BUFFER_NUMBER (4U)

#define DEMO_AUDIO_SAMPLE_RATE (kSAI_SampleRate16KHz)

#if (defined FSL_FEATURE_SAI_HAS_MCLKDIV_REGISTER && FSL_FEATURE_SAI_HAS_MCLKDIV_REGISTER) || \
    (defined FSL_FEATURE_PCC_HAS_SAI_DIVIDER && FSL_FEATURE_PCC_HAS_SAI_DIVIDER)
#define DEMO_AUDIO_MASTER_CLOCK OVER_SAMPLE_RATE *DEMO_AUDIO_SAMPLE_RATE
#else
#define DEMO_AUDIO_MASTER_CLOCK DEMO_SAI_CLK_FREQ
#endif

#define DEMO_AUDIO_DATA_CHANNEL (2U)

#define DEMO_AUDIO_BIT_WIDTH kSAI_WordWidth16bits

#ifndef DEMO_SAI_TX_SYNC_MODE
#define DEMO_SAI_TX_SYNC_MODE kSAI_ModeAsync
#endif
#ifndef DEMO_SAI_RX_SYNC_MODE
#define DEMO_SAI_RX_SYNC_MODE kSAI_ModeSync
#endif

void BOARD_I2C_ReleaseBus(void);

da7212_config_t da7212Config = {
    .i2cConfig    = {.codecI2CInstance = BOARD_CODEC_I2C_INSTANCE, .codecI2CSourceClock = 60000000},
    .dacSource    = kDA7212_DACSourceInputStream,
    .slaveAddress = DA7212_ADDRESS,
    .protocol     = kDA7212_BusI2S,
    .format       = {.mclk_HZ = 6144000U, .sampleRate = 16000, .bitWidth = 16},
    .isMaster     = false,
};

AT_NONCACHEABLE_SECTION_ALIGN(static uint8_t Buffer[BUFFER_NUMBER * BUFFER_SIZE], 4);

volatile uint32_t emptyBlock = BUFFER_NUMBER;

#if (defined(FSL_FEATURE_SAI_HAS_MCR) && (FSL_FEATURE_SAI_HAS_MCR)) || \
    (defined(FSL_FEATURE_SAI_HAS_MCLKDIV_REGISTER) && (FSL_FEATURE_SAI_HAS_MCLKDIV_REGISTER))
sai_master_clock_t mclkConfig = {
#if defined(FSL_FEATURE_SAI_HAS_MCR) && (FSL_FEATURE_SAI_HAS_MCR)
    .mclkOutputEnable = true,
#if !(defined(FSL_FEATURE_SAI_HAS_NO_MCR_MICS) && (FSL_FEATURE_SAI_HAS_NO_MCR_MICS))
    .mclkSource = kSAI_MclkSourceSysclk,
#endif
#endif
};
#endif

codec_config_t boardCodecConfig = {.codecDevType = kCODEC_DA7212, .codecDevConfig = &da7212Config};

sai_handle_t txHandle = {0}, rxHandle = {0};

codec_handle_t codecHandle;

static uint32_t tx_index = 0U, rx_index = 0U;

static void rx_callback(I2S_Type *base, sai_handle_t *handle, status_t status, void *userData) {
    if (kStatus_SAI_RxError == status) {
        /* Handle the error. */
    }
    else {
        emptyBlock--;
    }
}

static void tx_callback(I2S_Type *base, sai_handle_t *handle, status_t status, void *userData) {
    if (kStatus_SAI_TxError == status) {
        /* Handle the error. */
    }
    else {
        emptyBlock++;
    }
}

void UART_InitConfig(uart_config_t *uartConfig) {
	UART_GetDefaultConfig(uartConfig);
	uartConfig->baudRate_Bps = BOARD_DEBUG_UART_BAUDRATE;
	uartConfig->enableTx     = true;
	uartConfig->enableRx     = true;

	UART_Init(DEMO_UART, uartConfig, DEMO_UART_CLK_FREQ);
}

void SAI_InitConfig(sai_transceiver_t *saiConfig, sai_handle_t *txHandle, sai_handle_t *rxHandle, sai_master_clock_t *mclkConfig,
					 codec_handle_t *codecHandle, codec_config_t *boardCodecConfig) {
	SAI_Init(DEMO_SAI);
	SAI_TransferTxCreateHandle(DEMO_SAI, txHandle, tx_callback, NULL);
	SAI_TransferRxCreateHandle(DEMO_SAI, rxHandle, rx_callback, NULL);

	SAI_GetClassicI2SConfig(saiConfig, DEMO_AUDIO_BIT_WIDTH, kSAI_Stereo, kSAI_Channel0Mask);
	saiConfig->syncMode = DEMO_SAI_TX_SYNC_MODE;
	SAI_TransferTxSetConfig(DEMO_SAI, txHandle, saiConfig);
	saiConfig->syncMode = DEMO_SAI_RX_SYNC_MODE;
	SAI_TransferRxSetConfig(DEMO_SAI, rxHandle, saiConfig);

	SAI_TxSetBitClockRate(DEMO_SAI, DEMO_AUDIO_MASTER_CLOCK, DEMO_AUDIO_SAMPLE_RATE, DEMO_AUDIO_BIT_WIDTH,
						  DEMO_AUDIO_DATA_CHANNEL);
	SAI_RxSetBitClockRate(DEMO_SAI, DEMO_AUDIO_MASTER_CLOCK, DEMO_AUDIO_SAMPLE_RATE, DEMO_AUDIO_BIT_WIDTH,
						  DEMO_AUDIO_DATA_CHANNEL);

#if (defined(FSL_FEATURE_SAI_HAS_MCR) && (FSL_FEATURE_SAI_HAS_MCR)) || \
	(defined(FSL_FEATURE_SAI_HAS_MCLKDIV_REGISTER) && (FSL_FEATURE_SAI_HAS_MCLKDIV_REGISTER))
#if defined(FSL_FEATURE_SAI_HAS_MCLKDIV_REGISTER) && (FSL_FEATURE_SAI_HAS_MCLKDIV_REGISTER)
	mclkConfig->mclkHz          = DEMO_AUDIO_MASTER_CLOCK;
	mclkConfig->mclkSourceClkHz = DEMO_SAI_CLK_FREQ;
#endif
	SAI_SetMasterClockConfig(DEMO_SAI, mclkConfig);
#endif

	CODEC_Init(codecHandle, boardCodecConfig);

#if defined DIG_MIC
	DA7212_ChangeInput((da7212_handle_t *)((uint32_t)(codecHandle->codecDevHandle)), kDA7212_Input_MIC2);
#endif
}

u8 combined[12];

void sendFeaturesToSerial(low_level_descriptors* features) {
#if defined SPECTRAL_CENTROID_AND_SPREAD
	sprintf((char*)combined, "%.9f", features->m_spectralCentroid);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, ' ');
	sprintf((char*)combined, "%.9f", features->s_spectralCentroid);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, ' ');
	sprintf((char*)combined, "%.9f", features->m_spectralSpread);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, ' ');
	sprintf((char*)combined, "%.9f", features->s_spectralSpread);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, ' ');
#endif
#if defined SPECTRAL_FLUX
	sprintf((char*)combined, "%.9f", features->m_spectralFlux);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, ' ');
	sprintf((char*)combined, "%.9f", features->s_spectralFlux);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, ' ');
#endif
#if defined ENERGY_ENTROPY
	sprintf((char*)combined, "%.9f", features->m_energyEntropy);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, ' ');
#endif
#if defined PITCH
	sprintf((char*)combined, "%.9f", features->m_pitch);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, '\n');
	UART_WriteByte(DEMO_UART, '\r');
#endif
#if defined MFCC
	for (u32 i = 0; i < NUMBER_OF_CEPSTRALS; i++) {
		sprintf((char*)combined, "%.9f", features->m_MFCC[i]);
		UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
		if (i != NUMBER_OF_CEPSTRALS - 1) {
			UART_WriteByte(DEMO_UART, ' ');
		}
	}
	UART_WriteByte(DEMO_UART, '\n');
	UART_WriteByte(DEMO_UART, '\r');
#endif
#if defined SILENCE_CROSSING_RATE
	sprintf((char*)combined, "%.9f", features->music_activity_detection);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, ' ');
#endif
#if defined SOUND_ACTIVITY_DETECTION
	sprintf((char*)combined, "%.9f", features->sound_activity_detection);
	UART_WriteBlocking(DEMO_UART, combined, sizeof(combined) / sizeof(combined[0]));
	UART_WriteByte(DEMO_UART, '\n');
	UART_WriteByte(DEMO_UART, '\r');
	UART_WriteByte(DEMO_UART, '\n');
	UART_WriteByte(DEMO_UART, '\r');
#endif
}

int main(void) {
	sai_transfer_t xfer;
	uart_config_t uart_config;
	sai_transceiver_t sai_config;
	arm_rfft_instance_f32 RealFFT_Instance;
	arm_cfft_radix4_instance_f32 ComplexFFT_Instance;

	BOARD_InitPins();
	BOARD_BootClockRUN();
	BOARD_InitDebugConsole();
	UART_InitConfig(&uart_config);
	SAI_InitConfig(&sai_config, &txHandle, &rxHandle, &mclkConfig, &codecHandle, &boardCodecConfig);
	arm_rfft_init_f32(&RealFFT_Instance, &ComplexFFT_Instance, FFT_LEN, 0, 1);

    u32 time_index = 0;
    q15_t audio_samples[FRAME_LENGTH];
    low_level_descriptors features;
    init_LLD(&features);

    while (1) {
        if (emptyBlock > 0) {
            xfer.data     = Buffer + rx_index * BUFFER_SIZE;
            xfer.dataSize = BUFFER_SIZE;
            if (kStatus_Success == SAI_TransferReceiveNonBlocking(DEMO_SAI, &rxHandle, &xfer)) {
                rx_index++;
            }
            if (rx_index == BUFFER_NUMBER) {
                rx_index = 0U;
            }
        }
        if (emptyBlock < BUFFER_NUMBER) {
            xfer.data     = Buffer + tx_index * BUFFER_SIZE;
            xfer.dataSize = BUFFER_SIZE;
            if (kStatus_Success == SAI_TransferSendNonBlocking(DEMO_SAI, &txHandle, &xfer)) {
				for (u32 i = 0; i < BUFFER_SIZE; i += 4) {
					s16 sample = ((s16)xfer.data[i + 1] << 8) | xfer.data[i];
					audio_samples[i / 4] = sample;
				}
				arm_q15_to_float(audio_samples, features.x.samples, FRAME_LENGTH);
				compute_LowLevelDescriptors_f32(&features, time_index, RealFFT_Instance);
				time_index++;
				if (time_index == COLLECT_TIME) {
					sendFeaturesToSerial(&features);
					reload_LLD(&features);
					time_index = 0;
				}
            	tx_index++;
            }
            if (tx_index == BUFFER_NUMBER) {
                tx_index = 0U;
            }
        }
    }
    return 0;
}
