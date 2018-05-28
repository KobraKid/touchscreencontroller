# #!/usr/bin/python3
import struct
import time
import sys
import keyboard


def translate_press_to_key():
    print (x, y)
    if x > 600:
        if y > 100 and y < 300:
            keyboard.press_and_release('a')
        elif y > 300:
            keyboard.press_and_release('b')
    elif x < 180:
        if y > 100 and y < 300:
            keyboard.press_and_release('x')
        elif y > 300:
            keyboard.press_and_release('y')


# infile_path = "input"
infile_path = "/dev/input/event2"

# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

# open file in binary mode
in_file = open(infile_path, "rb")
event = in_file.read(EVENT_SIZE)

# coordinate variables
x = -1
y = -1

while event:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

    if type != 0 or code != 0 or value != 0:
        # print("Event type %u, code %u, value %u at %d.%d" % (type, code, value, tv_sec, tv_usec))
        if code == 0:
            x = value
        elif code == 1:
            y = value
        else:
            x = -1
            y = -1
    else:  # Events with code, type AND value == 0 are "separator" events
        # print("===========================================")
        x = -1
        y = -1

    if x != -1 and y != -1:
        translate_press_to_key()

    event = in_file.read(EVENT_SIZE)

in_file.close()
