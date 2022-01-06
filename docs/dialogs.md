# OpenPyTerminal Dialogs

In addition to views, you can display dialogs with OpenPyTerminal for the user to interact with. The available dialogs are:

* List dialog
* Menu dialog
* Message dialog
* Input dialog

Dialogs can be created with a single line of code. When a dialog is shown, the main view waits for the user's input.

All dialogs have the same constructor:
```python
Dialog.show_dialog(title, content, options={})
```

The options argument is optional and can be used to customize the dialog.

The user can accept or reject any dialog. Generally, the button "D" is used to accept and the button "C" to reject.

## Example

```python
import openpyterminal as pt


r = pt.MessageDialog.show_dialog(title="Title", content="Continue?", options={})
if r:
    pass # Continue
else:
    pass # Do not continue

```

## Message dialog

The message dialog can be used to display a message (text), ask a yes/no question, display HTML content or display an image.

### Content

The content can be:

* Simple text (string)
* HTML text (string)
* The path to an image (string)
* A list of any of the previous options (list)

If the content is passed as a list, the user will be able to navigate between the multiple messages with the "2" (up) and "8" (down) keys.

### Options

The following options can be set:

* `hide_btn_c` (boolean, default = False)
* `hide_btn_d` (boolean, default = False)
* `margin` (int, default = 20)
* `close_on_any_button` (boolean, default = False)
* `fullscreen` (boolean, default = False), hides the top bar
* `center_text` (boolean, default = False)


## Input dialog

The input dialog allows the user to insert a single value with the keypad (in case a touchscreen is used a keypad is displayed on the screen).

Returns the input value (int, string or float) or None if rejected.

### Content

The content is a dict that specifies the behavior of the dialog:

* `type`. Defines the type of variable that the user can input. Possible values: "int", "float", "date".
* `value`. The default value that the user will see when the dialog opens.
* `units`. The units that will be shown to the user to the right of the input box.
* `validate`. Function that validates the user input before closing the dialog. For example: `lambda x: x > 0 and x < 10`. Default = `None`. 
* `help`. Some help text for the user. Default = "".
* `date_format`. In case the user has to input a date, the format (using the datetime package convention). Default = `%Y-%m-%d`.


### Options

* `hide_btn_c` (boolean, default = False)
* `hide_btn_d` (boolean, default = False)
* `hide_keypad` (boolean, default = False)

### List dialog

The list dialog is a like a list view but when the user selects an item and clicks the button "D" (okay) the dialog is closed and the selected index is returned as the dialog result.

Returns the index of the selected item (int) or -1 if rejected.

### Content

The list of options for the user to choose from (list of string).

### Options

* `hide_btn_c` (boolean, default = False)
* `hide_btn_d` (boolean, default = False)
* `icon_btn_d` (string). Use the res path. Example: 'img/32/white/ok.svg'
* `use_monospace_font` (string, default = False)

## Menu dialog

Similar to the list dialog, the menu dialog is show a list of options and returns the index of the option selected by the user.

Returns the index of the selected item (int) or -1 if rejected.

### Content

The list of options for the user to choose from (list of string).

### Options

None





