from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, QTimer, QObject, pyqtSignal
from ..common.get_res import get_res
from ..common import environment as env


# ===================================================================================
# Helper Class
# ===================================================================================
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(float)

    def __init__(self, parent):
        super(Worker, self).__init__()
        self.parent = parent

    def __do__(self):
        self.parent.do()
        self.finished.emit()


# ===================================================================================
# Main Class
# ===================================================================================
class LoadingScreen(QDialog):

    def __init__(self, title):
        super(LoadingScreen, self).__init__(None)

        # Optional
        self.min_wait = 2000

        # Load ui
        loadUi(get_res('ui/loading.ui'), self)
        self.label.setText(title)
        env.set_qtform(self, title)

        # Set click event
        self.mousePressEvent = self.__click__

        # Focus
        self.setFocus()

        # Create thread and worker
        self.thread = QThread()
        self.worker = Worker(self)
        self.timer_done = True
        self.task_done = True

    def do(self):
        pass

    def update_progress(self, progress):
        if self.task_done:
            self.__update_progress__(progress)
        else:
            self.worker.progress.emit(progress)

    def run(self):
        # Create timer
        self.timer_done = False
        timer = QTimer()
        timer.singleShot(self.min_wait, self.__timer_done__)

        # Create thread
        self.task_done = False
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.__update_progress__)
        self.worker.finished.connect(self.__task_done__)
        self.thread.started.connect(self.worker.__do__)
        self.thread.start()

        # Block other screens
        self.exec_()

    def __timer_done__(self):
        self.timer_done = True
        if self.task_done: self.close()

    def __task_done__(self):
        self.task_done = True
        if self.timer_done: self.close()

    def __update_progress__(self, progress):
        self.progressbar.setMaximum(100)
        self.progressbar.setValue(progress * 100)

    def __click__(self, ev):
        return

    # ===================================================================================
    # Simple executing method
    # ===================================================================================
    @staticmethod
    def show_dialog(title, function, **options):
        loading_screen = LoadingScreen(title)
        loading_screen.do = function

        # Options
        if "min_wait" in options:
            loading_screen.min_wait = options["min_wait"]

        # Run
        loading_screen.run()


"""
class Load(pt.LoadingScreen):

    def __init__(self):
        super().__init__("LOADING")
        self.min_wait = 1250
        self.run()
    
    def do(self):
        print("CACA")
        import time
        for i in range(0, 10):
            time.sleep(1)
            self.update_progress(i/10)
        self.close()
"""
