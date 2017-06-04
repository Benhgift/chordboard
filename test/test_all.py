import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import lib.maps
import lib.key_state_manager
import lib.hardware_button_handler
from pygame.locals import JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
from time import sleep
from importlib import reload


def test_everything():
    reload(lib.key_state_manager)
    reload(lib.hardware_button_handler)
    ch = lib.key_state_manager.KeyStateManager(Joystick())

    b1 = Button(JOYHATMOTION, (1, 1), (1, 1))
    # dpad up
    assert(letter(ch, b1) == 'shift')

    b1 = Button(JOYBUTTONDOWN, None, 0)
    # A down
    assert(letter(ch, b1) == 'e')

    b1 = Button(JOYAXISMOTION, 50, .2)
    b1.axis = 0
    # left stick up
    ch.convert_controller_event_to_keys(b1)

    b1 = Button(JOYAXISMOTION, .2, .2)
    b1.axis = 2
    # L2 down
    assert(letter(ch, b1) == 'o')

    b1 = Button(JOYAXISMOTION, .1, .1)
    b1.axis = 2
    # L2 up
    assert(letter(ch, b1) == 'o')

    b1 = Button(JOYBUTTONUP, None, 0)
    # A up
    assert(letter(ch, b1) == 'e')

    b1 = Button(JOYAXISMOTION, 0, 0)
    b1.axis = 0
    # left stick up
    ch.convert_controller_event_to_keys(b1)

    b1 = Button(JOYAXISMOTION, .2, .2)
    b1.axis = 2
    # L2 down
    assert(letter(ch, b1) == 'n')

    b1 = Button(JOYAXISMOTION, .1, .1)
    b1.axis = 2
    # L2 up
    assert(letter(ch, b1) == 'n')

    b1 = Button(JOYHATMOTION, (0, 0), (0, 0))
    # dpad-up up
    assert(letter(ch, b1) == 'shift')


def test_double_shift_lock():
    ch = lib.key_state_manager.KeyStateManager(Joystick())
    print()

    # dpad up tap
    b1 = Button(JOYHATMOTION, (1, 1), (1, 1))
    assert(letter(ch, b1) == 'shift')
    b1 = Button(JOYHATMOTION, (0, 0), (0, 0))
    ch.convert_controller_event_to_keys(b1)

    b1 = Button(JOYBUTTONDOWN, None, 0)
    # A down
    assert(letter(ch, b1) == 'e')

    b1 = Button(JOYBUTTONUP, None, 0)
    # A up
    ch.convert_controller_event_to_keys(b1)


class Button:
    def __init__(self, t=None, value=None, button=None):
        self.type = t
        self.value = value
        self.button = button


class Joystick:
    def set_vibration(self, val, val2):
        return


def letter(ch, b1):
    return ch.convert_controller_event_to_keys(b1)[0]['letter']


