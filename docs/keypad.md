# Using the keypad

See the bin/key_event.py file to see how the keys are mapped from the keypad. A normal keyboard can be used, naturally, using the keys "A", "B", "C" and "D" for the special buttons.

If you want to use a keypad, you will have to write a program to map the keypad buttons (connected to the GPIO pins of a rapsberry pi, for example) to the corresponding keyboard keys. You can use the following python code (you will have to include this in a service to run on the background and on startup)

```python
from pad4pi import rpi_gpio
import time
import keyboard

KEYPAD = [
    ["1", "2", "3", "a"],
    ["4", "5", "6", "b"],
    ["7", "8", "9", "c"],
    ["-", "0", "+", "d"],
]

ROW_PINS = [26, 19, 13, 6]
COL_PINS = [22, 27, 17, 4]

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

def printKey(key):
    keyboard.press_and_release(key)
```

The "-" and "+" chars (corresponding to the "*" and "#" buttons) are then mapped to the stop (".") and backspace keys ion the key_event.py file.

