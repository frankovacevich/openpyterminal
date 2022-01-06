from PyQt5 import QtCore


def get_key(event):
    key = event.text()

    if event.key() == QtCore.Qt.Key_Up: key = "2"
    if event.key() == QtCore.Qt.Key_Down: key = "8"
    if event.key() == QtCore.Qt.Key_Left: key = "4"
    if event.key() == QtCore.Qt.Key_Right: key = "6"
    if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter: key = "d"
    if event.key() == QtCore.Qt.Key_Backspace: key = "backspace"
    if event.key() == QtCore.Qt.Key_Period: key = "."
    if event.key() == QtCore.Qt.Key_Escape: key = "c"
    if key == "+": key = "backspace"
    if key == "-": key = "."

    return key
