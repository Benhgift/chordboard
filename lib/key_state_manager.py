from lib.maps import maps, modifiers, sticky_modifiers
from lib.hardware_button_handler import HardwareButtonHandler


class KeyStateManager:
    def __init__(self, joystick):
        self.hardwareButtonHandler = HardwareButtonHandler(joystick)
        self.maps = {tuple(sorted(x)): y for x, y in maps.items()}
        self.letter_to_combo_maps = {y: x for x, y in self.maps.items()}
        self.sticky_mods = self._insert_sticks_into_sticky_mods(sticky_modifiers)
        self.sticky_mods = {tuple(sorted(x)): y for x, y in self.sticky_mods.items()}
        self.button_numbers = {0: 'a', 1: 'b', 2: 'x', 3: 'y', 4: 'l1', 5: 'r1', 6: 'select', 7: 'start', 8: 'l3',
                               9: 'r3', 10: 'l2', 11: 'r2', }
        self.buttons = {'a': 0, 'b': 0, 'x': 0, 'y': 0, 'l1': 0, 'l2': 0, 'l3': 0, 'r1': 0, 'r2': 0, 'r3': 0,
                        'ls': 'none', 'rs': 'none', 'dpad': 'none', 'start': 0, 'select': 0, }

        self.active_keys = []
        self.held_buttons = []
        self.held_letters = []

        self.modifiers = {'alt': 0, 'shift': 0, 'ctrl': 0, 'win': 0}
        self.activated_but_not_used = {'shift': False, 'ctrl': False}

    def convert_controller_event_to_keys(self, e):
        output = []
        # down_b = a str button like 'dpad_left' 
        down_b, up_b = self.hardwareButtonHandler.handle_hardware_button(e)
        if down_b:
            output += self.handle_button_down(down_b)
        if up_b:
            output += self.handle_button_up(up_b)
        return output

    def handle_button_down(self, button):
        self._record_that_button_is_down(button)
        letter = self._get_sticky_mod_to_print()
        if not letter:
            letter = self._get_letter_to_print()
        if not letter:
            return []
        self._record_held_letter(letter)
        self._wipe_active_keys()
        return [{'letter': letter, 'direction': 'down'}]

    def handle_button_up(self, button):
        self._try_remove_active(button)
        self._try_remove_held_button(button)
        self.buttons[button] = 0
        # we need to figure out which letter will be invalidated by this button up event
        letter = self._get_invalid_letter()
        if not letter:
            return []
        if letter in self.modifiers:
            letter = self._process_sticky_mod(letter)
        self.held_letters = [x for x in self.held_letters if x['letter'] != letter]
        return [{'letter': letter, 'direction': 'up'}]

    def _insert_sticks_into_sticky_mods(self, sticky_mods):
        output = sticky_mods.copy()
        directions = ['left', 'right', 'up', 'down']
        for combo, key in sticky_mods.items():
            rs_exists, ls_exists = self._get_ls_rs_existence(combo)
            if not rs_exists:
                for direction in directions:
                    new_combo = ('rs_' + direction,) + combo
                    output[new_combo] = key
            if not ls_exists:
                for direction in directions:
                    new_combo = ('ls_' + direction,) + combo
                    output[new_combo] = key
        return output

    def _try_remove_active(self, button):
        try:
            self.active_keys.remove(button)
        except:
            pass

    def _handle_modifiers(self, letter):
        # take all stick modifiers out (from maps.modifiers) and see if there's a match (dpad up?)
        # put them back and see if there's a match
        output = [letter]
        mod = self._get_target_from_maps(self.sticky_mods)
        mods_to_output = []
        # if mod:
        #    self.activated_but_not_used[mod] = True
        #    self.modifiers[mod] = 1
        for x in self.sticky_mods:
            # remove the mods that aren't pressed
            pass
        # if letter:
        #    actives = []
        #    for _mod, active in self.activated_but_not_used.items():
        #        if active:
        #            actives += [_mod]
        #        self.activated_but_not_used[_mod] = False

        # all these will be removed..?
        if letter:
            if letter in self.modifiers:
                self.modifiers[letter] = 1
                self.activated_but_not_used[letter] = True
                return []
            if letter.isalpha() and self.modifiers['shift']:
                if self.buttons['dpad'] == 'up' or self.activated_but_not_used['shift']:
                    output[0] = letter.upper()
                    self.activated_but_not_used['shift'] = False
                if self.buttons['dpad'] != 'up':
                    self.modifiers['shift'] = 0

            if self.modifiers['ctrl']:
                if self.buttons['dpad'] == 'down' or self.activated_but_not_used['ctrl']:
                    output = ['ctrl'] + output
                    self.activated_but_not_used['ctrl'] = False
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

    def _get_target_from_maps(self, maps):
        try:
            target = maps[tuple(sorted(self.active_keys))]
        except:
            target = None
        return target

    def _get_letter_to_print(self):
        return self._get_target_from_maps(self.maps)

    def _record_that_button_is_down(self, button):
        self.buttons[button] = 1
        self.active_keys += [button]
        self.held_buttons += [button]

    def _record_held_letter(self, letter):
        mapping = [x for x in self.active_keys if x not in modifiers]
        self.held_letters += [{'letter': letter, 'mapping': mapping}]

    @staticmethod
    def _get_ls_rs_existence(combo):
        rs_exists = False
        ls_exists = False
        for key in combo:
            if 'rs_' in key:
                rs_exists = True
            if 'ls_' in key:
                ls_exists = True
        return rs_exists, ls_exists

    def _get_sticky_mod_to_print(self):
        return self._get_target_from_maps(self.sticky_mods)

    def _get_invalid_letter(self):
        for letter in self.held_letters:
            for button in letter['mapping']:
                if button in modifiers:
                    # skip because we want to still be holding a button down even if the user stops holding down that analog direction
                    continue
                if button not in self.held_buttons:
                    return letter['letter']

    def _try_remove_held_button(self, button):
        try:
            self.held_buttons.remove(button)
        except:
            pass

    def _try_remove(self, _list, item):
        try:
            _list.remove(item)
        except:
            pass

    def _process_sticky_mod(self, mod):
        # do some key_up logic for sticky mods here and maybe don't return anything
        return mod
