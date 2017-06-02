[![Build Status](https://api.travis-ci.org/Benhgift/chordboard.svg?branch=master)](https://travis-ci.org/Benhgift/chordboard)


# Chordboard

Be able to touch type using Xbox (done) and Oculus Touch (not done)

Currently there's no solution for touch typing with a controller of any kind. 

# Quickstart

* Install pygame from http://www.pygame.org/download.shtml
* `pip install pyautogui`
* With an Xbox controller plugged in: `python3 main.py`
* Reference `lib/maps.py` for which button combos map to which letters

# Current goal 5/22

Fix how modifier keys are handled (tapping the button for 'shift' should leave it on till used)

# How it works

1. `main.py` initializes the Xbox controller and starts listening for input
2. Input is passed to `lib/chorded` which stores button state 
3. `lib/chorded` asks `lib/maps` what letter should be printed given the state
4. The letter is returned to the main loop and output

# Credit
To the awesome r4dian for the windows xbox controller handling code. 

https://github.com/r4dian/Xbox-360-Controller-for-Python
