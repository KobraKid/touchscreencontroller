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
import signal
import copy
import math
import screentest
import common

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


# screen size constants
# top-left = 0, 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

"""A dictionary of touch events. Format:
    id: [active?, x, y, slot, BTN]
"""
touches = {}

# FIFO for touch events
infile_path = "/dev/input/event2"
in_file = None


def on_exit(signum, frame):
    if in_file:
        in_file.close()
    sys.exit(0)


def translate_press_to_key():
    """Cycle through touch events, and press and release the corresponding keys."""
    global touches

    # Release inactive touches
    for key in touches:
        if not touches[key][common.ID.ACTIVE]:
            if touches[key][common.ID.BTN] is not None:
                keyboard.release(touches[key][common.ID.BTN])

    # Purge inactive touches from dictionary
    temp_touches = {key: value[:] for key, value in touches.items() if touches[key][common.ID.ACTIVE]}
    touches = {key: value[:] for key, value in temp_touches.items()}

    # Activate new touches
    for key in touches:
        # if touches[key][common.ID.BTN] is None:
        # Update all touches (to include sliding off a button)
        touches[key][common.ID.BTN] = within_button(touches[key][common.ID.X], touches[key][common.ID.Y])
        if touches[key][common.ID.BTN] is not None:
            if not keyboard.is_pressed(touches[key][common.ID.BTN]):
                keyboard.press(touches[key][common.ID.BTN])

    if touches:
        print("ID: [ACTV,  X,  Y,  S, BTN]")
    for key in touches:
        print(str(key) + ": " + str(touches[key]), end="")
    if touches:
        print("\n________________________________________________________________________________")


def within_button(x, y):
    """Given a point on the screen, returns the key corresponding to the button
    being pressed, or None if it does not fall within a button."""
    for key in common.buttons:
        if common.buttons[key][common.ID.B_TYPE] == common.Button.CIRC:
            # Determine if a touch is within circular bounds
            if math.sqrt(((common.buttons[key][common.ID.X] - x) ** 2)
                         + ((common.buttons[key][common.ID.Y] - y) ** 2)) \
                         <= common.buttons[key][common.ID.RAD]:
                return key
        elif common.buttons[key][common.ID.B_TYPE] == common.Button.RECT:
            # Determine if a touch is within rectangular bounds
            if (common.buttons[key][common.ID.X]
               <= x <=
               (common.buttons[key][common.ID.X] + common.buttons[key][common.ID.WIDTH])) \
               and (common.buttons[key][common.ID.Y]
               <= y <=
               (common.buttons[key][common.ID.Y] + common.buttons[key][common.ID.HEIGHT])):
                return key
        elif common.buttons[key][common.ID.B_TYPE] == common.Button.ANALOG:
            # TODO This will be for the analog sticks
            pass
    return None


def main():
    screentest.init_pygame()
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
        # screentest.update_screen()
        (tv_sec, tv_usec, type, code, value) = struct.unpack(Event.FORMAT, event)

        if type != 0 or code != 0 or value != 0:
            if code == Event.ABS_MT_SLOT:
                slot = value
            elif code == Event.ABS_MT_TRACKING_ID:
                id = value
                if id == Event.MIN_ID:  # This is a release, so set id to min id and remove it
                    # Remove by slot
                    for key in touches:
                        if touches[key][common.ID.SLOT] == slot:
                            id = key
                    # Remove by tracking id if that fails
                    if id == Event.MIN_ID:
                        for key in touches:
                            if id == Event.MIN_ID:
                                id = key
                            elif key < id:
                                id = key
                    print("Remove event", id)
                    touches[id][common.ID.ACTIVE] = False
                    x = -1
                    y = -1
                elif id in touches:  # This is a drag event, so update x | y
                    print("Modify event", id)
                    x = touches[id][common.ID.X]
                    y = touches[id][common.ID.Y]
                else:  # This is a new touch, so add it and set it as active
                    print("Create event", id)
                    touches[id] = [True, -1, -1, slot, None]
            elif code == Event.ABS_MT_POSITION_X:
                x = value
                if id in touches:
                    touches[id][common.ID.X] = x
            elif code == Event.ABS_MT_POSITION_Y:
                y = value
                if id in touches:
                    touches[id][common.ID.Y] = y

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
