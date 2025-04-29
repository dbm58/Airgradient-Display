import board

from airgradient import Airgradient
from connect import connect
from devices import Devices
from message_pump import *
from ui import Ui

ui = Ui(board.DISPLAY)
ui.define_fields(['CO2', 'TVOC', 'NOx'])
print(dir(ui))

requests = connect()

devices = Devices()
sn, descr = devices.current

airgradient = Airgradient()

def refresh():
    sn, descr = devices.current
    data = airgradient.fetch(requests, sn)

    ui.heading = descr
    ui['CO2'] = data.get_value('rco2')
    ui['TVOC'] = data.get_value('tvocIndex')
    ui['NOx'] = data.get_value('noxIndex')

    ui.refresh()

for msg in MessagePump():
    msg_type, msg_value = msg

    if msg_type == CHARGE_NEEDED:
        ui.battery.hidden = False
        # todo: this won't hide without a board reset
    elif msg_type == DISPLAY_DATA:
        refresh()
    elif msg_type == BUTTON_DOWN:
        ui.menu.hidden = not ui.menu.hidden
        ui.refresh()
    else:
        print('message_type', msg_type)

# -----------------------

print("Done")
