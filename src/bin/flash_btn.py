from . import timer


def flash_btn(btn):

    if not isinstance(btn, list): btn = [btn]
    stylesheets = []

    for i in range(0, len(btn)):
        b = btn[i]
        s = b.styleSheet()
        stylesheets.append(s)
        b.setStyleSheet(s + f";background-color: #000000;")

    timer.sleep(40)

    for i in range(0, len(btn)):
        btn[i].setStyleSheet(stylesheets[i])


class CycleFlashBtn:

    def __init__(self, btn, color="#000000"):
        self.btn = btn
        self.color = color
        self.stylesheet = btn.styleSheet()
        self.state = True
        self.is_on = False

    def on(self):
        if self.is_on: return
        self.is_on = True
        self.__cycle__()

    def off(self):
        if not self.is_on: return
        self.is_on = False
        self.btn.setStyleSheet(self.stylesheet)

    def __cycle__(self):
        if not self.is_on: return

        if self.state:
            self.btn.setStyleSheet(self.stylesheet + f";background-color: {self.color};")
        else:
            self.btn.setStyleSheet(self.stylesheet)

        # Change state
        self.state = not self.state

        # Next step
        timer.timeout(500, lambda: self.__cycle__())


def cycle_flash_btn(btn, color="#000000"):
    return CycleFlashBtn(btn, color)
