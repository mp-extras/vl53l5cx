# MicroPython
from machine import lightsleep, Pin
from esp32 import wake_on_ext1, WAKEUP_ALL_LOW

from sensor import make_sensor

from vl53l5cx import DATA_TARGET_STATUS, DATA_DISTANCE_MM
from vl53l5cx import RESOLUTION_4X4


def main():
    wake_on_ext1([Pin(13, Pin.IN)], WAKEUP_ALL_LOW)

    tof = make_sensor()
    tof.reset()
    tof.init()

    tof.resolution = RESOLUTION_4X4
    tof.ranging_freq = 30

    tof.start_ranging({DATA_DISTANCE_MM, DATA_TARGET_STATUS})

    while True:
        lightsleep()

        results = tof.get_ranging_data()
        print(min(results.distance_mm), max(results.distance_mm))


main()
