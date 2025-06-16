from machine import Pin
from config import SIMPLE_LED_PINS as PINS

LEDS = [
    Pin(PINS[0], Pin.OUT),
    Pin(PINS[1], Pin.OUT),
    Pin(PINS[2], Pin.OUT),
]

def set_led(*p):
    for i in range(len(p)):
        LEDS[i].value(p[i])