import datetime

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.uic import loadUi

from ..common.get_res import get_res
from ..common.flash_btn import flash_btn
from ..common.timer import interval
from ..common.key_event import get_key
from ..common import environment as env


class ListExtended(QWidget):

    def __init__(self, title):
        super(ListExtended, self).__init__(None)
        self.title = title

        # More options
        self.options = []
        self.selected_item = -1

        # Load UI
        loadUi(get_res('ui/list.ui'), self)
        self.label_title.setText(self.title)
        self.frame_btn_c_alt_out.setHidden(True)
        self.frame_btn_d_alt_out.setHidden(True)

        if env.get("TOUCHSCREEN_TERMINAL"): self.as_touchscreen()

        # Set title, hide cursor, make full screen
        env.set_qtform(self, title)

        # Click events
        self.frame_btn_a.mousePressEvent = self.click_a
        self.frame_btn_b.mousePressEvent = self.click_b
        self.frame_btn_c.mousePressEvent = self.click_c
        self.frame_btn_d.mousePressEvent = self.click_d
        self.frame_btn_c_alt_out.mousePressEvent = self.click_c
        self.frame_btn_d_alt_out.mousePressEvent = self.click_d
        self.frame_btn_2_out.mousePressEvent = self.click_2
        self.frame_btn_8_out.mousePressEvent = self.click_8

        # Set clock
        self.clock_tick()
        interval(1000, self, self.clock_tick)

        # Set focus
        self.setFocus()

        # Some events
        self.listbox.itemClicked.connect(self.setFocus)
        self.listbox.currentItemChanged.connect(self.selection_changed)

    # --------------------------------------------------------------------------
    # GUI Methods
    # --------------------------------------------------------------------------

    def update(self):
        # Update listbox items
        aux_selected = self.selected_item
        if aux_selected == -1: aux_selected = 0
        if aux_selected > len(self.options): aux_selected = len(self.options) - 1

        self.listbox.clear()
        for option in self.options:
            opt = option[0] if isinstance(option, list) else option
            self.listbox.addItem(QListWidgetItem(opt))

        self.listbox.setCurrentRow(aux_selected)

    def as_touchscreen(self):
        self.label_btn_2.setHidden(True)
        self.label_btn_8.setHidden(True)
        self.label_btn_c_alt.setHidden(True)
        self.label_btn_d_alt.setHidden(True)
        self.label_btn_a.setHidden(True)
        self.label_btn_b.setHidden(True)
        self.label_btn_c.setHidden(True)
        self.label_btn_d.setHidden(True)

    def set_icon(self, btn, res):
        pixmap = QtGui.QPixmap()
        pixmap.load(get_res(res))

        if btn == "a": self.icon_btn_a.setPixmap(pixmap)
        if btn == "b": self.icon_btn_b.setPixmap(pixmap)
        if btn == "c":
            self.icon_btn_c.setPixmap(pixmap)
            self.icon_btn_c_alt.setPixmap(pixmap)
        if btn == "d":
            self.icon_btn_d.setPixmap(pixmap)
            self.icon_btn_d_alt.setPixmap(pixmap)

    def hide_btn(self, btn, hide=True):
        if btn == "a": self.frame_btn_a_in.setHidden(hide)
        if btn == "b": self.frame_btn_b_in.setHidden(hide)
        if btn == "c":
            self.frame_btn_c_in.setHidden(hide)
            self.frame_btn_c_alt_out.setHidden(hide)
        if btn == "d":
            self.frame_btn_d_in.setHidden(hide)
            self.frame_btn_d_alt_out.setHidden(hide)

    def use_monospace_font(self):
        self.listbox.setFont(QtGui.QFont("Ubuntu Mono", 20))

    # --------------------------------------------------------------------------
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

    def click_a(self, ev=None):
        flash_btn([self.frame_btn_a])
        self.on_btn_a()

    def click_b(self, ev=None):
        flash_btn([self.frame_btn_b])
        self.on_btn_b()

    def click_c(self, ev=None):
        flash_btn([self.frame_btn_c, self.frame_btn_c_alt])
        self.on_btn_c()

    def click_d(self, ev=None):
        flash_btn([self.frame_btn_d, self.frame_btn_d_alt])
        i = self.listbox.currentRow()
        if len(self.options) > 0 and isinstance(self.options, list) and isinstance(self.options[i], list):
            self.options[i][1]()
        self.on_btn_d()

    def click_2(self, ev=None):
        flash_btn(self.frame_btn_2)
        c = self.listbox.currentRow()
        if c > 0: self.listbox.setCurrentRow(c - 1)

    def click_8(self, ev=None):
        flash_btn(self.frame_btn_8)
        c = self.listbox.currentRow()
        if c + 1 < len(self.options): self.listbox.setCurrentRow(c + 1)

    def selection_changed(self):
        self.selected_item = self.listbox.currentRow()
        self.on_item_selected_change()

    # --------------------------------------------------------------------------
    # Callbacks
    # --------------------------------------------------------------------------
    def on_btn_a(self): return
    def on_btn_b(self): return
    def on_btn_c(self): self.close()
    def on_btn_d(self): return
    def on_item_selected_change(self): return

    # --------------------------------------------------------------------------
    # Clock
    # --------------------------------------------------------------------------
    def clock_tick(self):
        self.label_clock.setText(datetime.datetime.today().strftime("%H:%M:%S"))
