from PyQt5.QtWidgets import QWidget


class LoadingScreen(QWidget):

    def __init__(self, title):
        super(LoadingScreen, self).__init__()
        self.label.setText(title)

    def update_progress(self, progress):
        self.progressbar.maximum = 1
        self.progressbar.value = progress
