import datetime

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from ..bin.get_res import get_res
from ..bin.flash_btn import flash_btn
from ..bin.timer import interval
from ..bin.key_event import get_key
from ..bin.input_helper import InputHelper
from ..bin import environment as env


class InputDialog(QDialog):

    def __init__(self, title, content):
        super(InputDialog, self).__init__(None)
        self.title = title
        self.content = content

        # Other options
        self.date_format = "%d/%m/%y"

        # Auxiliary
        self.aux_input = InputHelper(self.content["type"], self.date_format)
        if content['value'] != '': self.aux_input.value = str(content['value'])

        # Load UI
        loadUi(get_res("ui/input.ui"), self)
        self.label_title.setText(title)
        self.label_text.setText(content['help'])
        self.label_value.setText(self.aux_input.value)
        self.label_units.setText(content['units'])
        self.frame_keypad.setHidden(True)
        self.spacer_c.setHidden(True)
        self.spacer_d.setHidden(True)
        if env.get("TOUCHSCREEN_TERMINAL"): self.as_touchscreen()

        # Set title, hide cursor, make full screen
        env.set_qtform(self, title)

        # Hide "." button if type is int or date
        if self.content['type'] in ['int', 'date']:
            self.frame_btn_m.setHidden(True)

        # Click events
        self.frame_btn_c.mousePressEvent = self.click_c
        self.frame_btn_d.mousePressEvent = self.click_d
        self.frame_btn_m.mousePressEvent = self.click_keypad_period
        self.frame_btn_p.mousePressEvent = self.click_keypad_backspace
        self.frame_btn_0.mousePressEvent = lambda ev: self.click_keypad_number(ev, "0")
        self.frame_btn_1.mousePressEvent = lambda ev: self.click_keypad_number(ev, "1")
        self.frame_btn_2.mousePressEvent = lambda ev: self.click_keypad_number(ev, "2")
        self.frame_btn_3.mousePressEvent = lambda ev: self.click_keypad_number(ev, "3")
        self.frame_btn_4.mousePressEvent = lambda ev: self.click_keypad_number(ev, "4")
        self.frame_btn_5.mousePressEvent = lambda ev: self.click_keypad_number(ev, "5")
        self.frame_btn_6.mousePressEvent = lambda ev: self.click_keypad_number(ev, "6")
        self.frame_btn_7.mousePressEvent = lambda ev: self.click_keypad_number(ev, "7")
        self.frame_btn_8.mousePressEvent = lambda ev: self.click_keypad_number(ev, "8")
        self.frame_btn_9.mousePressEvent = lambda ev: self.click_keypad_number(ev, "9")

        # Set focus
        self.setFocus()

        # Preset result
        self.result = None

    def hide_btn_c(self):
        self.frame_btn_c_out.setHidden(True)
        self.spacer_c.setHidden(False)

    def hide_btn_d(self):
        self.frame_btn_d_out.setHidden(True)
        self.spacer_d.setHidden(False)

    def as_touchscreen(self):
        self.frame_keypad.setHidden(False)
        self.label_btn_c.setHidden(True)
        self.label_btn_d.setHidden(True)

    def keyPressEvent(self, event):
        key = get_key(event)

        if key == "": return
        elif key == "c": self.click_c(None)
        elif key == "d": self.click_d(None)
        elif key == ".": self.click_keypad_period(None)
        elif key == "backspace": self.click_keypad_backspace(None)
        else: self.click_keypad_number(None, key)

    def click_c(self, ev):
        flash_btn(self.frame_btn_c)
        self.on_btn_c()

    def on_btn_c(self):
        self.result = None
        self.reject()

    def click_d(self, ev):
        flash_btn(self.frame_btn_d)
        self.on_btn_d()

    def on_btn_d(self):
        valid = True

        # Get result
        r = self.aux_input.get_value()
        valid = self.aux_input.validate()

        # Validate
        if valid and self.content['validate'] is not None:
            valid = self.content['validate'](r)

        if not valid:
            self.label_value.setStyleSheet("color:red")
            self.label_units.setStyleSheet("color:red")
            return
        else:
            self.label_value.setStyleSheet("color:black")
            self.label_units.setStyleSheet("color:black")
            pass

        # Return
        self.result = r
        self.accept()

    def click_keypad_number(self, ev, number):
        if number == "0": flash_btn(self.frame_btn_0)
        if number == "1": flash_btn(self.frame_btn_1)
        if number == "2": flash_btn(self.frame_btn_2)
        if number == "3": flash_btn(self.frame_btn_3)
        if number == "4": flash_btn(self.frame_btn_4)
        if number == "5": flash_btn(self.frame_btn_5)
        if number == "6": flash_btn(self.frame_btn_6)
        if number == "7": flash_btn(self.frame_btn_7)
        if number == "8": flash_btn(self.frame_btn_8)
        if number == "9": flash_btn(self.frame_btn_9)
        self.label_value.setText(self.aux_input.write(number))
        self.on_input_change()

    def click_keypad_period(self, ev):
        flash_btn(self.frame_btn_m)
        self.label_value.setText(self.aux_input.write("."))
        self.on_input_change()

    def click_keypad_backspace(self, ev):
        flash_btn(self.frame_btn_p)
        self.label_value.setText(self.aux_input.clear())
        self.on_input_change()

    # --------------------------------------------------------------------------
    # Callbacks
    # --------------------------------------------------------------------------
    def on_input_change(self): return

    @staticmethod
    def show_dialog(title, content, options={}):
        default_content = {
            "type": "generic",  # int, float, date, generic
            "value": "",
            "units": "",
            "validate": None,
            "help": "",
            "date_format": "%d/%m/%y",
        }

        for c in content: default_content[c] = content[c]
        dialog = InputDialog(title, default_content)
        dialog.date_format = default_content["date_format"]
        dialog.aux_input.set_date_format(default_content["date_format"])

        if "hide_btn_c" in options and options["hide_btn_c"]: dialog.hide_btn_c()
        if "hide_btn_d" in options and options["hide_btn_d"]: dialog.hide_btn_d()
        if "hide_keypad" in options: dialog.frame_keypad.setHidden(options["hide_keypad"])

        dialog.exec_()
        return dialog.result

