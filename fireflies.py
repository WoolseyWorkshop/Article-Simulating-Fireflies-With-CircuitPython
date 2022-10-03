"""Simulates fireflies.

Description
-----------

A CircuitPython program that simulates fireflies.

Circuit
-------

- 8 LEDs, via 330 ohm resistors, are connected to pins D0-1, D4-6, and D9-11.

Libraries/Modules
-----------------

- random Standard Library
    - https://docs.python.org/3/library/random.html
    - Provides access to the uniform function.
- time Standard Library
    - https://docs.python.org/3/library/time.html
    - Provides access to the monotonic function.
- board CircuitPython Core Module
    - https://circuitpython.readthedocs.io/en/latest/shared-bindings/board/
    - Provides access to the board's GPIO pins and hardware.
- digitalio CircuitPython Core Module
    - https://circuitpython.readthedocs.io/en/latest/shared-bindings/digitalio/
    - Provides basic digital pin support.

Notes
-----

- Comments are Sphinx (reStructuredText) compatible.

TODO
----

- None.

Author(s)
---------

- Created by John Woolsey on 08/05/2021.
- Modified by John Woolsey on 09/28/2022.

Copyright (c) 2022 Woolsey Workshop.  All rights reserved.

Members
-------
"""


# Imports
import random
import time
import board
from digitalio import DigitalInOut


# Global Constants
DEBUG = False
"""The mode of operation; `False` = normal, `True` = debug."""

LIGHT_TIME = 0.5
"""The time that a firefly is lit in seconds."""

MIN_DARK_TIME = 5.0
"""The minimum time that a firefly is not lit in seconds."""

MAX_DARK_TIME = 10.0
"""The maximum time that a firefly is not lit in seconds."""


# Pin Mapping
LEDS = [
    DigitalInOut(board.D0),
    DigitalInOut(board.D1),
    DigitalInOut(board.D4),
    DigitalInOut(board.D5),
    DigitalInOut(board.D6),
    DigitalInOut(board.D9),
    DigitalInOut(board.D10),
    DigitalInOut(board.D11)
]
"""The LED pins representing the fireflies."""


# Classes
class Firefly:
    """The Firefly class.

    Contains the attributes needed for each simulated firefly.

    :param pin:           The pin controlling the LED.
    :type pin:            DigitalInOut
    :param name:          The name of the instance; defaults to `Unknown`.
    :type name:           string, optional
    :param is_lit:        The current lit status; `True` = on, `False` = off, defaults to `False`.
    :type is_lit:         bool, optional
    :param trigger_time:  The last time the firefly was lit; defaults to `0`.
    :type trigger_time:   time, optional
    :param trigger_delay: The delay between successive firefly light times; defaults to `0`.
    :type trigger_delay:  time, optional
    """

    def __init__(self, pin, name="Unknown", is_lit=False, trigger_time=0, trigger_delay=0):
        """The Firefly class constructor method."""

        self.pin = pin
        self.name = name
        self.is_lit = is_lit
        self.trigger_time = trigger_time
        self.trigger_delay = trigger_delay

    def __str__(self):
        """The string representation of a Firefly class instance."""

        return f"trigger_time = {self.trigger_time}, trigger_delay = {self.trigger_delay}, name = {self.name}, is_lit = {self.is_lit}"


# Global Instances
fireflies = []
"""The array of all firefly instances."""


# Functions
def process_firefly(firefly):
    """Processes the lighting timing of a firefly.

    :param firefly: The firefly instance.
    :type firefly:  Firefly
    """

    current_time = time.monotonic()  # time in seconds

    # Light firefly at appropriate trigger time
    if firefly.is_lit == False and current_time - firefly.trigger_time >= firefly.trigger_delay:
        if DEBUG:
            print(f"Firefly: currentTime = {current_time}, {firefly}")
            print("  Turning on firefly.")
        firefly.pin.value = True
        firefly.is_lit = True
        firefly.trigger_time = current_time
    # Turn off firefly after appropriate lit time
    elif firefly.is_lit == True and current_time - firefly.trigger_time >= LIGHT_TIME:
        if DEBUG:
            print(f"Firefly: currentTime = {current_time}, {firefly}")
            print("  Turning off firefly.")
        firefly.pin.value = False
        firefly.is_lit = False
        firefly.trigger_delay = LIGHT_TIME + random.uniform(MIN_DARK_TIME, MAX_DARK_TIME)


def main():
    """Main program entry."""

    if DEBUG:
        print("Running in DEBUG mode.  Turn off for normal operation.")

    # Configure all fireflies
    for index, led in enumerate(LEDS):
        led.switch_to_output(value=False)
        fireflies.append(Firefly(pin=led, name=f"LEDS[{index}]", trigger_delay=random.uniform(MIN_DARK_TIME, MAX_DARK_TIME)))

    # Process all fireflies
    while True:
        for firefly in fireflies:
            process_firefly(firefly)


if __name__ == "__main__":  # required for generating Sphinx documentation
    main()
