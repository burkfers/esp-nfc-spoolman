from simple_led import set_led

def led_off():
    set_led(0,0,0)

def led_error():
    set_led(1,0,0)

def led_ok():
    set_led(0,1,0)

def led_wait():
    set_led(0,0,1)