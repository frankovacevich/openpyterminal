import os
from PyQt5.QtCore import Qt


def set(variable, value):
    os.environ[variable] = str(value)

def get(variable):
    if variable not in os.environ: return False
    v = os.environ[variable]
    if v == "True": v = True
    if v == "False": v = False
    return v

def set_qtform(form, title, icon=None):
    form.setWindowTitle(title)
    if get("FULLSCREEN_TERMINAL"):
        form.setWindowFlag(Qt.FramelessWindowHint)
        form.setCursor(Qt.BlankCursor)
        form.showFullScreen()
    else:
        form.show()
