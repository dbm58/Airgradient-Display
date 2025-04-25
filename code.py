import supervisor
supervisor.set_next_code_file('test.ui.py')
# supervisor.set_next_code_file('main.py')
supervisor.reload()

import alarm
import time
import board

from airgradient import Airgradient
from battery import Battery
from connect import connect
from devices import Devices
from Display.horizontal import Horizontal
from Display.vertical import Vertical
from accelerometer import Accelerometer

horizontal = Horizontal()
vertical = Vertical()
display = vertical

requests = connect()

devices = Devices()
sn, descr = devices.current

airgradient = Airgradient()
battery = Battery()

accel = Accelerometer()

props = [
    {"prop": "rco2",      "descr": "CO2" },
    {"prop": "atmp",      "descr": "Temp"},
    {"prop": "tvocIndex", "descr": "TVOC"},
    {"prop": "noxIndex",  "descr": "NOx" },
]
prop = props[0]

refresh_rates = [1, 2, 5]
refresh_rate = refresh_rates[0]

def select_datum():
    pass

def select_rate():
    pass
    
def refresh():
    if accel.portrait:
        display = vertical
    else:
        display = horizontal
    display.rotation = accel.rotation

    sn, descr = devices.current
    data = airgradient.fetch(requests, sn)

    display.location = descr
    display.value1 = data.get_value('rco2')
    display.value1_label = 'CO2'
    display.value2 = data.get_value('tvocIndex')
    display.value2_label = 'TVOC'
    display.value3 = data.get_value('noxIndex')
    display.value3_label = 'NOx'

    display.charge_needed = battery.charge_needed
    
    display.refresh()

def next_floor():
    devices.next()
    refresh()
    
pin_alarm_a = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True)
pin_alarm_b = alarm.pin.PinAlarm(pin=board.BUTTON_B, value=False, pull=True)
pin_alarm_c = alarm.pin.PinAlarm(pin=board.BUTTON_C, value=False, pull=True)
pin_alarm_d = alarm.pin.PinAlarm(pin=board.BUTTON_D, value=False, pull=True)
buttons = (pin_alarm_a, pin_alarm_b, pin_alarm_c, pin_alarm_d)

refresh()
triggered_alarm = None
while True:
    if isinstance(triggered_alarm, alarm.pin.PinAlarm):
        if triggered_alarm == pin_alarm_a:
            #props = props[1:] + props[:1]
            #prop = props[0]
            if display == vertical:
                display = horizontal
            else:
                display = vertical
            refresh()
        elif triggered_alarm == pin_alarm_b:
            refresh_rates = refresh_rates[1:] + refresh_rates[:1]
            refresh_rate = refresh_rates[0]
            refresh()
        elif triggered_alarm == pin_alarm_c:
            refresh()
        elif triggered_alarm == pin_alarm_d:
            next_floor()
    elif isinstance(triggered_alarm, alarm.time.TimeAlarm):
        refresh()
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + (60 * refresh_rate))
    triggered_alarm = alarm.light_sleep_until_alarms(*(buttons), time_alarm)

# -----------------------

print("Done")
