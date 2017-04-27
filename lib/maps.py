dpad_maps = { 'up': 'shift', 'down': 'control' }

modifiers = (
        'ls_up', 'ls_down', 'ls_left', 'ls_right',
        'rs_up', 'rs_down', 'rs_left', 'rs_right',
        )

sticky_modifiers = {
        # if no stick modifier given, it means any stick modifier
        ('dpad_up',): 'shift', 
        ('dpad_down',): 'ctrl', 
        ('rs_up', 'l2',): 'alt', 
        ('ls_right', 'rs_down', 'r2',): 'win',
        }

maps = {
        # if no stick modifier given, it means zeroed stick only
        ('rs_up', 'l1',): '?',
        ('rs_up', 'r1',): '\b',
        ('rs_up', 'r2',): '\t',

        ('rs_left', 'l1',): "'",
        ('rs_left', 'l2',): '_',
        ('rs_left', 'r1',): '"',
        ('rs_left', 'r2',): '-',

        ('rs_right', 'l1',): '[',
        ('rs_right', 'l2',): '{',
        ('rs_right', 'r1',): ']',
        ('rs_right', 'r2',): '}',

        ('rs_down', 'l1',): ';',
        ('rs_down', 'l2',): '<',
        ('rs_down', 'r1',): ':',
        ('rs_down', 'r2',): '>',

        ('ls_up', 'rs_up', 'l1',): '1',
        ('ls_up', 'rs_up', 'l2',): '2',
        ('ls_up', 'rs_up', 'r1',): '3',
        ('ls_up', 'rs_up', 'r2',): '4',
        ('ls_up', 'rs_right', 'l1',): '5',
        ('ls_up', 'rs_right', 'l2',): '6',
        ('ls_up', 'rs_right', 'r1',): '7',
        ('ls_up', 'rs_right', 'r2',): '8',
        ('ls_up', 'rs_left', 'l1',): '9',
        ('ls_up', 'rs_left', 'l2',): '0',

        ('ls_right', 'rs_up', 'l1',): '=',
        ('ls_right', 'rs_up', 'l2',): '+',
        ('ls_right', 'rs_up', 'r1',): '*',
        ('ls_right', 'rs_up', 'r2',): '#',
        ('ls_right', 'rs_right', 'l1',): '$',
        ('ls_right', 'rs_right', 'l2',): '%',
        ('ls_right', 'rs_right', 'r1',): '^',
        ('ls_right', 'rs_right', 'r2',): '&',
        ('ls_right', 'rs_left', 'l1',): '@',
        ('ls_right', 'rs_left', 'l2',): '~',
        ('ls_right', 'rs_left', 'r1',): '/',
        ('ls_right', 'rs_left', 'r2',): '\\',
        ('ls_right', 'rs_down', 'l1',): '`',
        ('ls_right', 'rs_down', 'l2',): '|',
        ('ls_right', 'rs_down', 'r1',): '!',
        ('ls_right', 'rs_down', 'r2',): 'win',

        ('ls_left', 'rs_up', 'l1',): 'f1',
        ('ls_left', 'rs_up', 'l2',): 'f2',
        ('ls_left', 'rs_up', 'r1',): 'f3',
        ('ls_left', 'rs_up', 'r2',): 'f4',
        ('ls_left', 'rs_right', 'l1',): 'f5',
        ('ls_left', 'rs_right', 'l2',): 'f6',
        ('ls_left', 'rs_right', 'r1',): 'f7',
        ('ls_left', 'rs_right', 'r2',): 'f8',
        ('ls_left', 'rs_left', 'l1',): 'f9',
        ('ls_left', 'rs_left', 'l2',): 'f10',
        ('ls_left', 'rs_left', 'r1',): 'f11',
        ('ls_left', 'rs_left', 'r2',): 'f12',
        ('ls_left', 'rs_down', 'r2',): 'esc',

        ('a',): 'e',
        ('b',): 't',
        ('l1',): 'h',
        ('l2',): 'n',
        ('r1',): 'i',
        ('r2',): ' ',

        ('ls_up', 'a'): 's',
        ('ls_up', 'b'): 'a',
        ('ls_up', 'l1'): 'l',
        ('ls_up', 'l2'): 'o',
        ('ls_up', 'r1'): 'r',
        ('ls_up', 'r2'): 'd',

        ('ls_right', 'a'): 'p',
        ('ls_right', 'b'): 'c',
        ('ls_right', 'l1'): 'm',
        ('ls_right', 'l2'): 'u',
        ('ls_right', 'r1'): 'f',
        ('ls_right', 'r2'): 'b',

        ('ls_left', 'a'): 'g',
        ('ls_left', 'b'): 'y',
        ('ls_left', 'l1'): 'x',
        ('ls_left', 'l2'): 'k',
        ('ls_left', 'r1'): 'w',
        ('ls_left', 'r2'): 'v',

        ('ls_down', 'a'): 'j',
        ('ls_down', 'b'): '\n',
        ('ls_down', 'l1'): '.',
        ('ls_down', 'l2'): '(',
        ('ls_down', 'r1'): ',',
        ('ls_down', 'r2'): ')',
    }

