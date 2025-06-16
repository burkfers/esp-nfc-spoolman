# TWITS
## That Which Inspects The Spools (working title)

This project, inspired by [nfc2klipper](https://github.com/bofh69/nfc2klipper), uses an inexpensive NFC module and a wifi-capable microcontroller to read spool tags and send the info to your printer.
nfc2klipper is nice, but I wanted to avoid running wires all the way from the top of the printer to the electronics bay. By going wifi, I only needed to steal 5V from the MMU, which conveniently is on the top.

**Features:**
- NFC Tag scanning and sending the info to Moonraker
- Supports a single neopixel or three simple LEDs for status display

**Typical Use Case:**
- Scan an NFC tag attached to a filament spool
- The microcontroller reads the tag info and send an update to Happy Hare
- Load the spool into your MMU
- Happy Hare now knows which spoolman SpoolID you just loaded and fetches the relevant details, and is ready to update filament usage

## BOM (bill of materials)

- Wemos D1 Mini (ESP8266) or 38-Pin ESP32C \[ [Amazon US](https://www.amazon.com/dp/B09J95SMG7) \]
  - Will likely work on any ESP-type controller with minimal changes
- PN532 module \[ [Aliexpress](https://www.aliexpress.com/item/1005007182056113.html) \]
- A single neopixel, such as an SK6812 Mini-E, or three dumb LEDs (optional)
- A handful of wiring, soldering and crimping supplies

## Build
TODO

## Setup
TODO

## Troubleshooting
You can `ampy run test_pn532.py` to check for communication with the NFC module. If you don't see
```
Found PN532 with firmware version: 1.6
```
(or other version), the wiring is probably not quite right yet.

## License
This work is licensed as CC-BY-NC-4.0

## Credits
Thanks to
- @3DCoded for testing, ideas and development assistance
- @nom3rcy. for the idea to use a dedicated microcontroller to avoid long wire runs