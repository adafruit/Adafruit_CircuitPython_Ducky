# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Eva Herrada for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_ducky`
================================================================================

CircuitPython library for running DuckyScript


* Author(s): Eva Herrada

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
import time
from adafruit_hid.keycode import Keycode

try:
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keyboard_layout_base import KeyboardLayoutBase
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Ducky.git"

commands = {
    "DELETE": Keycode.DELETE,
    "HOME": Keycode.HOME,
    "END": Keycode.END,
    "INSERT": Keycode.INSERT,
    "PAGEUP": Keycode.PAGE_UP,
    "PAGEDOWN": Keycode.PAGE_DOWN,
    "ESC": Keycode.ESCAPE,
    "ESCAPE": Keycode.ESCAPE,
    "UPARROW": Keycode.UP_ARROW,
    "UP": Keycode.UP_ARROW,
    "DOWNARROW": Keycode.DOWN_ARROW,
    "DOWN": Keycode.DOWN_ARROW,
    "LEFTARROW": Keycode.LEFT_ARROW,
    "LEFT": Keycode.LEFT_ARROW,
    "RIGHTARROW": Keycode.RIGHT_ARROW,
    "RIGHT": Keycode.RIGHT_ARROW,
    "F1": Keycode.F1,
    "F2": Keycode.F2,
    "F3": Keycode.F3,
    "F4": Keycode.F4,
    "F5": Keycode.F5,
    "F6": Keycode.F6,
    "F7": Keycode.F7,
    "F8": Keycode.F8,
    "F9": Keycode.F9,
    "F10": Keycode.F10,
    "F11": Keycode.F11,
    "F12": Keycode.F12,
    "SPACE": Keycode.SPACE,
    "TAB": Keycode.TAB,
    "ENTER": Keycode.ENTER,
    "BREAK": Keycode.PAUSE,
    "PAUSE": Keycode.PAUSE,
    "CAPSLOCK": Keycode.CAPS_LOCK,
    "NUMLOCK": Keycode.KEYPAD_NUMLOCK,
    "PRINTSCREEN": Keycode.PRINT_SCREEN,
    "SCROLLLOCK": Keycode.SCROLL_LOCK,
    "FN": Keycode.OPTION,
    "MENU": Keycode.APPLICATION,
    "WINDOWS": Keycode.GUI,
    "GUI": Keycode.GUI,
    "SHIFT": Keycode.SHIFT,
    "ALT": Keycode.ALT,
    "CONTROL": Keycode.CONTROL,
    "CTRL": Keycode.CONTROL,
}


class Ducky:
    """
    Class that runs a DuckyScript file.

    **Quickstart: Importing and using the library**

        Here is an example of using the :class:`Ducky` class.
        First you will need to import the libraries

        .. code-block:: python

            import time
            import usb_hid
            from adafruit_hid.keyboard import Keyboard
            from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
            import ducky

        Once this is done, define the keyboard layout and initialize the :class:`Ducky` class.

        .. code-block:: python

            time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
            keyboard = Keyboard(usb_hid.devices)
            keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

            duck = ducky.Ducky('duckyscript.txt', keyboard, keyboard_layout)

        Now, set up a loop which will run a line of the script every time `loop` is called.

        .. code-block:: python

            result = True
            while result is not False:
                result = duck.loop()

    """

    def __init__(
        self, filename: str, keyboard: Keyboard, layout: KeyboardLayoutBase
    ) -> None:
        self.keyboard = keyboard
        self.layout = layout
        self.lines = []
        self.default_delay = 0
        self.prev_line = None
        self.next_index = 0
        self.wait_until = 0
        self.repeat = 0

        with open(filename, "r") as duckyscript:
            for line in duckyscript:
                line = line.strip(" \r")
                if len(line) > 0:
                    self.lines.append(line)

    def loop(  # pylint: disable=too-many-return-statements
        self,
    ) -> bool:  # pylint: disable=too-many-branches
        """Function that sends a line of the DuckyScript file over hid every time it is called"""

        now = time.monotonic_ns()
        if now < self.wait_until:
            return True

        try:
            if self.repeat > 0:
                self.repeat -= 1
                line = self.prev_line
            else:
                line = self.lines[self.next_index]
                self.next_index += 1
        except IndexError:
            print("  DONE!")
            self.prev_line = None
            self.next_index = 0
            return False

        words = line.split(" ", 1)
        start = words[0]

        if start == "REPEAT":
            self.repeat = int(words[1])
            return True

        self.prev_line = line

        # print(f"  {line}")

        if start == "REM":
            # print(words[1])
            return True

        self.wait_until = now + self.default_delay

        if start in ("DEFAULT_DELAY", "DEFAULTDELAY"):
            self.wait_until -= self.default_delay
            self.default_delay = int(words[1]) * 1000000
            self.wait_until += self.default_delay
            return True

        if start == "DELAY":
            self.wait_until += int(words[1]) * 1000000
            return True

        if start == "STRING":
            self.layout.write(words[1])
            return True

        self.write_key(start)
        if len(words) > 1:
            for key in words[1].split(" "):
                self.write_key(key)

        self.keyboard.release_all()
        return True

    def write_key(self, start: str) -> None:
        """Writes the keys over HID. Used to help with more complicated commands"""
        if start in commands:
            self.keyboard.press(commands[start])
        else:
            self.layout.write(start)
