from accelerometer import Accelerometer
from airgradient import Airgradient
from battery import Battery
from connect import connect
from devices import Devices
from Display.horizontal import Horizontal
from Display.vertical import Vertical
from message_pump import *

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
    # if accel.portrait:
    #     display = vertical
    # else:
    #     display = horizontal
    # display.rotation = accel.rotation

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
    
for msg in MessagePump():
    msg_type, msg_value = msg
    if msg_type == DISPLAY_DATA:
        refresh()
    elif msg_type == CHANGE_ORIENTATION:
        print('in handler')
        if display == vertical:
            display = horizontal
        else:
            display = vertical
        refresh()
    else:
        print('message_type', msg_type)

# -----------------------

print("Done")
