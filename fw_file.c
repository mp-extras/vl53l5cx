/*
 * Convert firware and config data to binary file for loading
 *
 * Copyright (c) 2021 Mark Grosen <mark@grosen.org>
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define VL53L5CX_NB_TARGET_PER_ZONE 1U
#include <vl53l5cx_buffers.h>

#define VL53L5CX_XTALK_BUFFER_SIZE		((uint16_t)776U)

void SwapBuffer( uint8_t   *buffer, uint16_t     size) {

    // Example of possible implementation using <string.h>
    for(uint32_t i = 0; i < size; i = i + 4) {

        uint32_t tmp = (
                buffer[i]<<24)
            |(buffer[i+1]<<16)
            |(buffer[i+2]<<8)
            |(buffer[i+3]);

        memcpy(&(buffer[i]), &tmp, 4);
    }
}

static void xtalk_4x4(uint8_t * xtalk4x4_data, const uint8_t * xtalk_data)
{
    uint8_t res4x4[] = {0x0F, 0x04, 0x04, 0x17, 0x08, 0x10, 0x10, 0x07};
    uint8_t dss_4x4[] = {0x00, 0x78, 0x00, 0x08, 0x00, 0x00, 0x00, 0x08};
    uint8_t profile_4x4[] = {0xA0, 0xFC, 0x01, 0x00};
    uint32_t signal_grid[64];
    int8_t i, j;

    (void)memcpy(xtalk4x4_data, xtalk_data,
                 VL53L5CX_XTALK_BUFFER_SIZE);

    (void)memcpy(&(xtalk4x4_data[0x8]), res4x4, sizeof(res4x4));
    (void)memcpy(&(xtalk4x4_data[0x020]), dss_4x4, sizeof(dss_4x4));

    SwapBuffer(xtalk4x4_data, VL53L5CX_XTALK_BUFFER_SIZE);
    (void)memcpy(signal_grid, &(xtalk4x4_data[0x34]),
                 sizeof(signal_grid));

    for (j = 0; j < (int8_t)4; j++) {
        for (i = 0; i < (int8_t)4; i++) {
            signal_grid[i + (4 * j)] = (signal_grid[(2 * i) + (16 * j) + 0] +
                                        signal_grid[(2 * i) + (16 * j) + 1] +
                                        signal_grid[(2 * i) + (16 * j) + 8] +
                                        signal_grid[(2 * i) + (16 * j) + 9]) / (uint32_t)4;
        }
    }
    (void)memset(&signal_grid[0x10], 0, (uint32_t)192);
    (void)memcpy(&(xtalk4x4_data[0x34]), signal_grid,
                 sizeof(signal_grid));
    SwapBuffer(xtalk4x4_data, VL53L5CX_XTALK_BUFFER_SIZE);
    (void)memcpy(&(xtalk4x4_data[0x134]), profile_4x4,
                 sizeof(profile_4x4));
    (void)memset(&(xtalk4x4_data[0x078]), 0,
                 (uint32_t)4 * sizeof(uint8_t));
}

int main(int argc, char * argv[])
{
    uint8_t xtalk4x4_data[VL53L5CX_XTALK_BUFFER_SIZE];
    FILE * fp;
    int status = -1;

    if ((fp = fopen("vl_fw_config.bin", "wb")) != NULL) {
        fwrite(VL53L5CX_FIRMWARE, sizeof(VL53L5CX_FIRMWARE), 1, fp);
        fwrite(VL53L5CX_DEFAULT_CONFIGURATION,
               sizeof(VL53L5CX_DEFAULT_CONFIGURATION), 1, fp);
        fwrite(VL53L5CX_DEFAULT_XTALK, sizeof(VL53L5CX_DEFAULT_XTALK), 1, fp);
        xtalk_4x4(xtalk4x4_data, VL53L5CX_DEFAULT_XTALK);
        fwrite(xtalk4x4_data, sizeof(xtalk4x4_data), 1, fp);

        fclose(fp);
        status = 0;

        printf("%ld %ld %ld %ld\n", sizeof(VL53L5CX_FIRMWARE),
               sizeof(VL53L5CX_DEFAULT_CONFIGURATION),
               sizeof(VL53L5CX_DEFAULT_XTALK),
               sizeof(xtalk4x4_data));
    }

    return status;
}
