import board
import wifi

from airgradient import Airgradient
from battery import Battery
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
battery = Battery()

def refresh():
    if not wifi.radio.connected:
        ui.wifi_off_dialog.hidden = False
        ui.refresh()
        return

    if battery.charge_needed:
        ui.battery_alert_dialog.hidden = False
        ui.refresh()
        return

    try:
        sn, descr = devices.current
        data = airgradient.fetch(requests, sn)
    except Exception:
        ui.hourglass_dialog.hidden = False
    else:
        ui.battery_alert_dialog.hidden = True
        ui.hourglass_dialog.hidden = True
        ui.wifi_off_dialog.hidden = True

        ui.heading = descr
        ui['CO2'] = data.get_value('rco2')
        ui['TVOC'] = data.get_value('tvocIndex')
        ui['NOx'] = data.get_value('noxIndex')
    finally:
        ui.refresh()

def button_handler_menu_closed(msg_type, msg_value):
    global button_handler
    if msg_type == BUTTON_DOWN:
        if ui.menu.hidden:
            ui.menu.hidden = False
            ui.refresh()
    elif msg_type == BUTTON_UP:
        button_handler = button_handler_menu_open

def button_handler_menu_open(msg_type, msg_value):
    global button_handler
    if msg_type == BUTTON_DOWN_A:
        if not ui.menu.hidden:
            ui.menu.hidden = True
            ui.refresh()
    elif msg_type == BUTTON_DOWN_B:
        pass
    elif msg_type == BUTTON_DOWN_C:
        ui.menu.hidden = True
        ui.locations.hidden = False
        ui.refresh()
        button_handler = button_handler_pick_location
    elif msg_type == BUTTON_DOWN_D:
        if not ui.menu.hidden:
            ui.menu.hidden = True
            refresh()
    elif msg_type == BUTTON_UP:
        if msg_value != 'C':
            button_handler = button_handler_menu_closed

def button_handler_pick_location(msg_type, msg_value):
    global button_handler
    if msg_type == BUTTON_DOWN_B:
        devices.current_device = 2
        ui.locations.hidden = True
        button_handler = button_handler_menu_closed
        refresh()
    elif msg_type == BUTTON_DOWN_C:
        devices.current_device = 1
        ui.locations.hidden = True
        button_handler = button_handler_menu_closed
        refresh()
    elif msg_type == BUTTON_DOWN_D:
        devices.current_device = 0
        ui.locations.hidden = True
        button_handler = button_handler_menu_closed
        refresh()

button_handler = button_handler_menu_closed

for msg in MessagePump():
    msg_type, msg_value = msg

    if msg_type == DISPLAY_DATA:
        if ui.menu.hidden:
            refresh()
    else:
        button_handler(msg_type, msg_value)

# -----------------------

print("Done")
