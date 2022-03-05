import time
from PyQt5.QtCore import QEventLoop
from PyQt5.Qt import QTimer


def sleep(ms):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()


def interval(ms, parent, function):
    timer = QTimer(parent)
    timer.timeout.connect(function)
    timer.start(ms)


def timeout(ms, function):
    QTimer.singleShot(ms, function)


def seconds_to_hh_mm_ss(duration, include_hours=True):
    import math
    duration_hh = math.floor(duration / 3600)
    duration_mm = math.floor((duration - duration_hh * 3600) / 60)
    duration_ss = math.floor(duration - duration_hh * 3600 - duration_mm * 60)
    if include_hours:
        return aux_pad(duration_hh) + ":" + aux_pad(duration_mm) + ":" + aux_pad(duration_ss)
    else:
        return aux_pad(duration_mm) + ":" + aux_pad(duration_ss)


def aux_pad(v):
    if v < 10:
        return "0" + str(v)
    return str(v)


class Chronometer:

    def __init__(self):
        self.t = time.time()
        self.enabled = False
        self.text = ""

    def start(self, text):
        self.t = time.time()
        self.text = text
        self.enabled = True

    def end(self):
        self.enabled = False
        self.text = ""

    def get_str_time(self):
        chrtime = time.time() - self.t
        return seconds_to_hh_mm_ss(chrtime, False)
