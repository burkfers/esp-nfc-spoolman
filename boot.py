import gc
from time import sleep
import time
gc.collect()

from pn532 import setup_pn532

from ledcontrol import set_led, LED_READY, LED_OK, LED_WAIT, LED_ERROR
from ledcontrol import led_timer as flash_led_timer
set_led(LED_WAIT)

from nfc_data import find_spool_filament, parse_nfc
import wifi
print("Setting up WiFi...")
wifi.setup()
if not wifi.wait_for_wifi():
    set_led(LED_ERROR)
    print("Failed to connect to WiFi, exiting.")

from nfc_data import read_nfc_raw, read_nfc_raw_dummy
from moonraker import set_next_spoolid
from config import DUMMY

print("Setting up PN532 NFC reader...")
pn532 = setup_pn532()
try:
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
except:
    flash_led_timer.deinit()
    set_led(LED_ERROR)
    raise

flash_led_timer.deinit()

set_led(LED_READY)

def set_led_timer(status):
    global led_timer
    led_timer = time.ticks_ms()
    set_led(status)

led_timer = None

while True:
    try:
        # Since Ctrl-C only stops the NFC read returning None instead of exiting,
        # we break the loop if we've iterated 10 times in the span of 5 seconds
        # Simply hammer Ctrl-C on the console to get the REPL.

        # reset the LED every 5 seconds
        if led_timer and time.ticks_diff(time.ticks_ms(), led_timer) > 5000:
            led_timer = None
            set_led(LED_READY)

        if DUMMY:
            from nfc_data import read_nfc_raw_dummy
            raw = read_nfc_raw_dummy()
        else:
            from nfc_data import read_nfc_raw
            print("Reading NFC data...")
            try:
                raw = read_nfc_raw(pn532, 500)
            except KeyboardInterrupt:
                print("KeyboardInterrupt received, exiting")
                break
            except Exception as e:
                set_led_timer(LED_ERROR)
                print("NFC read failed, retrying...")
                continue
        if raw is None:
            # timed out because no tag nearby, OR Ctrl-C was pressed
            print("No NFC data read, retrying...")
            continue
        set_led_timer(LED_WAIT)
        data = parse_nfc(raw)
        result = find_spool_filament(data)
        if result is None:
            set_led_timer(LED_ERROR)
            print("No SPOOL/FILAMENT data found.")
            continue
        else:
            spool_id = result[0]
            print("SPOOL_ID found:", spool_id)
            if set_next_spoolid(spool_id):
                set_led_timer(LED_OK)
                print("Spool ID {spool_id} for next gate set successfully.")
                sleep(5) # Don't immediately read again
            else:
                set_led_timer(LED_ERROR)
        if DUMMY: break
        gc.collect()
        sleep(0.5)
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            print("KeyboardInterrupt received, exiting loop.")
            break
        set_led_timer(LED_ERROR)
        print("Error during NFC processing:", type(e).__name__, e)


print("Script end")

