from config import CS_GPIO

def setup_pn532():
    import lib.nfc_pn532 as nfc
    from machine import Pin, SPI

    # SPI
    spi_dev = SPI(1, baudrate=1000000)
    cs = Pin(CS_GPIO, Pin.OUT)
    cs.on()

    # SENSOR INIT
    pn532 = nfc.PN532(spi_dev,cs)

    # My NFC reader doesn't like to use the IRQ pin
    pn532.call_function(0x14,
                           params=[0x01, 0x14, 0x0])

    return pn532