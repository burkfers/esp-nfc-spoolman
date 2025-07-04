from config import LED_TYPE, LED_STEALTH
from machine import Timer


if LED_TYPE == 'neopixel':
    def set_led(color):
        import machine
        import neopixel
        from config import LED_NEOPIXEL_GPIO
        pin = machine.Pin(LED_NEOPIXEL_GPIO, machine.Pin.OUT)
        np = neopixel.NeoPixel(pin, 1)
        np[0] = color  # color should be (R, G, B)
        np.write()

    if LED_STEALTH:
        LED_READY = (0, 0, 0)
    else:
        LED_READY = (0, 0, 255)
    LED_OK = (0, 255, 0)
    LED_WAIT = (0, 0, 255)
    LED_ERROR = (255, 0, 0)
    LED_OFF = (0, 0, 0)

elif LED_TYPE == 'simple':
    from machine import Pin
    from config import LED_SIMPLE_LED_PINS as PINS

    LEDS = [
        Pin(PINS[0], Pin.OUT),
        Pin(PINS[1], Pin.OUT),
        Pin(PINS[2], Pin.OUT),
    ]

    def set_led(p):
        for i in range(len(p)):
            LEDS[i].value(p[i])

    if LED_STEALTH:
        LED_READY = (0, 0, 0)
    else:
        LED_READY = (0, 0, 1)
    LED_OK = (0, 1, 0)
    LED_WAIT = (0, 0, 1)
    LED_ERROR = (1, 0, 0)
    LED_OFF = (0, 0, 0)

else:

    def set_led(dummy):
        """Dummy function for no LED setup."""
        pass
    LED_READY = None
    LED_OK = None
    LED_WAIT = None
    LED_ERROR = None
    LED_OFF = None

_last_led = 'off'
def led_timer_callback(timer):
    global _last_led
    if _last_led == 'off':
        set_led(LED_WAIT)
        _last_led = 'wait'
    else:
        set_led(LED_OFF)
        _last_led = 'off'

led_timer = Timer(0)
led_timer.init(period=250, mode=Timer.PERIODIC, callback=led_timer_callback)
