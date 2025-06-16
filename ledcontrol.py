from config import LED_TYPE

if LED_TYPE == 'neopixel':    
    def set_led(color):
        import machine
        import neopixel
        from config import LED_NEOPIXEL_GPIO
        pin = machine.Pin(LED_NEOPIXEL_GPIO, machine.Pin.OUT)
        np = neopixel.NeoPixel(pin, 1)
        np[0] = color  # color should be (R, G, B)
        np.write()

    def led_off():
        set_led((0, 0, 0))

    def led_error():
        set_led((255, 0, 0))

    def led_ok():
        set_led((0, 255, 0))

    def led_wait():
        set_led((0, 0, 255))
    
elif LED_TYPE == 'simple':
    from machine import Pin
    from config import LED_SIMPLE_LED_PINS as PINS

    LEDS = [
        Pin(PINS[0], Pin.OUT),
        Pin(PINS[1], Pin.OUT),
        Pin(PINS[2], Pin.OUT),
    ]

    def set_led(*p):
        for i in range(len(p)):
            LEDS[i].value(p[i])
    def led_off():
        set_led(0,0,0)

    def led_error():
        set_led(1,0,0)

    def led_ok():
        set_led(0,1,0)

    def led_wait():
        set_led(0,0,1)

else:
    def led_off():
        pass

    def led_error():
        pass

    def led_ok():
        pass

    def led_wait():
        pass