from pn532 import setup_pn532
from nfc_data import read_nfc_raw
sensor = setup_pn532()
from time import sleep
while 1:
    uid = sensor.read_passive_target()
    read = read_nfc_raw(sensor, 1000)
    print(uid, read)
    sleep(1)
