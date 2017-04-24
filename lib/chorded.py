import pygame
import time
import threading
from datetime import timedelta
from lib.maps import maps, dpad_maps, modifiers
from threading import Thread, Lock
from math import atan2, pi
from pygame.locals import *


class Chorded:
    def __init__(self, joystick):
        self.joystick = joystick
        self.hats = {}
        self.which_hat = None  # save state
        self.maps = {tuple(sorted(x)):y for x, y in maps.items()}
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
                'l3':0,
                'r1':0,
                'r2':0,
                'r3':0,
                'ls':'none',
                'rs':'none',
                'dpad':'none',
                'start':0,
                'select':0,
                }
        self.active_keys = []
        self.modifiers = {'alt':0, 'shift':0, 'ctrl':0}
        self.triggered = self.modifiers.copy()
        self._lx = 0
        self._ly = 0
        self._rx = 0
        self._ry = 0
        self.start_time = time.time()

    def _check_no_magnitude(self, magnitude, stick):
        current = self.buttons[stick]
        if magnitude < 40:
            if current != 'none':
                self._try_remove_active(stick + '_' + current)
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

    def _try_remove_active(self, key):
        try: 
            self.active_keys.remove(key)
        except:
            pass

    def _set_direction(self, direction, stick):
        current = self.buttons[stick]
        if current != direction:
            self.buttons[stick] = direction
            self.async_vib()
            if current != 'none':
                self._try_remove_active(stick + '_' + current)
            self.active_keys.append(stick + '_' + direction)

    def _get_direction(self, directions, angle):
        for direction, direction_fn in directions.items():
            if direction_fn(angle):
                return direction

    def handle_analog(self, x, y, stick):
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

    def handle_modifiers(self, letter):
        output = [letter]
        if letter:
            if letter in self.modifiers:
                self.modifiers[letter] = 1
                return []
            if letter.isalpha() and self.modifiers['shift']:
                output[0] = letter.upper()
                print(self.buttons['dpad'])
                if self.buttons['dpad'] != 'up':
                    self.modifiers['shift'] = 0
            if self.modifiers['ctrl']:
                output = ['ctrl'] + output
                if self.buttons['dpad'] != 'down':
                    self.modifiers['ctrl'] = 0
            if self.modifiers['alt']:
                output = ['alt'] + output
                if self.buttons['rs'] != 'up':
                    if not self.buttons['l1']:
                        self.modifiers['alt'] = 0
        else:
            return []
        return output

    def _wipe_active_keys(self):
        for key in self.active_keys:
            if key not in modifiers:
                self._try_remove_active(key)

    def _get_letter_to_print(self):
        try:
            letter = self.maps[tuple(sorted(self.active_keys))]
        except:
            letter = None
        return letter

    def handle_button_down(self, button_num):
        button = self.button_numbers[button_num]
        self.buttons[button] = 1
        self.active_keys += [button]
        letter = self._get_letter_to_print()
        self._wipe_active_keys()
        return self.handle_modifiers(letter)

    def handle_button_up(self, button_num):
        button = self.button_numbers[button_num]
        self._try_remove_active(button)
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
                self.handle_analog(self._lx, self._ly, 'ls')
            elif e.axis == 1:
                self._lx = e.value
                self.handle_analog(self._lx, self._ly, 'ls')
            elif e.axis == 3:
                self._ry = e.value
                self.handle_analog(self._rx, self._ry, 'rs')
            elif e.axis == 4:
                self._rx = e.value
                self.handle_analog(self._rx, self._ry, 'rs')
        elif e.type == JOYBUTTONDOWN:
            return self.handle_button_down(e.button)
        elif e.type == JOYBUTTONUP:
            self.handle_button_up(e.button)
        elif e.type == JOYHATMOTION:
            if self.which_hat:
                self.hats[self.which_hat] = 0
            if e.value != (0, 0):
                self.which_hat = e.value
            if e.value[1] == 1:
                self.buttons['dpad'] = 'up'
                self.modifiers['shift'] = 1
            elif e.value[1] == -1:
                self.buttons['dpad'] = 'down'
                self.modifiers['ctrl'] = 1
            else:
                self.buttons['dpad'] = 'none'

