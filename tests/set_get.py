from sensor import make_sensor

from vl53l5cx import RESOLUTION_4X4, TARGET_ORDER_CLOSEST
from vl53l5cx import RANGING_MODE_AUTONOMOUS


def main():
    tof = make_sensor()

    tof.reset()
    tof.init()

    tof.resolution = RESOLUTION_4X4
    assert(tof.resolution == RESOLUTION_4X4)

    tof.ranging_freq = 10
    assert(tof.ranging_freq == 10)

    tof.target_order = TARGET_ORDER_CLOSEST
    assert(tof.target_order == TARGET_ORDER_CLOSEST)

    tof.integration_time_ms = 30
    assert(tof.integration_time_ms == 30)

    tof.sharpener_percent = 52
    assert(tof.sharpener_percent <= 52 and tof.sharpener_percent >= 51)

    tof.ranging_mode = RANGING_MODE_AUTONOMOUS
    assert(tof.ranging_mode == RANGING_MODE_AUTONOMOUS)

    print("pass")


if __name__ == "__main__":
    main()
