from connect import connect
from airgradient import Airgradient
from display import Display
from devices import Devices
# todo:  get a better font
#import adafruit_bitmap_font
# ----
import time
import board

# todo:  battery indicator
# todo:  implement datum selector
# todo:  implement refresh rate selector (also needs button)

requests = connect()

devices = Devices()
sn, descr = devices.current

airgradient = Airgradient()
data = airgradient.fetch(requests, sn)

display = Display()
display.floor = descr
display.co2 = data.co2
display.refresh()

def select_datum():
    pass

def refresh():
    sn, descr = devices.current
    data = airgradient.fetch(requests, sn)
    display.floor = descr
    display.co2 = data.co2
    display.refresh()

def next_floor():
    sn, descr = devices.next()
    data = airgradient.fetch(requests, sn)
    display.floor = descr
    display.co2 = data.co2
    display.refresh()
    
button_funcs = [
    { 'button': board.BUTTON_A, 'func': select_datum },
    { 'button': board.BUTTON_C, 'func': refresh      },
    { 'button': board.BUTTON_D, 'func': next_floor   },
]

import keypad
button_pins = (board.BUTTON_A, board.BUTTON_C, board.BUTTON_D)
buttons = keypad.Keys(button_pins, value_when_pressed=False, pull=True)

now = time.monotonic()
while True:
    # go to sleep.  wake up on button, and timer
    button = buttons.events.get()
    if button:
        if button.released:
            button_funcs[button.key_number]['func']()

    if (now + 60) < time.monotonic():
        refresh()
        now = time.monotonic()

    time.sleep(0.01)


# -----------------------

print("Done")
