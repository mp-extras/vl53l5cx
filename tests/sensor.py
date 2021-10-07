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

        tof = VL53L5CXMP(i2c, lpn=Pin(lpn_pin, Pin.OUT, value=1))
    else:
        import busio
        from microcontroller import pin
        from digitalio import DigitalInOut, Direction

        from vl53l5cx.cp import VL53L5CXCP

        # Pimoroni TINY2040
        scl_pin, sda_pin, lpn_pin, _ = (pin.GPIO1, pin.GPIO0, pin.GPIO28, pin.GPIO5)
        i2c = busio.I2C(scl_pin, sda_pin, frequency=1_000_000)

        lpn = DigitalInOut(lpn_pin)
        lpn.direction = Direction.OUTPUT
        lpn.value = True

        tof = VL53L5CXCP(i2c, lpn=lpn)

    return tof
