from pad4pi import rpi_gpio
import time
import keyboard

KEYPAD = [
    ["1", "2", "3", "a"],
    ["4", "5", "6", "b"],
    ["7", "8", "9", "c"],
    ["-", "0", "+", "d"],
]

# ROW_PINS = [4, 17, 27, 22]
# COL_PINS = [6, 13, 19, 26]
ROW_PINS = [26, 19, 13, 6]
COL_PINS = [22, 27, 17, 4]

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)


def printKey(key):
    keyboard.press_and_release(key)


keypad.registerKeyPressHandler(printKey)

try:
    while True:
        time.sleep(0.8)
except:
    keypad.cleanup()