import config
import time

COLOR_RED = (255, 0, 0)
COLOR_ORANGE = (255, 128, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_OFF = (0, 0, 0)

def set_led(color):
    """Set a single WS2812 LED to the given color (R, G, B tuple) on GPIO 1."""
    try:
        import machine
        import neopixel
    except ImportError:
        print("This function requires the neopixel and machine modules (MicroPython).")
        return
    pin = machine.Pin(config.LED_GPIO, machine.Pin.OUT)
    np = neopixel.NeoPixel(pin, 1)
    np[0] = color  # color should be (R, G, B)
    np.write()

set_led(COLOR_RED)
time.sleep(1)
set_led(COLOR_ORANGE)
time.sleep(1)
set_led(COLOR_GREEN)
time.sleep(1)
set_led(COLOR_OFF)