def setup():
    import network, secrets
    sta_if = network.WLAN(network.WLAN.IF_STA)
    ap_if = network.WLAN(network.WLAN.IF_AP)
    ap_if.active(False)
    sta_if.active(True)
    sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_KEY)
    

def wait_for_wifi(timeout_ms=10000):
    import network
    import time
    sta_if = network.WLAN(network.WLAN.IF_STA)
    start = time.ticks_ms()
    while not sta_if.isconnected():
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            return False
        time.sleep(0.1)
    return True
