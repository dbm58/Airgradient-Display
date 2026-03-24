import alarm
import board
from digitalio import DigitalInOut, Direction, Pull
import time
import wifi

from battery import Battery
battery = Battery()
from buttons import Buttons

DISPLAY_DATA = 1
CHARGE_NEEDED = 2
WIFI_DOWN = 3
BUTTON_DOWN = 10
BUTTON_UP = 11
BUTTON_DOWN_A = 12
BUTTON_DOWN_B = 13
BUTTON_DOWN_C = 14
BUTTON_DOWN_D = 15
BUTTON_UP_A = 16
BUTTON_UP_B = 17
BUTTON_UP_C = 18
BUTTON_UP_D = 19
PROGRAM_DONE = 99

def is_wifi_connected():
    # If we aren't associated with an AP, the connection is definitely down
    if wifi.radio.ap_info is None:
        print('ap info is none')
        return False
    # Double check we still have an IP
    if wifi.radio.ipv4_address is None:
        print('ipv4 address is none')
        return False
    print('wifi is connected')
    return True

class MessagePump:
    def __init__(self):
        self.buttons = Buttons()

        self.refresh_rate = 1 # 1 minute

    @property
    def time_alarm(self):
        next_update = time.monotonic() + (60 * self.refresh_rate)
        return alarm.time.TimeAlarm(monotonic_time=next_update)

    def __iter__(self):
        triggered_alarm = self.time_alarm
        while True:
            if battery.charge_needed:
                #  If the battery is flat:
                #  *  Send a message to the UI
                #  *  Sleep.  This lets the UI catch up, and provides a
                #     safety net so we don't get caught in a reboot loop
                #  *  Deep sleep.  This is close as we can get to shutting
                #     off the device
                #  To wake, reset the device after charging or connecting
                #  to USB
                yield (CHARGE_NEEDED, battery.voltage)
                time.sleep(5)
                alarm.exit_and_deep_sleep_until_alarms()
            elif not is_wifi_connected():
                yield (WIFI_DOWN, None)
                if is_wifi_connected():
                    continue
            elif isinstance(triggered_alarm, alarm.pin.PinAlarm):
                yield (BUTTON_DOWN, self.buttons.name(triggered_alarm))
                if triggered_alarm == self.buttons.pin_alarm_a:
                    yield (BUTTON_DOWN_A, None)
                    self.buttons.debounce(board.BUTTON_A)
                    yield (BUTTON_UP_A, None)
                elif triggered_alarm == self.buttons.pin_alarm_b:
                    yield (BUTTON_DOWN_B, None)
                    self.buttons.debounce(board.BUTTON_B)
                    yield (BUTTON_UP_B, None)
                elif triggered_alarm == self.buttons.pin_alarm_c:
                    yield (BUTTON_DOWN_C, None)
                    self.buttons.debounce(board.BUTTON_C)
                    yield (BUTTON_UP_C, None)
                elif triggered_alarm == self.buttons.pin_alarm_d:
                    yield (BUTTON_DOWN_D, None)
                    self.buttons.debounce(board.BUTTON_D)
                    yield (BUTTON_UP_D, None)
                yield (BUTTON_UP, self.buttons.name(triggered_alarm))
            elif isinstance(triggered_alarm, alarm.time.TimeAlarm):
                yield (DISPLAY_DATA, None)
            all_alarms = self.buttons.alarms + (self.time_alarm,)
            triggered_alarm = alarm.light_sleep_until_alarms(*(all_alarms))
