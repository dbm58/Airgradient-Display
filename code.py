from connect import connect
from airgradient import Airgradient
from display import Display
from devices import Devices
# todo:  get a better font
#import adafruit_bitmap_font
# ----
import alarm
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

pin_alarm_a = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True)
pin_alarm_c = alarm.pin.PinAlarm(pin=board.BUTTON_C, value=False, pull=True)
pin_alarm_d = alarm.pin.PinAlarm(pin=board.BUTTON_D, value=False, pull=True)

triggered_alarm = None
while True:
    if isinstance(triggered_alarm, alarm.pin.PinAlarm):
        if triggered_alarm == pin_alarm_a:
            select_datum()
        elif triggered_alarm == pin_alarm_c:
            refresh()
        elif triggered_alarm == pin_alarm_d:
            next_floor()
    elif isinstance(triggered_alarm, alarm.time.TimeAlarm):
        refresh()
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 60)
    triggered_alarm = alarm.light_sleep_until_alarms(pin_alarm_a, pin_alarm_c, pin_alarm_d, time_alarm)

# -----------------------

print("Done")
