import openpyterminal as pt


MY_ITEMS = []


class Sample2(pt.MenuSimple):

    def __init__(self):
        super().__init__("Main menu")
        self.options = [
            ["Open list", self.open_list],
            ["Add item", self.add_item],
            ["Remove all items", self.remove_all_items],
            ["Close", self.close],
        ]
        
        self.update()
        
    def open_list(self):
        pt.ListDialog.show_dialog("My items", MY_ITEMS, {'hide_btn_d': True})
        
    def add_item(self):
        r = pt.InputDialog.show_dialog("Add new item", {"type": "int", "help": "insert numeric value"})
        if r is not None:
            MY_ITEMS.append(str(r))
        
    def remove_all_items(self):
        if pt.MessageDialog.show_dialog("Remove all items", "Do you want to remove all items?"):
            MY_ITEMS.clear()
        
        
app = pt.TerminalApp(Sample2)
app.fullscreen = True
app.touchscreen = True
app.run()

