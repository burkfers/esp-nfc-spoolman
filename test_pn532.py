# Tiny test ro run directly (eg via `ampy run test_pn532.py`) to see if the PN532 is working and reading NFC tags.
from pn532 import setup_pn532
from nfc_data import read_nfc_raw
sensor = setup_pn532()
ic, ver, rev, support = sensor.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
from time import sleep
while 1:
    uid = sensor.read_passive_target()
    read = read_nfc_raw(sensor, 1000)
    print(uid, read)
    sleep(1)
