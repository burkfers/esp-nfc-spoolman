# Setup

## Secrets

1. Open `secrets.example.py` and input your Wi-Fi credentials.

    ```py
    # secrets.example.py
    WIFI_SSID = 'SSID here'
    WIFI_KEY = 'Password here'
    ```

2. Rename `secrets.example.py` to `secrets.py`.

## Configuration

Open `config.py` and work through each of the settings following the comments in the file. Below are settings for common setups.

**ESP32 with WS2812B:**

```py
LED_TYPE = 'neopixel'
LED_NEOPIXEL_GPIO = 17
```

**ESP32 with RGB LED:**

```py
LED_TYPE = 'simple'
LED_SIMPLE_LED_PINS = [23,22,21]
```

ESP8266 WIP

## Software Installation

WIP