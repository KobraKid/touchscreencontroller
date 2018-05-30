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

__author__ = "Michael Huyler"
__copyright__ = "Copyright 2018"
__credits__ = ["https://stackoverflow.com/a/16682549/7789614"]
__license__ = ""
__version__ = "1"
__maintainer__ = "Michael Huyler"
__email__ = "michaelhuyler2020@u.northwestern.edu"
__status__ = "Development"


# screen size constants
# top-left = 0, 0
WIDTH = 800
HEIGHT = 480

# infile_path = "input"
infile_path = "/dev/input/event2"

# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

# button types
RECT = 0
CIRC = 1
ANALOG = 2

# other globals
TOUCH = False

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
    "a": (CIRC, 750, 240, 50),
    "b": (CIRC, 750, 240, 50),
    "x": (CIRC, 750, 240, 50),
    "y": (CIRC, 750, 240, 50),
    # D-Pad
    "up": (RECT, 750, 240, 32),
    "down": (RECT, 750, 240, 32),
    "left": (RECT, 750, 240, 32),
    "right": (RECT, 750, 240, 32),
    # Hotkey
    "home": (RECT, 750, 240, 50),
    # Menu
    "start": (RECT, 750, 240, 50),
    "select": (RECT, 750, 240, 50)
}


def on_exit(signum, frame):
    in_file.close()
    sys.exit(0)


def translate_press_to_key():
    """Check x and y of a touch event, and type the corresponding key."""
    # print (x, y)
    # A: 'z', B: 'x', X: 'a', Y: 's'
    # L: 'c', R: 'v', ZL: 'd', ZR: 'f'
    # Select: 'left shift', Start: 'enter', Hotkey: 'escape'
    # keyboard.press_and_release('z')


def within_button(radius, x, y):
    return False


def main():
    # coordinate variables
    x = -1
    y = -1

    # open file in binary mode
    in_file = open(infile_path, "rb")
    event = in_file.read(EVENT_SIZE)

    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

        # Triggered every downpress and every uppress, so toggle press bool
        if type == 1:
            if code == 330:
                TOUCH = !TOUCH
        elif type != 0 or code != 0 or value != 0:
            if code == 0:
                x = value
            elif code == 1:
                y = value
            else:
                x = -1
                y = -1
        else:  # Events with code, type AND value == 0 are "separator" events
            x = -1
            y = -1

        if x != -1 and y != -1:
            translate_press_to_key()

        event = in_file.read(EVENT_SIZE)
    on_exit(None, None)


if __name__ == "__main__":
    # catch exit and close file to prevent resource leaks
    signal.signal(signal.SIGINT, on_exit)
    # begin main
    main()
