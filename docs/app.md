# OpenPyTerminal apps

To create a new app, first create a class that inherits one of the main views. See the example (from sample1.py):

## Example

```python
import openpyterminal as pt


class Sample1(pt.ListSimple):

    def __init__(self):
        super().__init__("Terminal")
        self.options = [
            ["Option 1", lambda: self.select_option("1")],
            ["Option 2", lambda: self.select_option("2")],
            ["Option 3", lambda: self.select_option("3")],
            ["Option 4", lambda: self.select_option("4")],
            ["Exit", self.close]
        ]
        
        self.update()
        
    def select_option(self, number):
        pt.MessageDialog.show_dialog("Dialog Example", f"You have selected option {number}", {'hide_btn_c': True})
        
# Use these lines to create an OpenPyTerminal App
app = pt.TerminalApp(Sample1)
app.fullscreen = True
app.touchscreen = False
app.run()
```

You can also use your own custom class that uses PyQt to display a QWidget.

