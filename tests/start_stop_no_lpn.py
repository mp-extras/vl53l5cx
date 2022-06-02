from time import sleep

from sensor_no_lpn import make_sensor

from vl53l5cx import DATA_TARGET_STATUS, DATA_DISTANCE_MM
from vl53l5cx import RESOLUTION_4X4, RESOLUTION_8X8


def main():
    tof = make_sensor()
    tof.reset()
    tof.init()

    tof.ranging_freq = 15

    for i in range(10):
        if i & 0x1:
            tof.resolution = RESOLUTION_4X4
            length = 16
        else:
            tof.resolution = RESOLUTION_8X8
            length = 64

        tof.start_ranging({DATA_DISTANCE_MM, DATA_TARGET_STATUS})

        while not tof.check_data_ready():
            sleep(0.010)

        results = tof.get_ranging_data()

        assert(len(results.distance_mm) == length)
        assert(len(results.target_status) == length)
        assert(not results.motion_indicator)

        tof.stop_ranging()

    print("pass")


main()
