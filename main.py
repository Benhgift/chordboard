import platform
import pygame
from lib import xinput
from lib.key_state_manager import KeyStateManager
from pyautogui import keyDown, keyUp

pygame.init()
pygame.joystick.init()

# Initialize a joystick object: grabs the first joystick
_platform = platform.uname()[0].upper()
windows_platform = _platform == 'WINDOWS'
windows_xbox_360 = False
joystick_name = ''
joysticks = xinput.XInputJoystick.enumerate_devices()
device_numbers = [x.device_number for x in joysticks]
joystick = None
if device_numbers:
    joystick = pygame.joystick.Joystick(device_numbers[0])
    joystick_name = joystick.get_name().upper()
    print('joystick: {} using "{}" device'.format(platform, joystick_name))
    if 'XBOX' in joystick_name and windows_platform:
        windows_xbox_360 = True
        joystick = xinput.XInputJoystick(device_numbers[0])
        print('Using xinput.XInputJoystick')
    else:
        # put other logic here for handling platform + device type in the event loop
        print('Using pygame joystick')
        joystick.init()

clock = pygame.time.Clock()

max_fps = 60
chorded = KeyStateManager(joystick)

while True:
    clock.tick(max_fps)
    joystick.dispatch_events()

    for e in pygame.event.get():
        keys = chorded.convert_controller_event_to_keys(e)
        if not keys:
            continue
        for key in keys:
            if not key:
                print(keys)
                continue
            letter = key['letter']
            if key['direction'] == 'down':
                #print(letter, 'down')
                keyDown(letter)
            elif key['direction'] == 'up':
                #print(letter, 'up')
                keyUp(letter)
