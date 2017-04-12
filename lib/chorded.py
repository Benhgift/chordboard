import pygame
import time
import threading
from datetime import timedelta
from lib.maps import maps
from threading import Thread, Lock
from math import atan2, pi
from pygame.locals import *


class Chorded:
    def __init__(self, joystick):
        self.joystick = joystick
        self.hats = {}
        self.which_hat = None  # save state
        self.poop = None
        self.button_numbers = {
                0:'a',
                1:'b',
                2:'x',
                3:'y',
                4:'l1',
                5:'r1',
                6:'select',
                7:'start',
                8:'l3',
                9:'r3',
                10:'l2',
                11:'r2',
                }
        self.buttons = {
                'a':0,
                'b':0,
                'x':0,
                'y':0,
                'l1':0,
                'l2':0,
                'r1':0,
                'r2':0,
                'ls':'none',
                'l3':0,
                'rs':'none',
                'r3':0,
                'dpad':'none',
                'start':0,
                'select':0,
                }
        self._lx = 0
        self._ly = 0
        self._rx = 0
        self._ry = 0
        self.start_time = time.time()

    def _check_no_magnitude(self, magnitude, stick):
        if magnitude < 40:
            self.buttons[stick] = 'none'
            return True
        return False

    def async_vib(self):
        def vibe(joystick):
            start_time = time.time()
            self.start_time = start_time
            joystick.set_vibration(.5, .5)
            time.sleep(.1)
            if self.start_time == start_time:
                joystick.set_vibration(0, 0)

        t = threading.Thread(target=vibe, args=(self.joystick,))
        t.start()

    def _set_direction(self, direction, stick):
        if self.buttons[stick] != direction:
            self.buttons[stick] = direction
            self.async_vib()

    def _get_direction(self, directions, angle):
        for direction, direction_fn in directions.items():
            if direction_fn(angle):
                return direction

    def _handle_analog(self, x, y, stick):
        angle = atan2(y, x) / pi
        magnitide = (x*10)**2 + (y*10)**2
        if self._check_no_magnitude(magnitide, stick): return 
        directions = {
                'right' : lambda angle: -.25 < angle < .25,
                'up' : lambda angle: .25 < angle < .75,
                'left' : lambda angle: angle > .75 or angle < -.75,
                'down' : lambda angle: -.75 < angle < -.25,
            }
        current_direction = self._get_direction(directions, angle)
        self._set_direction(current_direction, stick)

    def handle_button_down(self, button_num):
        button = self.button_numbers[button_num]
        self.buttons[button] = 1
        target_letters = maps[self.buttons['ls']]
        letter = target_letters[button]
        return letter

    def handle_button_up(self, button_num):
        button = self.button_numbers[button_num]
        self.buttons[button] = 0

    def handle_triggers(self, trigger_num, value):
        if value > .1:
            if self.buttons[self.button_numbers[trigger_num]] != 1:
                return self.handle_button_down(trigger_num)
        else:
            if self.buttons[self.button_numbers[trigger_num]] != 0:
                return self.handle_button_up(trigger_num)

    def process_button(self, e):
        if e.type == JOYAXISMOTION:
            if e.axis == 2:
                # l2
                return self.handle_triggers(10, e.value)
            elif e.axis == 5:
                # r2
                return self.handle_triggers(11, e.value)
            elif e.axis == 0:
                self._ly = e.value
                self._handle_analog(self._lx, self._ly, 'ls')
            elif e.axis == 1:
                self._lx = e.value
                self._handle_analog(self._lx, self._ly, 'ls')
            elif e.axis == 3:
                self._ry = e.value
                self._handle_analog(self._rx, self._ry, 'rs')
            elif e.axis == 4:
                self._rx = e.value
                self._handle_analog(self._rx, self._ry, 'rs')
        elif e.type == JOYBUTTONDOWN:
            return self.handle_button_down(e.button)
        elif e.type == JOYBUTTONUP:
            self.handle_button_up(e.button)
        elif e.type == JOYHATMOTION:
            if self.which_hat:
                self.hats[self.which_hat] = 0
            if e.value != (0, 0):
                self.which_hat = e.value
                self.hats[self.which_hat] = 1
