"""

Options can are set as environment variables

"""


import sys
from PyQt5.QtWidgets import QApplication
from .common import environment as env


class TerminalApp:

    def __init__(self, main_view):
        self.app = QApplication(sys.argv)
        self.view = main_view

        # Extra options
        self.touchscreen = True
        self.fullscreen = True

    def run(self):
        env.set("TOUCHSCREEN_TERMINAL", self.touchscreen)
        env.set("FULLSCREEN_TERMINAL", self.fullscreen)

        self.view = self.view()
        sys.exit(self.app.exec_())

    def stop(self):
        exit()
