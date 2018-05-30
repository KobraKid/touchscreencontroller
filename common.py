class Button:
    # button types
    RECT = 0
    CIRC = 1
    ANALOG = 2


class ID:
    # Index references
    B_TYPE = 0
    X = 1
    Y = 2
    WIDTH = 3
    HEIGHT = 4
    RAD = 3
    ACTIVE = 0
    SLOT = 3
    BTN = 4


"""List of buttons, where
    key = button name
    value = (RECT, x, y, w, h) OR (CIRC, x, y, radius)
"""
buttons = {
    # Main
    "a": (Button.CIRC, 683, 224, 20),
    "b": (Button.CIRC, 726, 184, 20),
    "x": (Button.CIRC, 641, 184, 20),
    "y": (Button.CIRC, 683, 144, 20),
    # D-Pad
    "up arrow": (Button.RECT, 74, 256, 40, 40),
    "down arrow": (Button.RECT, 74, 336, 40, 40),
    "left arrow": (Button.RECT, 34, 296, 40, 40),
    "right arrow": (Button.RECT, 114, 296, 40, 40),
    # Hotkey
    "esc": (Button.RECT, 375, 440, 50, 30),
    # Menu
    # "enter": (Button.RECT, ),
    # "left shift": (Button.RECT, )  # Potentially needs 'right shift'
}
