from machine import Pin
from time import sleep

from sensor import make_sensor

from vl53l5cx import POWER_MODE_WAKEUP, POWER_MODE_SLEEP


def main():
    trigger = Pin(2, Pin.OUT, value=0)
    button = Pin(0)

    tof = make_sensor()
    tof.reset()
    tof.init()

    while button.value():
        pass

    trigger.value(1)

    assert(tof.power_mode == POWER_MODE_WAKEUP)
    sleep(0.5)

    tof.power_mode = POWER_MODE_SLEEP
    assert(tof.power_mode == POWER_MODE_SLEEP)
    sleep(0.55)

    tof.power_mode = POWER_MODE_WAKEUP
    assert(tof.power_mode == POWER_MODE_WAKEUP)
    sleep(0.5)

    tof.power_mode = POWER_MODE_SLEEP
    assert(tof.power_mode == POWER_MODE_SLEEP)
    sleep(0.55)

    tof.power_mode = POWER_MODE_WAKEUP
    assert(tof.power_mode == POWER_MODE_WAKEUP)
    sleep(0.5)

    trigger.value(0)
    sleep(1)
    print("done")


main()
