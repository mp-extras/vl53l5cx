from time import sleep

from sensor import make_sensor

from vl53l5cx import DATA_TARGET_STATUS, DATA_DISTANCE_MM, DATA_AMBIENT_PER_SPAD
from vl53l5cx import DATA_NB_SPADS_ENABLED, DATA_NB_TARGET_DETECTED
from vl53l5cx import DATA_SIGNAL_PER_SPAD, DATA_RANGE_SIGMA_MM
from vl53l5cx import DATA_REFLECTANCE, DATA_MOTION_INDICATOR


def main():
    tof = make_sensor()
    tof.reset()
    tof.init()

    length = 16

    tof.start_ranging({DATA_DISTANCE_MM, DATA_TARGET_STATUS,
                       DATA_AMBIENT_PER_SPAD,
                       DATA_NB_SPADS_ENABLED, DATA_NB_TARGET_DETECTED,
                       DATA_SIGNAL_PER_SPAD, DATA_RANGE_SIGMA_MM,
                       DATA_REFLECTANCE, DATA_MOTION_INDICATOR})

    while not tof.check_data_ready():
        sleep(0.010)

    results = tof.get_ranging_data()

    assert(len(results.distance_mm) == length)
    assert(len(results.target_status) == length)
    assert(len(results.ambient_per_spad) == length)
    assert(len(results.nb_spads_enabled) == length)
    assert(len(results.nb_target_detected))
    assert(len(results.reflectance) == length)
    assert(len(results.range_sigma_mm) == length)
    assert(len(results.signal_per_spad) == length)
    assert(results.motion_indicator)

    tof.stop_ranging()

    print("pass")


main()
