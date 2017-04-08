from operator import attrgetter
import platform

import pygame
from pygame.locals import *

from lib import xinput
from lib.chorded import Chorded

__version__ = '1.0.0'
__vernum__ = tuple([int(s) for s in __version__.split('.')])

class Struct(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)
        self.__dict__.update(**kwargs)


def draw_button(button):
    rect = button.rect
    value = 0 if button.value else 1
    pygame.draw.rect(screen, white, rect, value)


def draw_stick(stick):
    ox, oy = origin = stick.rect.center
    radius = stick.rect.h
    x, y = int(round(ox + stick.x * radius)), int(round(oy + stick.y * radius))
    pygame.draw.circle(screen, white, origin, radius, 1)
    pygame.draw.circle(screen, red, (x, y), 5, 0)


def draw_trigger(trigger):
    rect = trigger.rect
    pygame.draw.rect(screen, white, rect, 1)
    if trigger.value > 0.0:
        r = rect.copy()
        r.h = rect.h * trigger.value
        r.bottom = rect.bottom
        screen.fill(white, r)


def draw_hats(hats):
    pygame.draw.circle(screen, white, hats[0, 0].rect.center, 40, 1)
    for hat in hats.values():
        if hat.value:
            pygame.draw.rect(screen, white, hat.rect, 0)
    pygame.draw.rect(screen, white, hats[0, 0].rect, 1)


def stick_center_snap(value, snap=0.2):
    # Feeble attempt to compensate for calibration and loose stick.
    if value >= snap or value <= -snap:
        return value
    else:
        return 0.0


pygame.init()
pygame.joystick.init()

# Initialize a joystick object: grabs the first joystick
PLATFORM = platform.uname()[0].upper()
WINDOWS_PLATFORM = PLATFORM == 'WINDOWS'
WINDOWS_XBOX_360 = False
JOYSTICK_NAME = ''
joysticks = xinput.XInputJoystick.enumerate_devices()
device_numbers = list(map(attrgetter('device_number'), joysticks))
joystick = None
if device_numbers:
    joystick = pygame.joystick.Joystick(device_numbers[0])
    JOYSTICK_NAME = joystick.get_name().upper()
    print('Joystick: {} using "{}" device'.format(PLATFORM, JOYSTICK_NAME))
    if 'XBOX 360' in JOYSTICK_NAME and WINDOWS_PLATFORM:
        WINDOWS_XBOX_360 = True
        joystick = xinput.XInputJoystick(device_numbers[0])
        print('Using xinput.XInputJoystick')
    else:
        # put other logic here for handling platform + device type in the event loop
        print('Using pygame joystick')
        joystick.init()

#screen = pygame.display.set_mode((640, 480))
#screen_rect = screen.get_rect()
clock = pygame.time.Clock()
black = Color('black')
white = Color('white')
red = Color('red')

# button display
button_a = Struct(rect=Rect(560, 200, 20, 20), value=0)
button_b = Struct(rect=Rect(600, 160, 20, 20), value=0)
button_x = Struct(rect=Rect(520, 160, 20, 20), value=0)
button_y = Struct(rect=Rect(560, 120, 20, 20), value=0)
button_left_bumper = Struct(rect=Rect(40, 80, 40, 20), value=0)
button_right_bumper = Struct(rect=Rect(560, 80, 40, 20), value=0)
button_back = Struct(rect=Rect(240, 160, 20, 20), value=0)
button_start = Struct(rect=Rect(400, 160, 20, 20), value=0)
button_left_stick = Struct(rect=Rect(60, 160, 20, 20), value=0)
button_right_stick = Struct(rect=Rect(400, 240, 20, 20), value=0)
buttons = (
    button_a, button_b, button_x, button_y,
    button_left_bumper, button_right_bumper,
    button_back, button_start,
    button_left_stick, button_right_stick)

# stick display
left_stick = Struct(rect=Rect(0, 0, 80, 40), x=0.0, y=0.0)
right_stick = Struct(rect=Rect(0, 0, 40, 40), x=0.0, y=0.0)
left_stick.rect.center = button_left_stick.rect.center
right_stick.rect.center = button_right_stick.rect.center

# trigger display
left_trigger = Struct(rect=Rect(40, 40, 40, 40), value=0.0)
right_trigger = Struct(rect=Rect(560, 40, 40, 40), value=0.0)

# hat display
# arrangement:
# (-1,  1)    (0,  1)    (1,  1)
# (-1,  0     (0,  0)    (1,  0)
# (-1, -1)    (0, -1)    (1, -1)
hats = {}
hat_posx = {-1: 0, 0: 20, 1: 40}
hat_posy = {1: 0, 0: 20, -1: 40}
for y in 1, 0, -1:
    for x in -1, 0, 1:
        hats[x, y] = Struct(rect=Rect(220 + hat_posx[x], 220 + hat_posy[y], 20, 20), value=0)
which_hat = None  # save state

max_fps = 60
chorded = Chorded()

while True:
    clock.tick(max_fps)
    if WINDOWS_XBOX_360:
        joystick.dispatch_events()

    for e in pygame.event.get():
        chorded.process_button(e)
        if e.type == QUIT:
            quit()

    # draw the controls
    #screen.fill(black)
    #for button in buttons:
    #    draw_button(button)
    #draw_stick(left_stick)
    #draw_stick(right_stick)
    #draw_trigger(left_trigger)
    #draw_trigger(right_trigger)
    #draw_hats(hats)
    #pygame.display.flip()
