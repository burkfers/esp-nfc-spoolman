# This file is executed on every boot (including wake-boot from deepsleep)
import gc
from time import sleep
import time
gc.collect()

from pn532 import setup_pn532

from nfc_data import find_spool_filament, parse_nfc
import wifi
print("Setting up WiFi...")
wifi.setup()

from nfc_data import read_nfc_raw, read_nfc_raw_dummy
from moonraker import set_next_spoolid
from config import DUMMY

print("Setting up PN532 NFC reader...")
pn532 = setup_pn532()

i = 1
start_time = time.ticks_ms()
while True:
    try:
        # Reset i after 10 seconds
        if time.ticks_diff(time.ticks_ms(), start_time) > 10000:
            i = 1
            start_time = time.ticks_ms()
        if i >= 10: break
        i += 1

        if DUMMY:
            from nfc_data import read_nfc_raw_dummy
            raw = read_nfc_raw_dummy()
        else:
            from nfc_data import read_nfc_raw
            print("Reading NFC data...")
            try:
                raw = read_nfc_raw(pn532, 10000)
            except Exception as e:
                print("NFC read failed, retrying...")
                i += 1
                continue
        if raw is None:
            print("No NFC data read, retrying...")
            continue
        data = parse_nfc(raw)
        result = find_spool_filament(data)
        if result is None:
            print("No SPOOL/FILAMENT data found.")
        else:
            spool_id = result[0]
            print("SPOOL_ID found:", spool_id)
            if set_next_spoolid(spool_id):
                print("Spool ID {spool_id} for next gate set successfully.")
        if DUMMY: break
        gc.collect()
        sleep(1)
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            print("KeyboardInterrupt received, exiting loop.")
            break
        print("Error during NFC processing:", type(e).__name__, e)