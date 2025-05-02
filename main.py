import board

from airgradient import Airgradient
from connect import connect
from devices import Devices
from message_pump import *
from ui import Ui

ui = Ui(board.DISPLAY)
ui.define_fields(['CO2', 'TVOC', 'NOx'])

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

def button_handler_menu_closed(msg_type, msg_vlaue):
    global button_handler
    if msg_type == BUTTON_DOWN:
        if ui.menu.hidden:
            ui.menu.hidden = False
            ui.refresh()
    elif msg_type == BUTTON_UP:
        button_handler = button_handler_menu_open

def button_handler_menu_open(msg_type, msg_vlaue):
    global button_handler
    if msg_type == BUTTON_DOWN_A:
        if not ui.menu.hidden:
            ui.menu.hidden = True
            ui.refresh()
    elif msg_type == BUTTON_DOWN_B:
        pass
    elif msg_type == BUTTON_DOWN_C:
        pass
    elif msg_type == BUTTON_DOWN_D:
        if not ui.menu.hidden:
            ui.menu.hidden = True
            refresh()
    elif msg_type == BUTTON_UP:
        button_handler = button_handler_menu_closed

button_handler = button_handler_menu_closed

for msg in MessagePump():
    msg_type, msg_value = msg

    if msg_type == CHARGE_NEEDED:
        ui.battery.hidden = False
        # todo: this won't hide without a board reset
    elif msg_type == DISPLAY_DATA:
        if ui.menu.hidden:
            refresh()
    else:
        button_handler(msg_type, msg_value)

# -----------------------

print("Done")
