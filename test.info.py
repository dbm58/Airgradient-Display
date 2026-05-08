import board
import time
import sys
import wifi
import socketpool
import adafruit_requests
import adafruit_connection_manager

from ui_base import UiBase
from data import info
from layout import Layout
from battery import Battery

ui = UiBase(board.DISPLAY)
ui.display.rotation = 0
ui.set_background()

layout = Layout()
group, widgets = layout.render(info)
ui.display.root_group.append(group)
widgets['board'].text = sys.implementation._machine
widgets['version'].text = ".".join(map(str,  filter(None, sys.implementation.version)))

bat = Battery()
alarm = ' !!!' if bat.charge_needed else ''
widgets['voltage'].text = str(bat.voltage) + alarm
widgets['ext-power'].text = str(bat.on_external_power)

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
radio = wifi.radio
ap_info = radio.ap_info
widgets['ssid'].text = str(ap_info.ssid)
widgets['address'].text = str(radio.addresses[0])
widgets['rssi'].text = str(ap_info.rssi)

ui.refresh()

while True:
    pass


