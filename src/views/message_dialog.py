"""
Display text, images or html
"""

import datetime

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from ..bin.get_res import get_res
from ..bin.flash_btn import flash_btn
from ..bin.timer import timeout
from ..bin.key_event import get_key
from ..bin import environment as env


class MessageDialog(QDialog):

    def __init__(self, title, content):
        super(MessageDialog, self).__init__(None)
        self.title = title
        self.content = content if isinstance(content, list) else [content]
        self.current = 0

        # More options
        self.close_on_any_button = False

        # Load UI
        ui = 'ui/message1.ui' if len(self.content) == 1 else 'ui/message2.ui'
        loadUi(get_res(ui), self)

        # Set title, hide cursor, make full screen
        env.set_qtform(self, title)

        self.label_title.setText(title)
        self.bottom_bar.setHidden(True)
        self.frame_btn_b_out.setHidden(True)
        self.frame_btn_a_out.setHidden(True)
        self.spacer_c.setHidden(True)
        self.spacer_d.setHidden(True)
        self.label_text.setMargin(40)

        if env.get("TOUCHSCREEN_TERMINAL"): self.as_touchscreen()

        # Click events
        self.frame_btn_c.mousePressEvent = self.click_c
        self.frame_btn_d.mousePressEvent = self.click_d
        self.frame_btn_2_out.mousePressEvent = self.click_2
        self.frame_btn_8_out.mousePressEvent = self.click_8

        # Set focus
        self.setFocus()
        timeout(20, self.update)

        # Preset result
        self.result = False

    def update(self):
        c = self.content[self.current]

        if c[-4:] in [".jpg", ".png", ".gif", ".svg"]:
            pxmap = QtGui.QPixmap(c)
            w = 2 * self.label_text.margin()
            pxmap = pxmap.scaled(self.label_text.width() - w, self.label_text.height() - w)
            self.label_text.setPixmap(pxmap)
        else:
            self.label_text.setText(c)

        if len(self.content) > 1:
            self.label_title.setText(f"{self.title} ({str(self.current + 1)}/{str(len(self.content))})")

    def set_icon(self, btn, res):
        pixmap = QtGui.QPixmap()
        pixmap.load(get_res(res))
        if btn == "a": self.icon_btn_c.setPixmap(pixmap)
        if btn == "b": self.icon_btn_d.setPixmap(pixmap)
        if btn == "c": self.icon_btn_c.setPixmap(pixmap)
        if btn == "d": self.icon_btn_d.setPixmap(pixmap)

    def hide_btn_c(self):
        self.frame_btn_c_out.setHidden(True)
        self.spacer_c.setHidden(False)

    def hide_btn_d(self):
        self.frame_btn_d_out.setHidden(True)
        self.spacer_d.setHidden(False)

    def hide_top_bar(self):
        self.top_bar.setHidden(True)

    def as_touchscreen(self):
        self.label_btn_c.setHidden(True)
        self.label_btn_d.setHidden(True)
        self.label_btn_2.setHidden(True)
        self.label_btn_8.setHidden(True)

    def center_text(self):
        self.label_text.setAlignment(QtCore.Qt.AlignCenter)

    def keyPressEvent(self, event):
        key = get_key(event)
        if key == "": return
        elif self.close_on_any_button: self.reject()
        elif key == "2": self.click_2(None)
        elif key == "8": self.click_8(None)
        elif key == "a": self.click_a(None)
        elif key == "b": self.click_b(None)
        elif key == "c": self.click_c(None)
        elif key == "d": self.click_d(None)

    def click_a(self, ev):
        flash_btn(self.frame_btn_a)
        self.on_btn_a()

    def click_b(self, ev):
        flash_btn(self.frame_btn_b)
        self.on_btn_b()

    def click_c(self, ev):
        flash_btn(self.frame_btn_c)
        self.on_btn_c()
        self.result = False
        self.reject()

    def click_d(self, ev):
        flash_btn(self.frame_btn_d)
        self.on_btn_d()
        self.result = True
        self.accept()

    def click_2(self, ev):
        flash_btn(self.frame_btn_2)
        if self.current > 0:
            self.current -= 1
            self.update()
        self.on_message_change()

    def click_8(self, ev):
        flash_btn(self.frame_btn_8)
        if self.current + 1 < len(self.content):
            self.current += 1
            self.update()
        self.on_message_change()

    # --------------------------------------------------------------------------
    # Callbacks
    # --------------------------------------------------------------------------
    def on_btn_a(self): return
    def on_btn_b(self): return
    def on_btn_c(self): return
    def on_btn_d(self): return
    def on_message_change(self): return

    @staticmethod
    def show_dialog(title, content, options={}):
        dialog = MessageDialog(title, content)

        if "hide_btn_c" in options and options["hide_btn_c"]: dialog.hide_btn_c()
        if "hide_btn_d" in options and options["hide_btn_d"]: dialog.hide_btn_d()
        if "margin" in options: dialog.label_text.setMargin(options["margin"])
        if "close_on_any_button" in options and options["close_on_any_button"]: dialog.close_on_any_button = True
        if "fullscreen" in options and options["fullscreen"]: dialog.hide_top_bar()
        if "center_text" in options and options["center_text"]: dialog.center_text()

        dialog.exec_()
        return dialog.result
