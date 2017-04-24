# Chordboard

Be able to type in VR using VR controllers, starting with Oculus Touch. Currently it only works with the Xbox controller (any) but only uses buttons which are available on the Oculus Touch. 

# Quickstart

With an Xbox controller on: `python3 main.py`

# Current goal 4/23

Refactor how modifiers are handled in `lib/chorded` and `lib/maps` to be better. Shift should act like shift on a smartphone. Tap to activate, disable after 1 character, double tap to keep on, hold to keep on. 

# How it works

1. `main.py` initializes the Xbox controller and starts listening for input
2. Input is passed to `lib/chorded` which stores button state 
3. `lib/chorded` asks `lib/maps` what letter should be printed given the state
4. The letter is returned to the main loop and output

![how to gif](https://i.imgur.com/t4z772K.gif)
