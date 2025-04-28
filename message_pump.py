import alarm
import board
from digitalio import DigitalInOut, Direction, Pull
import time

from battery import Battery

DISPLAY_DATA = 1
CHARGE_NEEDED = 2
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

class MessagePump:
    def __init__(self):
        attrs = { 'value': False, 'pull': True }
        self.pin_alarm_a = alarm.pin.PinAlarm(pin=board.BUTTON_A, **attrs)
        self.pin_alarm_b = alarm.pin.PinAlarm(pin=board.BUTTON_B, **attrs)
        self.pin_alarm_c = alarm.pin.PinAlarm(pin=board.BUTTON_C, **attrs)
        self.pin_alarm_d = alarm.pin.PinAlarm(pin=board.BUTTON_D, **attrs)
        self.alarms = (
            self.pin_alarm_a,
            self.pin_alarm_b,
            self.pin_alarm_c,
            self.pin_alarm_d
            )
        self.refresh_rate = 1 # 1 minute

        self.battery = Battery()

    def Button(self, pin):
        switch = DigitalInOut(pin)
        switch.direction = Direction.INPUT
        switch.pull = Pull.UP
        return switch

    def _debounce(self, pin):
        button = self.Button(pin)
        while not button.value:
            pass

    @property
    def time_alarm(self):
        next_update = time.monotonic() + (60 * self.refresh_rate)
        return alarm.time.TimeAlarm(monotonic_time=next_update)
        
    def __iter__(self):
        yield (DISPLAY_DATA, None)
        triggered_alarm = None
        while True:
            if self.battery.charge_needed:
                yield (CHARGE_NEEDED, self.battery.voltage)
            if isinstance(triggered_alarm, alarm.pin.PinAlarm):
                yield (BUTTON_DOWN, None)
                if triggered_alarm == self.pin_alarm_a:
                    yield (BUTTON_DOWN_A, None)
                    _debounce(board.BUTTON_A)
                    yield (BUTTON_UP_A, None)
                elif triggered_alarm == self.pin_alarm_b:
                    yield (BUTTON_DOWN_B, None)
                    _debounce(board.BUTTON_B)
                    yield (BUTTON_UP_B, None)
                elif triggered_alarm == self.pin_alarm_c:
                    yield (BUTTON_DOWN_C, None)
                    _debounce(board.BUTTON_C)
                    yield (BUTTON_UP_C, None)
                elif triggered_alarm == self.pin_alarm_d:
                    yield (BUTTON_DOWN_D, None)
                    _debounce(board.BUTTON_D)
                    yield (BUTTON_UP_D, None)
                yield (BUTTON_UP, None)
            elif isinstance(triggered_alarm, alarm.time.TimeAlarm):
                yield (DISPLAY_DATA, None)
            triggered_alarm = \
                alarm.light_sleep_until_alarms(*(self.alarms), self.time_alarm)
        
                
