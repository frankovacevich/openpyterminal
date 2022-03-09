from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt5.uic import loadUi

from ..common.get_res import get_res
from ..common.flash_btn import flash_btn
from ..common.key_event import get_key
from ..common import environment as env


class MenuSimple(QWidget):

    def __init__(self, title):
        super(MenuSimple, self).__init__(None)
        self.title = title

        # More options
        self.options = []

        # Load UI
        loadUi(get_res('ui/menu.ui'), self)
        self.label_title.setText(self.title)
        self.spacer_c.setHidden(True)

        # Set title, hide cursor, make full screen
        env.set_qtform(self, title)

        # List of Buttons
        self.buttons = [
            (self.frame_btn_1_out, self.frame_btn_1, self.label_btn_1, self.label_1),
            (self.frame_btn_2_out, self.frame_btn_2, self.label_btn_2, self.label_2),
            (self.frame_btn_3_out, self.frame_btn_3, self.label_btn_3, self.label_3),
            (self.frame_btn_4_out, self.frame_btn_4, self.label_btn_4, self.label_4),
            (self.frame_btn_5_out, self.frame_btn_5, self.label_btn_5, self.label_5),
            (self.frame_btn_6_out, self.frame_btn_6, self.label_btn_6, self.label_6),
            (self.frame_btn_7_out, self.frame_btn_7, self.label_btn_7, self.label_7),
            (self.frame_btn_8_out, self.frame_btn_8, self.label_btn_8, self.label_8),
            (self.frame_btn_9_out, self.frame_btn_9, self.label_btn_9, self.label_9),
            (self.frame_btn_10_out, self.frame_btn_10, self.label_btn_10, self.label_10),
        ]

        # Click events
        self.frame_btn_c.mousePressEvent = self.click_c
        for b in range(0, len(self.buttons)):
            self.buttons[b][0].mousePressEvent = lambda ev, b=b: self.click_number(ev, b+1)

        # Set focus
        self.setFocus()

        # Touchscreen
        self.touchscreen = False
        if env.get("TOUCHSCREEN_TERMINAL"): self.as_touchscreen()

        # Aux
        self.selected_item = -1

    def update(self):
        # Update menu items
        if len(self.options) > 10: self.options = self.options[0:10]

        for i in range(0, len(self.options)):
            opt = self.options[i]
            if isinstance(opt, list): opt = opt[0]
            self.buttons[i][3].setText(opt)

        for i in range(len(self.options), 10):
            self.buttons[i][0].setHidden(True)

    def hide_btn_c(self):
        self.frame_btn_c_out.setHidden(True)
        self.spacer_c.setHidden(False)

    def as_touchscreen(self):
        self.touchscreen = True
        self.label_btn_c.setHidden(True)

        for b in self.buttons:
            b[1].setHidden(True)
            b[0].setStyleSheet('border-radius: 10px; border: 1px solid #cccccc;')
            b[3].setStyleSheet('border: none')
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setOffset(3)
            b[0].setGraphicsEffect(shadow)

    def set_icon(self, btn, res):
        pixmap = QtGui.QPixmap()
        pixmap.load(get_res(res))
        if btn == "c": self.icon_btn_c.setPixmap(pixmap)

    def keyPressEvent(self, event):
        key = get_key(event)
        if key == "": return
        elif key == "c": self.click_c(None)
        elif key in "0123456789": self.click_number(None, int(key))

    def click_c(self, ev):
        flash_btn(self.frame_btn_c)
        self.on_btn_c()

    def click_number(self, ev, number):
        # Get number
        n = number - 1
        if n == -1: n = 9
        if n >= len(self.options): return
        self.selected_item = n

        # Flash button
        if not self.touchscreen: flash_btn(self.buttons[n][1])
        else: flash_btn(self.buttons[n][0])

        # Callback 1
        if isinstance(self.options[n], list): self.options[n][1]()

        # Callback 2
        self.on_option_selected()

    # --------------------------------------------------------------------------
    # Callbacks
    # --------------------------------------------------------------------------
    def on_btn_c(self): self.close()
    def on_option_selected(self): return
