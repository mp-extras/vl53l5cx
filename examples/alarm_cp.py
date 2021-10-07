# CircuitPython
import alarm
from microcontroller import pin

from sensor import make_sensor

from vl53l5cx import DATA_TARGET_STATUS, DATA_DISTANCE_MM
from vl53l5cx import RESOLUTION_4X4


def main():
    pin_alarm = alarm.pin.PinAlarm(pin=pin.GPIO5, value=False, pull=True)

    tof = make_sensor()
    tof.reset()
    tof.init()

    tof.resolution = RESOLUTION_4X4
    tof.ranging_freq = 30

    tof.start_ranging({DATA_DISTANCE_MM, DATA_TARGET_STATUS})

    while True:
        alarm.light_sleep_until_alarms(pin_alarm)

        results = tof.get_ranging_data()
        print(min(results.distance_mm), max(results.distance_mm))


main()
