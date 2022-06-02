def make_sensor():
    mp = False
    try:
        import microcontroller
    except:
        mp = True

    if mp:
        from machine import I2C, Pin

        from vl53l5cx.mp import VL53L5CXMP

        # LILYGO TTGO
        scl_pin, sda_pin, lpn_pin, _ = (22, 21, 12, 13)

        # Pimoroni TINY2040
        # scl_pin, sda_pin, lpn_pin, irq_pin = (1, 0, 28, 5)

        i2c = I2C(0, scl=Pin(scl_pin, Pin.OUT), sda=Pin(sda_pin), freq=1_000_000)

        tof = VL53L5CXMP(i2c)
    else:
        import busio
        #from microcontroller import pin
        from digitalio import DigitalInOut, Direction

        from vl53l5cx.cp import VL53L5CXCP
        
        ## import adafruit boards library for named pins
        import boards
        
        # Sparkfun RP2040 Thing Plus or other boards with one set of SCL/SDA pins
        scl_pin, sda_pin = (boards.SCL, boards.SDA)
        
        # Pimoroni TINY2040 coupled with VL53L5CX breakout with low-power-pin (lpn)
        #scl_pin, sda_pin = (pin.GPIO1, pin.GPIO0, pin.GPIO28, pin.GPIO5)

        i2c = busio.I2C(scl_pin, sda_pin, frequency=1_000_000)

        tof = VL53L5CXCP(i2c)

    return tof
