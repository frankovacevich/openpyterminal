from .list_simple import ListSimple
from PyQt5.QtWidgets import QDialog


class ListDialog(QDialog, ListSimple):

    def __init__(self, title, content):
        QDialog.__init__(self, None)
        ListSimple.__init__(self, title)

        self.options = content
        self.update()
        self.result = -1

    def on_btn_c(self):
        self.result = -1
        self.reject()

    def on_btn_d(self):
        if isinstance(self.options, list): self.result = self.selected_item
        elif isinstance(self.options, dict): self.result = self.options[list(self.options.keys())[self.selected_item]]
        self.accept()

    @staticmethod
    def show_dialog(title, content, options={}):
        dialog = ListDialog(title, content)

        if "hide_btn_d" in options and options["hide_btn_d"]: dialog.hide_btn("d")
        if "hide_btn_c" in options and options["hide_btn_c"]: dialog.hide_btn("c")
        if "icon_btn_d" in options: dialog.set_icon("d", options["icon_btn_d"])
        if "use_monospace_font" in options and options["use_monospace_font"]: dialog.use_monospace_font()

        dialog.exec_()
        return dialog.result
