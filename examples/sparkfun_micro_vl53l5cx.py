### This is written for an RP2040 (Sparkfun Thing Plus), to provide a tab separated grid of data,
### but should work with any single I2C board, otherwise change pins (check names under board in REPL).
###
### The low power enable/disable pin is not available on the mini / low-profile Sparkfun VL53L5CX
### breakout https://www.sparkfun.com/products/19013 (if using low-power add LPN pins like examples)
###
### Designed to be visualised using processing (processing.org) as mentioned in the hookup guide
### https://learn.sparkfun.com/tutorials/qwiic-tof-imager---vl53l5cx-hookup-guide
### https://cdn.sparkfun.com/assets/learn_tutorials/2/0/0/2/SparkFun_VL53L5CX_3D_Depth_Map.zip


# depends on 
import board
import busio

from vl53l5cx.cp import VL53L5CXCP

def make_sensor():

    # lpn = low power pin, removed as using the micro VL53L5CX breakout without lpn
    scl_pin, sda_pin = (board.SCL, board.SDA)

    #i2c = busio.I2C(board.SCL1, board.SDA1,frequency=1_000_000)
    i2c = busio.I2C(scl_pin, sda_pin, frequency=1_000_000)

    return VL53L5CXCP(i2c)


from vl53l5cx import DATA_TARGET_STATUS, DATA_DISTANCE_MM
from vl53l5cx import STATUS_VALID, RESOLUTION_4X4, RESOLUTION_8X8


def main():
    tof = make_sensor()
    tof.reset()

    if not tof.is_alive():
        raise ValueError("VL53L5CX not detected")

    tof.init()

    tof.resolution = RESOLUTION_8X8
    grid = 7 # change to 3 if 4x4 grid

    tof.ranging_freq = 4 # was 2, 4 felt intense!

    tof.start_ranging({DATA_DISTANCE_MM, DATA_TARGET_STATUS})

    while True:
        if tof.check_data_ready():
            results = tof.get_ranging_data()
            distance = results.distance_mm
            status = results.target_status

            for i, d in enumerate(distance):
                if status[i] == STATUS_VALID:
                    print(d, end="")
                else:
                    print("0", end="")

                print(",", end="")

            print("")


main()