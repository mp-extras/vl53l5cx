# MicroPython
from machine import lightsleep, Pin
from time import sleep, ticks_ms

from esp32 import wake_on_ext1, WAKEUP_ALL_LOW

from sensor import make_sensor

from vl53l5cx import DATA_TARGET_STATUS, DATA_DISTANCE_MM, POWER_MODE_WAKEUP
from vl53l5cx import RESOLUTION_4X4, RANGING_MODE_AUTONOMOUS, POWER_MODE_SLEEP


def main():
    wake_on_ext1([Pin(13, Pin.IN)], WAKEUP_ALL_LOW)
    trigger = Pin(2, Pin.OUT, value=0)
    bl = Pin(4, Pin.OUT, value=0)
    button = Pin(0)

#    while button.value():
#        pass

    trigger.value(1)
    tof = make_sensor()
    tof.reset()
    tof.init()

    tof.resolution = RESOLUTION_4X4
    tof.ranging_freq = 15
    tof.ranging_mode = RANGING_MODE_AUTONOMOUS
    tof.integration_time_ms = 10

    tof.start_ranging((DATA_DISTANCE_MM, DATA_TARGET_STATUS))

    for _ in range(10):
        lightsleep()
        results = tof.get_ranging_data()
        # print(len(results.distance_mm))

    tof.integration_time_ms = 25

    for _ in range(10):
        lightsleep()
        results = tof.get_ranging_data()
        # print(len(results.distance_mm))

    tof.stop_ranging()

    # print(ticks_ms())
    lightsleep(100)

    tof.power_mode = POWER_MODE_SLEEP
    lightsleep(1000)

    # print(ticks_ms())
    tof.power_mode = POWER_MODE_WAKEUP
    lightsleep(1000)

    # print(ticks_ms())
    trigger.value(0)

    # print("done:", tof.is_alive())


main()
