# OpenPyTerminal views

OpenPyTerminal provides three main views to use as menus or main screens. They are:

* Menu
* List simple
* List extended

They are all used to display a set of options. Menus (see sample2.py) can only display up to 10 options, but the user can select an option faster than with lists (see sample1.py).

Extended lists (see sample3.py) are like simple lists but have a side bar with more options.

## Example:

```python
class MainView(pt.ListExtended):
    def __init__(self):
        super().__init__("Title")
        
        # Set and display options
        self.options(["list", "of", "options"])
        self.update()
        
    # Override button A
    def on_btn_a(self):
        print("Button A clicked")
```

The three views have a property called `options` that is used to display the different elements of the menu or list. It can be a list of string or a list of lists: [["Option text", function], ...]. When a list of lists is used, the first item is the text displayed for that option and the second item is the function called when the option is selected.

You must call the `update()` function to load the options into the view.

NOTE: lists and menus can be dialogs too.

## Methods and properties

### List extended

* Use `set_icon(btn_id, res)` to change the icon of a button. The `btn_id` can be the string "a", "b", "c" or "d". The `res` is the string to the resource (see the openpyterminal/res folder). For example: `img/32/black/home.svg`.

* Use `hide_btn(btn_id, hide=True)` to hide/show a button. The `btn_id` can be the string "a", "b", "c" or "d".

* Use `set_monospace_font()` to use a monospace font.

* Override the buttons "a", "b", "c" and "d" with the functions `on_btn_a()`, `on_btn_b()`, `on_btn_c()` and `on_btn_d()`. The button "c" by default closes the view, the others have no effect.

* Override the function `on_item_selected_change()` for a callback when the user changed the selected item.

* The property `selected_item` gives the index of the selected option (defaults to -1 if the options are empty).


### List simple

All the methods inhereted from list extended, plus:

* Use `hide_btn_c()` to hide the 'C' (close) button.


### Menu

* Use `hide_btn_c()` to hide the 'C' (close) button.

* Use `set_icon(btn_id, res)` to change the icon of a btn (see the same method under list extended). Currently the only button displayed is the "C" button.

* Overrde the button "C" effect with `on_btn_c()`.

* Override the function `on_option_selected()` for a callback when the user selected an option. 

