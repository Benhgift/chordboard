import sys
sys.path.insert(0, '../')
import lib.maps
import lib.key_state_manager
import lib.hardware_button_handler
from pygame.locals import JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
from time import sleep
from importlib import reload

def pslp(x=''):
    print(x); sleep(.5)

def phlf(x=''):
    print(x); sleep(.25)

class Joystick:
    def set_vibration(self, val, val2):
        return

def pretty_tst():
    reload(lib.key_state_manager)
    reload(lib.hardware_button_handler)
    pslp('creating key_state_manager')
    ch = lib.key_state_manager.KeyStateManager(Joystick())

    b1 = Button(JOYHATMOTION, (1, 1), (1, 1))
    pslp('pressing dpad up')
    x = ch.convert_controller_event_to_keys(b1)[0]['letter']
    pslp('  output = ' + x)

    b1 = Button(JOYBUTTONDOWN, None, 0)
    pslp('pressing A')
    x = ch.convert_controller_event_to_keys(b1)[0]['letter']
    pslp('  output = ' + x)

    b1 = Button(JOYAXISMOTION, 50, .2)
    b1.axis = 0 
    pslp('pressing left stick up')
    ch.convert_controller_event_to_keys(b1)

    b1 = Button(JOYAXISMOTION, .2, .2)
    b1.axis = 2 
    pslp('pressing L2')
    x = ch.convert_controller_event_to_keys(b1)[0]['letter']
    pslp('  output = ' + x)

    b1 = Button(JOYAXISMOTION, .1, .1)
    b1.axis = 2 
    pslp('releasing L2')
    x = ch.convert_controller_event_to_keys(b1)[0]['letter']
    pslp('  output = ' + x)

    b1 = Button(JOYBUTTONUP, None, 0)
    pslp('releasing A')
    x = ch.convert_controller_event_to_keys(b1)[0]['letter']
    pslp('released letter = ' + str(x))

    b1 = Button(JOYAXISMOTION, 0, 0)
    b1.axis = 0 
    pslp('releasing left stick up')
    ch.convert_controller_event_to_keys(b1)

    b1 = Button(JOYAXISMOTION, .2, .2)
    b1.axis = 2 
    pslp('pressing L2')
    x = ch.convert_controller_event_to_keys(b1)[0]['letter']
    pslp('  output = ' + x)

    b1 = Button(JOYAXISMOTION, .1, .1)
    b1.axis = 2 
    pslp('releasing L2')
    x = ch.convert_controller_event_to_keys(b1)[0]['letter']
    pslp('  output = ' + x)

    b1 = Button(JOYHATMOTION, (0, 0), (0, 0))
    pslp('releasing dpad up')
    x = ch.convert_controller_event_to_keys(b1)[0]['letter']
    pslp('released ' + x)
    pslp()


def test_all():
    print()
    ch = lib.chorded.Chorded('hi')

    # basic key
    b1 = Button(JOYBUTTONDOWN, None, 0)
    assert(ch.convert_controller_event_to_keys(b1)['letter'] == 'e')
    b1 = Button(JOYBUTTONUP, None, 0)
    assert(ch.convert_controller_event_to_keys(b1)['letter'] == 'e')


class Button:
    def __init__(self, t=None, value=None, button=None):
        self.type = t
        self.value = value
        self.button = button
    


