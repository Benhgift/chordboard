import pygame
from pygame.locals import *


class Chorded:
    def __init__(self):
        self.hats = {}
        self.which_hat = None  # save state
        self.poop = None
        self.buttons = {
                'a':0,
                }

    def _handle_analog(self, e):
        pass

    def process_button(self, e):
        #print('event: {}'.format(pygame.event.event_name(e.type)))
        if e.type == JOYAXISMOTION:
            print('JOYAXISMOTION: axis {}, value {}'.format(e.axis, e.value))
            if e.axis == 2:
                # left _trigger
                pass
            elif e.axis == 5:
                # right _trigger
                pass
            elif e.axis == 0:
                # left stick y
                pass
            elif e.axis == 1:
                # left stick x
                pass
            elif e.axis == 3:
                # right stick y
                pass
            elif e.axis == 4:
                # right stick x
                pass
        elif e.type == JOYBUTTONDOWN:
            print('JOYBUTTONDOWN: button {}'.format(e.button))
        elif e.type == JOYBUTTONUP:
            print('JOYBUTTONUP: button {}'.format(e.button))
        elif e.type == JOYHATMOTION:
            # pygame sends this; xinput sends a button instead--the handler converts the button to a hat event
            #print('JOYHATMOTION: joy {} hat {} value {}'.format(e.joy, e.hat, e.value))
            if self.which_hat:
                self.hats[self.which_hat] = 0
            if e.value != (0, 0):
                self.which_hat = e.value
                self.hats[self.which_hat] = 1
            print(self.hats)
