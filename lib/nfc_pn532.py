# @Author: carlosgilgonzalez
# @Date:   2019-10-15T16:13:47+01:00
# @Last modified by:   carlosgilgonzalez
# @Last modified time: 2019-10-15T16:56:27+01:00


# Original work:
# Adafruit PN532 NFC/RFID control library.
# Author: Tony DiCola

# Partial Port to Micropython:
# Micropython PN532 NFC/RFID control library.
# Author: Carlos Gil Gonzalez
"""
Micropython PN532 NFC/RFID control library (SPI)
https://github.com/Carglglz/NFC_PN532_SPI
"""

import time
from machine import Pin
from micropython import const

_PREAMBLE = const(0x00)
_STARTCODE1 = const(0x00)
_STARTCODE2 = const(0xFF)
_POSTAMBLE = const(0x00)

_HOSTTOPN532 = const(0xD4)
_PN532TOHOST = const(0xD5)

_COMMAND_GETFIRMWAREVERSION = const(0x02)
_COMMAND_INLISTPASSIVETARGET = const(0x4A)
_COMMAND_INDATAEXCHANGE = const(0x40)

_MIFARE_ISO14443A = const(0x00)
MIFARE_CMD_READ = const(0x30)
_ACK = b'\x00\x00\xFF\x00\xFF\x00'
_SPI_STATREAD = const(0x02)
_SPI_DATAWRITE = const(0x01)
_SPI_DATAREAD = const(0x03)


def reverse_bit(num):
    result = 0
    for _ in range(8):
        result <<= 1
        result += (num & 1)
        num >>= 1
    return result

class PN532:
    def __init__(self, spi, cs_pin):
        self.CSB = cs_pin
        self._spi = spi
        self.CSB.on()
        self._wakeup()

    def _wakeup(self):
        time.sleep(1)
        self.CSB.off()
        time.sleep_ms(2)
        self._spi.write(bytearray([0x00]))
        time.sleep_ms(2)
        self.CSB.on()
        time.sleep(1)

    def _wait_ready(self, timeout=1000):
        status_query = bytearray([reverse_bit(_SPI_STATREAD), 0])
        status = bytearray([0, 0])
        timestamp = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), timestamp) < timeout:
            time.sleep(0.02)
            self.CSB.off()
            time.sleep_ms(2)
            self._spi.write_readinto(status_query, status)
            time.sleep_ms(2)
            self.CSB.on()
            if reverse_bit(status[1]) == 0x01:
                return True
            time.sleep(0.01)
        return False

    def _read_data(self, count):
        frame = bytearray(count+1)
        frame[0] = reverse_bit(_SPI_DATAREAD)
        time.sleep(0.02)
        self.CSB.off()
        time.sleep_ms(2)
        self._spi.write_readinto(frame, frame)
        time.sleep_ms(2)
        self.CSB.on()
        for i, val in enumerate(frame):
            frame[i] = reverse_bit(val)
        return frame[1:]

    def _write_data(self, framebytes):
        rev_frame = [reverse_bit(x) for x in bytes([_SPI_DATAWRITE]) + framebytes]
        time.sleep(0.02)
        self.CSB.off()
        time.sleep_ms(2)
        self._spi.write(bytes(rev_frame))
        time.sleep_ms(2)
        self.CSB.on()

    def _write_frame(self, data):
        length = len(data)
        frame = bytearray(length+8)
        frame[0] = _PREAMBLE
        frame[1] = _STARTCODE1
        frame[2] = _STARTCODE2
        checksum = sum(frame[0:3])
        frame[3] = length & 0xFF
        frame[4] = (~length + 1) & 0xFF
        frame[5:-2] = data
        checksum += sum(data)
        frame[-2] = ~checksum & 0xFF
        frame[-1] = _POSTAMBLE
        self._write_data(bytes(frame))

    def _read_frame(self, length):
        response = self._read_data(length+8)
        offset = 0
        while response[offset] == 0x00:
            offset += 1
            if offset >= len(response):
                return None
        if response[offset] != 0xFF:
            return None
        offset += 1
        if offset >= len(response):
            return None
        frame_len = response[offset]
        if (frame_len + response[offset+1]) & 0xFF != 0:
            return None
        checksum = sum(response[offset+2:offset+2+frame_len+1]) & 0xFF
        if checksum != 0:
            return None
        return response[offset+2:offset+2+frame_len]

    def call_function(self, command, response_length=0, params=[], timeout=1000):
        data = bytearray(2+len(params))
        data[0] = _HOSTTOPN532
        data[1] = command & 0xFF
        for i, val in enumerate(params):
            data[2+i] = val
        try:
            self._write_frame(data)
        except OSError:
            self._wakeup()
            return None
        if not self._wait_ready(timeout):
            return None
        if not _ACK == self._read_data(len(_ACK)):
            return None
        if not self._wait_ready(timeout):
            return None
        response = self._read_frame(response_length+2)
        if not response or not (response[0] == _PN532TOHOST and response[1] == (command+1)):
            return None
        return response[2:]

    def get_firmware_version(self):
        """Call PN532 GetFirmwareVersion function and return a tuple with the IC,
        Ver, Rev, and Support values.
        """
        response = self.call_function(
            _COMMAND_GETFIRMWAREVERSION, 4, timeout=500)
        if response is None:
            raise RuntimeError('Failed to detect the PN532')
        return tuple(response)

    def read_passive_target(self, card_baud=_MIFARE_ISO14443A, timeout=1000):
        try:
            response = self.call_function(_COMMAND_INLISTPASSIVETARGET,
                                          params=[0x01, card_baud],
                                          response_length=19,
                                          timeout=timeout)
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise e
            return None
        if response is None:
            return None
        if response[0] != 0x01:
            return None
        if response[5] > 7:
            return None
        return response[6:6+response[5]]

    def mifare_classic_read_block(self, block_number):
        response = self.call_function(_COMMAND_INDATAEXCHANGE,
                                      params=[0x01, MIFARE_CMD_READ,
                                              block_number & 0xFF],
                                      response_length=17)
        if response is None or response[0] != 0x00:
            return None
        return response[1:]
