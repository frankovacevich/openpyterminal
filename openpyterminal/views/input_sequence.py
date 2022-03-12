import datetime

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from ..common.get_res import get_res
from ..common.flash_btn import flash_btn, cycle_flash_btn
from ..common.timer import interval, Chronometer
from ..common.key_event import get_key
from ..common.input_helper import InputHelper
from ..common import environment as env

from .input_dialog import InputDialog


# ==============================================================================
# Helper class
# ==============================================================================
class Sequence:

    def __init__(self, fields, copy=True):
        self.fields = [x.copy() for x in fields] if copy else fields
        self.entries = []
        self.cf = 0  # current field
        self.ce = 0  # current entry
        self.add_entry()

    def add_entry(self):
        new_entry = {}
        for f in self.fields: new_entry[f['name']] = None

        # Add new entry
        self.entries.append(new_entry)
        self.ce = len(self.entries) - 1
        self.cf = 0

    def prev_field(self):
        # Move to previous field
        while self.cf > 0:
            self.cf -= 1
            if "skip" in self.fields[self.cf] and self.fields[self.cf]["skip"]: continue
            return True
        return False

    def next_field(self):
        # Move to next field
        while self.cf + 1 < len(self.fields):
            self.cf += 1
            if "skip" in self.fields[self.cf] and self.fields[self.cf]["skip"]: continue
            return True
        return False

    def go_to_entry(self, indx):
        # Change current entry
        self.ce = indx

    def update_field(self, field_name, parameter, value):
        # Modify field
        for f in self.fields:
            if f["name"] == field_name:
                f[parameter] = value
                return True
        return False

    def get_current(self):
        # Returns current field and current entry value
        if len(self.entries) == 0: return None
        field = self.fields[self.cf]
        return field, self.entries[self.ce][field['name']]

    def get_value_from_previous_entry(self):
        # Returns value of the current field but the previous entry (used for default values)
        if self.ce == 0: return None
        field = self.fields[self.cf]
        return self.entries[self.ce - 1][field["name"]]

    def set_current(self, value):
        # Set current field of current entry value
        self.entries[self.ce][self.fields[self.cf]['name']] = value

    def get_entry(self, entry_number=None, skip_null=False):
        # Returns the complete entry
        if len(self.entries) == 0: return None
        if entry_number is None: entry_number = self.ce

        E = self.entries[entry_number]
        if skip_null: return {e: E[e] for e in E if E[e] is not None}
        else: return E

    def remove_all_entries_except_last(self):
        # Removes all but the last entry
        if len(self.entries) == 0: return None
        new_entries = [self.entries[-1]]
        self.entries = new_entries
        self.ce = 0
        return

    def reset(self):
        self.entries = []
        self.ce = 0
        self.cf = 0
        self.add_entry()


# ==============================================================================
# Main class
# ==============================================================================
class InputSequence(QWidget):

    def __init__(self, title):
        super(InputSequence, self).__init__(None)
        self.title = title
        self.subtitle = ""
        self.field_title = ""
        self.field_subtitle = ""
        self.bottom_text = ""
        self.alt_bottom_text = ""
        self.date_format = "%d/%m/%y"

        # More options
        self.sequence = None
        self.close_on_first_field = False # Close the widget when button C is pressed on the first field of the sequence

        # Load UI
        loadUi(get_res('ui/input_sequence.ui'), self)
        self.label_title.setText(self.title)
        if env.get("TOUCHSCREEN_TERMINAL"): self.as_touchscreen()
        self.frame_btn_a_in.setHidden(True)

        # Set title, hide cursor, make full screen
        env.set_qtform(self, title)

        # Click events
        self.frame_btn_a.mousePressEvent = self.click_a
        self.frame_btn_b.mousePressEvent = self.click_b
        self.frame_btn_c.mousePressEvent = self.click_c
        self.frame_btn_d.mousePressEvent = self.click_d
        self.frame_btn_2_out.mousePressEvent = self.click_2
        self.frame_btn_8_out.mousePressEvent = self.click_8

        self.label_value.mousePressEvent = self.label_value_clicked

        # Set clock
        self.clock_tick()
        interval(1000, self, self.clock_tick)

        # Button flashing
        self.cycle_flash_btn_a = cycle_flash_btn(self.frame_btn_a)
        self.cycle_flash_btn_b = cycle_flash_btn(self.frame_btn_b)

        # Set focus
        self.setFocus()

        # Auxiliary
        self.aux_input = InputHelper()
        self.chronometer = Chronometer()

    # --------------------------------------------------------------------------
    # GUI Methods
    # --------------------------------------------------------------------------
    def as_touchscreen(self):
        self.label_btn_2.setHidden(True)
        self.label_btn_8.setHidden(True)
        self.label_btn_a.setHidden(True)
        self.label_btn_b.setHidden(True)
        self.label_btn_c.setHidden(True)
        self.label_btn_d.setHidden(True)

    def set_icon(self, btn, res):
        pixmap = QtGui.QPixmap()
        pixmap.load(get_res(res))
        if btn == "a": self.icon_btn_a.setPixmap(pixmap)
        if btn == "b": self.icon_btn_b.setPixmap(pixmap)
        if btn == "c": self.icon_btn_c.setPixmap(pixmap)
        if btn == "d": self.icon_btn_d.setPixmap(pixmap)

    def hide_btn(self, btn, hide=True):
        if btn == "a": self.frame_btn_a_in.setHidden(hide)
        if btn == "b": self.frame_btn_b_in.setHidden(hide)
        if btn == "c": self.frame_btn_c_in.setHidden(hide)
        if btn == "d": self.frame_btn_d_in.setHidden(hide)

    def update(self):
        # Callback
        self.on_field_load()

        # Get current field and value
        c, v = self.sequence.get_current()
        self.field_title = c['title']
        self.field_subtitle = c['subtitle']

        # Labels
        self.label_text0.setText(self.subtitle)
        self.label_text1.setText(self.field_title)
        self.label_text2.setText(self.field_subtitle)
        self.label_text3.setText(self.bottom_text)
        self.label_text4.setText(self.alt_bottom_text)

        # Units
        units = c['units'] if 'units' in c else ''
        self.label_units.setText(units)

        # Value
        if c['type'] == "current_time":
            if v is not None: self.label_value.setText(str(v))
            else: self.clock_tick()
        else:
            options = c['options'] if 'options' in c else {}
            self.aux_input = InputHelper(c['type'], options=options)
            self.aux_input.set_date_format(self.date_format)

            if v is None and 'default' in c:
                if c['default'] == 'auto': v = self.sequence.get_value_from_previous_entry()
                else: v = c['default']

            #if v is not None: self.aux_input.value = str(v)
            if v is not None: self.aux_input.set_value(v)
            self.label_value.setText(self.aux_input.value)

        # Buttons 2 and 8
        if c['type'] == 'options':
            self.frame_btn_2_out.setHidden(False)
            self.frame_btn_8_out.setHidden(False)
        else:
            self.frame_btn_2_out.setHidden(True)
            self.frame_btn_8_out.setHidden(True)

    # ---------------------------------------------------------------------------
    # Buttons
    # --------------------------------------------------------------------------
    def keyPressEvent(self, event):
        key = get_key(event)
        if key == "": return
        elif key == "a": self.click_a(None)
        elif key == "b": self.click_b(None)
        elif key == "c": self.click_c(None)
        elif key == "d": self.click_d(None)
        elif key == "2": self.click_2(None)
        elif key == "8": self.click_8(None)
        elif key == ".": self.click_keypad_period(None)
        elif key == "backspace": self.click_keypad_backspace(None)
        else: self.click_keypad_number(None, key)

    def click_a(self, ev):
        flash_btn(self.frame_btn_a)
        self.on_btn_a()

    def click_b(self, ev):
        flash_btn(self.frame_btn_b)
        self.on_btn_b()

    def click_c(self, ev):
        flash_btn(self.frame_btn_c)
        self.on_btn_c()
        if self.close_on_first_field and self.sequence.cf == 0 and self.sequence.ce == 0: self.close()
        self.sequence.prev_field()
        self.update()

    def click_d(self, ev):
        flash_btn(self.frame_btn_d)

        c, v = self.sequence.get_current()
        valid = True

        # Get value
        if c['type'] == "current_time":
            if v is None: value = datetime.datetime.now().strftime("%H:%M:%S")
            else: value = v
        else:
            value = self.aux_input.get_value()
            valid = self.aux_input.validate()

        # Validate value
        if valid and "validate" in c:
            validate_function = c["validate"]
            if not validate_function(value): valid = False

        if not valid:
            self.label_value.setStyleSheet("color: red")
            self.label_units.setStyleSheet("color: red")
            return
        else:
            self.label_value.setStyleSheet("color: black")
            self.label_units.setStyleSheet("color: black")

        # Save value
        self.sequence.set_current(value)

        # Start / end chronometer
        if "chronometer" in c and v is None:
            if c['chronometer'] == "start": self.chronometer.start(c["title"])
            if c['chronometer'] == "end": self.chronometer.end()

        if "chronometer_label" in c and v is None:
            self.chronometer.text = c['chronometer_label']

        self.clock_tick()

        # Callback
        self.on_btn_d()

        # Go to next field
        if not self.sequence.next_field():
            self.on_sequence_end()
            self.sequence.add_entry()

        self.update()

    def click_2(self, ev):
        flash_btn(self.frame_btn_2)
        c, v = self.sequence.get_current()
        if c["type"] == "current_time": return
        self.label_value.setText(self.aux_input.write("2"))
        self.on_value_change()

    def click_8(self, ev):
        flash_btn(self.frame_btn_8)
        c, v = self.sequence.get_current()
        if c["type"] == "current_time": return
        self.label_value.setText(self.aux_input.write("8"))
        self.on_value_change()

    def click_keypad_number(self, ev, number):
        c, v = self.sequence.get_current()
        if c["type"] == "current_time": return
        self.label_value.setText(self.aux_input.write(number))
        self.on_value_change()

    def click_keypad_period(self, ev):
        c, v = self.sequence.get_current()
        if c["type"] == "current_time": return
        self.label_value.setText(self.aux_input.write("."))
        self.on_value_change()

    def click_keypad_backspace(self, ev):
        c, v = self.sequence.get_current()
        if c["type"] == "current_time": return
        self.label_value.setText(self.aux_input.clear())
        self.on_value_change()

    # --------------------------------------------------------------------------
    # Value setting
    # --------------------------------------------------------------------------
    def set_value(self, value):
        self.label_value.setText(self.aux_input.set_value(value))
        self.on_value_change()

    def label_value_clicked(self, ev):
        c, v = self.sequence.get_current()
        if c["type"] not in ["int", "float"]: return

        r = InputDialog.show_dialog(c["title"] + " - " + c["subtitle"], c, {"hide_keypad": False})
        if r is not None:
            self.set_value(r)
            self.on_value_change()
        self.setFocus()

    # --------------------------------------------------------------------------
    # Callbacks
    # --------------------------------------------------------------------------
    def on_btn_a(self): return
    def on_btn_b(self): return
    def on_btn_c(self): return
    def on_btn_d(self): return
    def on_sequence_end(self): return
    def on_field_load(self): return
    def on_value_change(self): return

    # --------------------------------------------------------------------------
    # Clock
    # --------------------------------------------------------------------------
    def clock_tick(self):
        t = datetime.datetime.today().strftime("%H:%M:%S")
        self.label_clock.setText(t)

        # Display clock / chronometer time on value label and bottom label
        if self.sequence is None: return
        c, v = self.sequence.get_current()

        if self.chronometer.enabled:
            t = self.chronometer.get_str_time()
            self.bottom_text = f'{self.chronometer.text}: {t}'
            self.label_text3.setText(self.bottom_text)
        else:
            self.bottom_text = ""
            self.label_text3.setText("")

        if c['type'] == "current_time" and v is None:
            self.label_value.setText(t)

    # --------------------------------------------------------------------------
    # Reset
    # --------------------------------------------------------------------------
    def reset(self):
        self.chronometer = Chronometer()
        self.sequence.reset()
        self.update()

