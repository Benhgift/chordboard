import lib.maps
import lib.chorded
from pygame.locals import *


def test_all():
    print()
    ch = lib.chorded.Chorded('hi')

    # basic key
    e = Button(JOYBUTTONDOWN, None, 0)
    assert(ch.process_button(e) == ['e'])

    dpad_up = Button(JOYHATMOTION, (0, 1), None)
    dpad_none = Button(JOYHATMOTION, (0, 0), None)
    # hold shift
    ch.process_button(dpad_up) 
    assert(ch.process_button(e) == ['E'])
    ch.process_button(dpad_none) 
    assert(ch.process_button(e) == ['e'])

    # tap shift twice to disable
    ch.process_button(dpad_up) 
    ch.process_button(dpad_none) 
    ch.process_button(dpad_up) 
    ch.process_button(dpad_none) 
    assert(ch.process_button(e) == ['e'])
    # and once for one E
    ch.process_button(dpad_up) 
    ch.process_button(dpad_none) 
    assert(ch.process_button(e) == ['E'])
    assert(ch.process_button(e) == ['e'])
    assert(ch.process_button(e) == ['e'])


class Button:
    def __init__(self, t=None, value=None, button=None):
        self.type = t
        self.value = value
        self.button = button
    


