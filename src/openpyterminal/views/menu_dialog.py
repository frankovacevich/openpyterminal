from .menu_simple import MenuSimple
from PyQt5.QtWidgets import QDialog


class MenuDialog(QDialog, MenuSimple):

    def __init__(self, title, content):
        QDialog.__init__(self, None)
        MenuSimple.__init__(self, title)

        self.on_btn_c = self.btn_c
        self.on_option_selected = self.option_selected

        self.options = content
        self.update()
        self.result = -1

    def btn_c(self):
        self.result = -1
        self.reject()

    def option_selected(self):
        self.result = self.selected_item
        self.accept()

    @staticmethod
    def show_dialog(title, content, options={}):
        dialog = MenuDialog(title, content)
        dialog.exec_()
        return dialog.result
