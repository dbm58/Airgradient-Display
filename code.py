import alarm
import time
import board

from airgradient import Airgradient
from battery import Battery
from connect import connect
from devices import Devices
from display import Display

# todo:  battery indicator
# todo:  implement datum selector
# todo:  implement refresh rate selector (also needs button)

requests = connect()

devices = Devices()
sn, descr = devices.current

airgradient = Airgradient()
# data = airgradient.fetch(requests, sn)
battery = Battery()

display = Display()
#display.floor = descr
#display.co2 = data.co2
#display.refresh()

def select_datum():
    pass

def refresh():
    sn, descr = devices.current
    data = airgradient.fetch(requests, sn)

    display.floor = descr
    display.co2 = data.co2
    display.charge_needed = battery.charge_needed
    display.refresh()

def next_floor():
    devices.next()
    refresh()
    
pin_alarm_a = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True)
pin_alarm_b = alarm.pin.PinAlarm(pin=board.BUTTON_B, value=False, pull=True)
pin_alarm_c = alarm.pin.PinAlarm(pin=board.BUTTON_C, value=False, pull=True)
pin_alarm_d = alarm.pin.PinAlarm(pin=board.BUTTON_D, value=False, pull=True)
buttons = (pin_alarm_a, pin_alarm_c, pin_alarm_d)

refresh()
triggered_alarm = None
while True:
    if isinstance(triggered_alarm, alarm.pin.PinAlarm):
        if triggered_alarm == pin_alarm_a:
            select_datum()
        elif triggered_alarm == pin_alarm_b:
            print('toggling battery')
            display.charge_needed = not display.charge_needed
            refresh()
        elif triggered_alarm == pin_alarm_c:
            refresh()
        elif triggered_alarm == pin_alarm_d:
            next_floor()
    elif isinstance(triggered_alarm, alarm.time.TimeAlarm):
        refresh()
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 60)
    triggered_alarm = alarm.light_sleep_until_alarms(*(buttons), time_alarm)

# -----------------------

print("Done")
