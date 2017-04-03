import pdir
import time
from inputs import devices, get_gamepad

for device in devices.gamepads:
    print(device)
print("number of devices = " + str(len(devices.gamepads)))

def print_event(event):
    print(event.ev_type, end='  |  ')
    print(event.code, end='   |   ')
    print(event.state)

gamepad = devices.gamepads[0]

class ChordedKeyboard:
    def __init__(self):
        self.buttons = {
            'BTN_NORTH':0,
            'BTN_EAST':0,
            'BTN_SOUTH':0,
            'BTN_WEST':0
        }

    def process_event(self, event):
        if event.code in self.buttons:
            self.buttons[event.code] = event.state
            print(self.buttons[event.code])

        print_event(event)

while True:
    events = gamepad.read()
    chorded_keyboard = ChordedKeyboard()

    if events[0].ev_type == '':
        pass
    for event in events:
        if event.ev_type in ['Key', 'Absolute']:
            chorded_keyboard.process_event(event)

