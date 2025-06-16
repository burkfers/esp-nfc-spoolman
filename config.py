# Moonraker host configuration
MOONRAKER_HOST = '192.168.0.41'
MOONRAKER_PORT = 80
# Set USE_NEXT_SPOOLID to True if your MMU has pre-gate sensors and supports
# auto-loading. Set this to False if your MMU does not have pre-gate sensors.
USE_NEXT_SPOOLID = True

# PN532
# NFC reader configuration
CS_GPIO = 16  # Chip Select GPIO for PN532
DUMMY = False  # Set to True to use dummy NFC reader for testing

# LED
LED_TYPE = 'neopixel'  # Options: 'neopixel', 'simple', or None
# If LED_TYPE is 'simple', specify the GPIO pins for the simple LED setup.
LED_SIMPLE_LED_PINS = [23, 22, 21]  # GPIO pins for simple LED setup in the order of error, ok, wait
# If LED_TYPE is 'neopixel', specify the GPIO pin for the WS2812 LED.
LED_NEOPIXEL_GPIO = 5  # GPIO pin for WS2812 LED
# If LED_TYPE is None, no LED will be used.