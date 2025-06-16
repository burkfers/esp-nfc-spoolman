# Moonraker printer host configuration
MOONRAKER_HOST = '192.168.0.41'
MOONRAKER_PORT = 80
CS_GPIO = 16  # Chip Select GPIO for PN532
DUMMY = False  # Set to True to use dummy NFC reader for testing

LED_GPIO = 5  # GPIO for LED indicator

SIMPLE_LED_PINS = [23,22,21]

# Set USE_NEXT_SPOOLID to True if your MMU has pre-gate sensors and supports
# auto-loading. Set this to False if your MMU does not have pre-gate sensors.
USE_NEXT_SPOOLID = False