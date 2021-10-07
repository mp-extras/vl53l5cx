from machine import Pin, I2C
from time import ticks_ms

from adafruit_fancyled import CRGB, CHSV

from vl53l5cx.mp import VL53L5CXMP
from vl53l5cx import RESOLUTION_4X4, RESOLUTION_8X8, RANGING_MODE_CONTINUOUS
from vl53l5cx import DATA_DISTANCE_MM, DATA_TARGET_STATUS
from vl53l5cx import STATUS_VALID, STATUS_VALID_LARGE_PULSE

import board

# TTGO is 240 x 135
XY_DIM = 9
SPACE = 5
GAP = XY_DIM + SPACE
OFFSET = 10

def box(display, index, grid, distance, target):
    x = index % grid
    y = index // grid
    if (target == STATUS_VALID) or (target == STATUS_VALID_LARGE_PULSE):
        scaled = distance / 4000.0
        rgb = CRGB(CHSV(scaled, 255, 128))
        color = display.rgbcolor(int(rgb.red * 255), int(rgb.green * 255),
                                       int(rgb.blue * 255))
    else:
        color = 0
    display.fill_rect(x * GAP + 10, y * GAP + 10, XY_DIM, XY_DIM, color)


def main():
    display = board.make_display()

    # TINY2040
    # scl_pin, sda_pin, lpn_pin, irq_pin = (1, 0, 28, 5)

    # TTGO T-Display
    scl_pin, sda_pin, lpn_pin, _ = (22, 21, 12, 13)

    i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=1_000_000)

    tof = VL53L5CXMP(i2c, lpn=Pin(lpn_pin, Pin.OUT, value=1))
    tof.reset()
    tof.init()

    tof.resolution = RESOLUTION_8X8
    grid = 8

    tof.ranging_freq = 15
    tof.ranging_mode = RANGING_MODE_CONTINUOUS
    tof.integration_time_ms = 15

    tof.start_ranging({DATA_DISTANCE_MM, DATA_TARGET_STATUS})

    prev = ticks_ms()
    while True:
        if tof.check_data_ready():
            now = ticks_ms()
            delta = now - prev
            prev = now

            results = tof.get_ranging_data()
            distances = results.distance_mm
            target = results.target_status

            display.fill(0)
            for i, d in enumerate(distances):
                box(display, i, grid, d, target[i])

            display.text("{} {} {}".format(min(distances), max(distances),
                                           int(1000 / delta)),
                         10, 200, display.rgbcolor(255, 0, 0))

            display.show()


main()
