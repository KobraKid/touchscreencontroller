# #!/usr/bin/python3
"""Touchscreen game controller for official Raspberry Pi 7" touchscreen.

Takes in touch events from /dev/input/eventX where X is the index of
the touchscreen. Translates touch events into virtual keyboard presses.

TODO: Draw bounds on screen (in assembly?).
      Determine if keys are correct.
      Determine how to handle continuous pressure.
      Determine how to handle analog input (joysticks).
"""
import struct
import time
import sys
import keyboard
import pygame
import signal
import copy

__author__ = "Michael Huyler"
__copyright__ = "Copyright 2018"
__credits__ = ["https://stackoverflow.com/a/16682549/7789614"]
__license__ = ""
__version__ = "1"
__maintainer__ = "Michael Huyler"
__email__ = "michaelhuyler2020@u.northwestern.edu"
__status__ = "Development"


class Event:
    # Event constants
    MIN_ID = 4294967295
    # long int, long int, unsigned short, unsigned short, unsigned int
    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)
    ABS_MT_SLOT = 47
    ABS_MT_TRACKING_ID = 57
    ABS_MT_POSITION_X = 53
    ABS_MT_POSITION_Y = 54


class Button:
    # button types
    RECT = 0
    CIRC = 1
    ANALOG = 2


# screen size constants
# top-left = 0, 0
WIDTH = 800
HEIGHT = 480

# infile_path = "input"
infile_path = "/dev/input/event2"

"""List of buttons, where
    key = button name
    value = (RECT, x, y, w, h) OR (CIRC, x, y, radius)

    Button coordinates:

    Main
    x: 693 129 - 732 174
    y: 651 174 - 689 216
    a: 736 174 - 774 216
    b: 693 216 - 732 257

    D-Pad
    up:    64 232 -  96 264
    right: 96 264 - 128 296
    down:  64 296 -  96 328
    left:  32 264 -  64 296

    Hotkey
    home: 371 439 - 425 470

    Menu
    start:  657 318 - 683 344
    select: 657 370 - 683 397

    Analog
    r-stick: 25 92 - 138 208
    l-stick:
"""
buttons = {
    # Main
    "a": (Button.CIRC, 750, 240, 50),
    "b": (Button.CIRC, 750, 240, 50),
    "x": (Button.CIRC, 750, 240, 50),
    "y": (Button.CIRC, 750, 240, 50),
    # D-Pad
    "up": (Button.RECT, 750, 240, 32),
    "down": (Button.RECT, 750, 240, 32),
    "left": (Button.RECT, 750, 240, 32),
    "right": (Button.RECT, 750, 240, 32),
    # Hotkey
    "home": (Button.RECT, 750, 240, 50),
    # Menu
    "start": (Button.RECT, 750, 240, 50),
    "select": (Button.RECT, 750, 240, 50)
}

"""A dictionary of touch events. Format:
    id: [x, y, slot, active?]
"""
touches = {}

in_file = None


def on_exit(signum, frame):
    if in_file:
        in_file.close()
    sys.exit(0)


def translate_press_to_key():
    """Cycle through touch events, and type the corresponding key."""
    # A: 'z', B: 'x', X: 'a', Y: 's'
    # L: 'c', R: 'v', ZL: 'd', ZR: 'f'
    # Select: 'left shift', Start: 'enter', Hotkey: 'escape'
    # temp_touches = {key: value[:] for key, value in touches.items()}
    # for key in touches:  # Remove inactive touches
    #     if not touches[key][3]:  # Touch is no longer active
    #         keyboard.release('z')
    #         del temp_touches[key]
    # touches = {key: value[:] for key, value in temp_touches.items()}
    # for key in touches:  # Maintian touches
    #     if not keyboard.is_pressed('z'):
    #         keyboard.press('z')
    print(str(touches))


def within_button(radius, x, y):
    return False


def main():
    # coordinate variables
    slot = -1
    id = -1
    x = -1
    y = -1

    # open file in binary mode
    in_file = open(infile_path, "rb")
    event = in_file.read(Event.EVENT_SIZE)

    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(Event.FORMAT, event)

        if type != 0 or code != 0 or value != 0:
            if code == Event.ABS_MT_SLOT:
                slot = value
            elif code == Event.ABS_MT_TRACKING_ID:
                id = value
                if id == Event.MIN_ID:  # This is a release, so set id to min id and remove it
                    for key in touches:
                        if id == Event.MIN_ID:
                            id = key
                        elif key < id:
                            id = key
                    print("Remove event", id)
                    touches[id][3] = False
                    x = -1
                    y = -1
                elif id in touches:  # This is a drag event, so update x | y
                    print("Modify event", id)
                    x = touches[id][0]
                    y = touches[id][1]
                else:  # This is a new touch, so add it and set it as active
                    print("Create event", id)
                    touches[id] = [-1, -1, -1, True]
            elif code == Event.ABS_MT_POSITION_X:
                x = value
            elif code == Event.ABS_MT_POSITION_Y:
                y = value

        else:  # Events with code, type AND value == 0 are "separator" events
            x = -1
            y = -1

        # Perform button presses for each button being pressed
        translate_press_to_key()

        event = in_file.read(Event.EVENT_SIZE)

    on_exit(None, None)


if __name__ == "__main__":
    # catch exit and close file to prevent resource leaks
    signal.signal(signal.SIGINT, on_exit)
    # begin main
    main()
