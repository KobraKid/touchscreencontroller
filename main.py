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
import math

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


class Ind:
    # Index references
    B_TYPE = 0
    X = 1
    Y = 2
    WIDTH = 3
    HEIGHT = 4
    RAD = 3


# screen size constants
# top-left = 0, 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# infile_path = "input"
infile_path = "/dev/input/event2"

"""List of buttons, where
    key = button name
    value = (RECT, x, y, w, h) OR (CIRC, x, y, radius)

    Button coordinates:

    Main
    x: 693 351 - 732 306 }
    y: 651 306 - 689 264 } only correct coords right now
    a: 736 306 - 774 264 }
    b: 693 264 - 732 223 }

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
    "a": (Button.CIRC, 726, 296, 20),
    "b": (Button.CIRC, 683, 341, 20),
    "x": (Button.CIRC, 683, 254, 20),
    "y": (Button.CIRC, 641, 296, 20),
    # D-Pad
    # "up": (Button.RECT, 750, 240, 32),
    # "down": (Button.RECT, 750, 240, 32),
    # "left": (Button.RECT, 750, 240, 32),
    # "right": (Button.RECT, 750, 240, 32),
    # Hotkey
    # "home": (Button.RECT, 750, 240, 50),
    # Menu
    # "start": (Button.RECT, 750, 240, 50),
    # "select": (Button.RECT, 750, 240, 50)
}

"""A dictionary of touch events. Format:
    id: [x, y, slot, active?, BTN]
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
    # touches = {key: value[:] for key, value in temp_touches.items()}
    # for key in touches:  # Maintian touches
    #     if not keyboard.is_pressed('z'):
    #         keyboard.press('z')
    global touches

    # Release inactive touches
    for key in touches:
        if not touches[key][3]:
            if touches[key][4] is not None:
                keyboard.release(touches[key][4])

    # Purge inactive touches from dictionary
    temp_touches = {key: value[:] for key, value in touches.items() if touches[key][3]}
    touches = {key: value[:] for key, value in temp_touches.items()}

    # Activate new touches
    for key in touches:
        if touches[key][4] is None:
            touches[key][4] = within_button(touches[key][0], touches[key][1])
        if touches[key][4] is not None:
            if not keyboard.is_pressed(touches[key][4]):
                keyboard.press(touches[key][4])

    if touches:
        print("ID: [  X,  Y,  S, ACTV]")
    for key in touches:
        print(str(key) + ": " + str(touches[key]), end="")
    if touches:
        print("\n=============================================================")


def within_button(x, y):
    """Given a point on the screen, returns the key corresponding to the button
    being pressed, or None if it does not fall within a button."""
    for key in buttons:
        if buttons[key][Ind.B_TYPE] == Button.CIRC:
            if math.sqrt(((buttons[key][Ind.X] - x) ** 2) + ((buttons[key][Ind.Y] - y) ** 2)) <= buttons[key][Ind.RAD]:
                return key
        elif buttons[key][Ind.B_TYPE] == Button.RECT:
            if (buttons[key][Ind.X] <= x <= (buttons[key][Ind.X] + buttons[key][Ind.WIDTH])) \
               and (buttons[key][Ind.Y] <= y <= (buttons[key][Ind.Y] + buttons[key][Ind.HEIGHT])):
                return key
    return None


def main():
    # Set up Pygame for testing button locations
    global SCREEN_WIDTH, SCREEN_HEIGHT
    pygame.init()
    myfont = pygame.font.SysFont("monospace", 40)
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 127))
    pygame.draw.circle(screen, (0, 255, 0), (buttons["a"][Ind.X], buttons["a"][Ind.Y]), 20)
    label = myfont.render("A", 1, (255, 0, 255))
    screen.blit(label, (buttons["a"][Ind.X] - 12, buttons["a"][Ind.Y] - 20))
    pygame.draw.circle(screen, (255, 0, 0), (buttons["b"][Ind.X], buttons["b"][Ind.Y]), 20)
    label = myfont.render("B", 1, (0, 255, 255))
    screen.blit(label, (buttons["b"][Ind.X] - 12, buttons["b"][Ind.Y] - 20))
    pygame.draw.circle(screen, (0, 0, 255), (buttons["x"][Ind.X], buttons["x"][Ind.Y]), 20)
    label = myfont.render("X", 1, (255, 255, 0))
    screen.blit(label, (buttons["x"][Ind.X] - 12, buttons["x"][Ind.Y] - 20))
    pygame.draw.circle(screen, (255, 255, 0), (buttons["y"][Ind.X], buttons["y"][Ind.Y]), 20)
    label = myfont.render("Y", 1, (0, 0, 255))
    screen.blit(label, (buttons["y"][Ind.X] - 12, buttons["y"][Ind.Y] - 20))
    pygame.display.update()

    # Touch event variables
    global touches
    slot = -1
    id = -1
    x = -1
    y = -1

    # Open file in binary mode
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
                    touches[id] = [-1, -1, slot, True, None]
            elif code == Event.ABS_MT_POSITION_X:
                x = value
                touches[id][0] = x
            elif code == Event.ABS_MT_POSITION_Y:
                y = value
                touches[id][1] = y

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
