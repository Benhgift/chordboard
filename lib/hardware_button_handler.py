import threading
import time
from pygame.locals import JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
from math import atan2, pi


class HardwareButtonHandler:
    def __init__(self, joystick):
        self.joystick = joystick
        self.button_numbers = {0: 'a', 1: 'b', 2: 'x', 3: 'y', 4: 'l1', 5: 'r1', 6: 'select', 7: 'start', 8: 'l3',
                               9: 'r3', 10: 'l2', 11: 'r2', }
        self.dpad = 'none'
        self.triggers = {10: None, 11: None}

        self.stick_nums = {0: 'ls', 1: 'ls', 3: 'rs', 4: 'rs'}
        self.x_y_num_map = {0: 'y', 1: 'x', 3: 'y', 4: 'x'}
        self.stick_direction = {'ls': None, 'rs': None}
        self.stick_vals = {'ls': {'x': 0, 'y': 0}, 'rs': {'x': 0, 'y': 0}}
        self.start_time = time.time

    def handle_hardware_button(self, event):
        down_b, up_b = None, None
        if event.type == JOYAXISMOTION:
            down_b, up_b = self._handle_axis_motion(event)
        if event.type == JOYBUTTONDOWN:
            down_b = self.button_numbers[event.button]
        elif event.type == JOYBUTTONUP:
            up_b = self.button_numbers[event.button]
        elif event.type == JOYHATMOTION:
            down_b, up_b = self._handle_dpad(event.value)
        return down_b, up_b

    def _handle_axis_motion(self, e):
        if e.axis == 2:
            # l2
            return self.handle_triggers(10, e.value)
        elif e.axis == 5:
            # r2
            return self.handle_triggers(11, e.value)
        else:
            stick = self.stick_nums[e.axis]  # = 'ls' or 'rs'
            x_or_y = self.x_y_num_map[e.axis]
            self.stick_vals[stick][x_or_y] = e.value
            x = self.stick_vals[stick]['x']
            y = self.stick_vals[stick]['y']
            return self.handle_analog(x, y, stick)

    def handle_analog(self, x, y, stick):
        down_b, up_b = None, None
        angle = atan2(y, x) / pi
        magnitide = (x * 10) ** 2 + (y * 10) ** 2
        if self._check_no_magnitude(magnitide, stick):
            if self.stick_direction[stick]:
                up_b = stick + '_' + self.stick_direction[stick]
            self.stick_direction[stick] = None
            return down_b, up_b
        directions = {
            'right': lambda angle: -.25 < angle <= .25,
            'up': lambda angle: .25 < angle <= .75,
            'left': lambda angle: .75 < angle or angle <= -.75,
            'down': lambda angle: -.75 < angle <= -.25,
        }
        current_direction = self._get_direction(directions, angle)
        down_b, up_b = self._set_direction(current_direction, stick)
        return down_b, up_b

    def _set_direction(self, new_direction, stick):
        down_b, up_b = None, None
        current = self.stick_direction[stick]
        if current != new_direction:
            self.stick_direction[stick] = new_direction
            self.async_vib()
            if current:
                up_b = stick + '_' + current
            print()
            print(stick)
            print(current)
            print(new_direction)
            down_b = stick + '_' + new_direction
        return down_b, up_b

    def _get_direction(self, directions, angle):
        for direction, direction_fn in directions.items():
            if direction_fn(angle):
                return direction

    def handle_triggers(self, trigger_num, value):
        down_b, up_b = None, None
        trigger_state = self.triggers[trigger_num]
        trigger = self.button_numbers[trigger_num]
        if value > .1:
            if not trigger_state:
                self.triggers[trigger_num] = 'on'
                down_b = trigger
        else:
            if trigger_state:
                self.triggers[trigger_num] = None
                up_b = trigger
        return down_b, up_b

    def _check_no_magnitude(self, magnitude, stick):
        if magnitude < 40:
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

    def _handle_dpad(self, value):
        down_b, up_b = None, None
        if value[1] == 1:
            up_b = self._handle_up('down')
            self.dpad = 'up'
            down_b = 'dpad_up'
        elif value[1] == -1:
            up_b = self._handle_up('up')
            self.dpad = 'down'
            down_b = 'dpad_down'
        else:
            if self.dpad != 'none':
                up_b = 'dpad_' + self.dpad
            self.dpad = 'none'
        return down_b, up_b

    def _handle_up(self, button):
        if self.dpad == button:
            return button
        return None
