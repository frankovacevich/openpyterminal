import openpyterminal as pt
import datetime


# This app will get some user input and display the records created

# Here is the list of records with a sample record already created
RECORDS = [
    {
        "user": "John Doe",
        "date": "2021-12-01",
        "timestamp": datetime.datetime.now(),
        "qty": 112,
        "temperature": 25.2,
        "ready": True,
    }
]

# Sequence of steps that the user has to fill in to create a new record
SEQUENCE = [
    {
        "name": "user",
        "title": "User",
        "subtitle": "",
        "type": "options",
        "options": ["John Doe", "Mark Twain", "Sarah Sanchez"],
    },
    {
        "name": "date",
        "title": "Date",
        "subtitle": "",
        "type": "date",
    },
    {
        "name": "time",
        "title": "Time",
        "subtitle": "",
        "type": "time",
    },
    {
        "name": "current_time",
        "title": "Current Time",
        "subtitle": "",
        "type": "current_time",
    },
    {
        "name": "qty",
        "title": "Quantity",
        "subtitle": "(count)",
        "type": "int",
    },
    {
        "name": "temperature",
        "title": "Temperature",
        "subtitle": "(last measurement)",
        "units": "°C",
        "type": "float",
        "default": 25.0,
    },
    {
        "name": "ready",
        "title": "Status", 
        "subtitle": "",
        "type": "options",
        "options": {"ready": True, "not ready": False}
    },
    
]


# The main view will be a list with all the records and options to add, remove and view the records.
class Sample3(pt.ListExtended):
    
    def __init__(self):
        super().__init__("Sample 3")
        self.set_icon("a", "img/32/white/eye.svg")
        self.set_icon("c", "img/32/white/trash.svg")
        self.set_icon("d", "img/32/white/add-box-fill.svg")
        self.update_options()
    
    def update_options(self):
        options = []
        for i in range(0, len(RECORDS)):
            r = RECORDS[i]
            options.append(f"Record #{i + 1}\t\tQty: {r['qty']}\t\tReady: {r['ready']}")
        
        self.options = options
        self.update()
        
    # New
    def on_btn_d(self):
        CreateRecordSequence(self)
    
    # Delete
    def on_btn_c(self):
        if len(RECORDS) == 0 or self.selected_item < 0 or self.selected_item > len(RECORDS) - 1: return
        if pt.MessageDialog.show_dialog("Delete record", f"Do you want to delete record #{self.selected_item + 1}?"):
            RECORDS.pop(self.selected_item)
            self.update_options()

    # Menu
    def on_btn_b(self):
        pt.MenuDialog.show_dialog("Menu", [["Close", self.close]])
            
    # Details  
    def on_btn_a(self):
        r = RECORDS[self.selected_item]
        details = "Record details:\n\n"
        details += f"User: {r['user']}\n"
        details += f"Date: {r['date']}\n"
        details += f"Quantity: {r['qty']}\n"
        details += f"Temperature: {r['temperature']}°C\n"
        details += f"Ready: {r['ready']}\n"
        details += f"Timestamp: {r['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        pt.MessageDialog.show_dialog(f"Record #{self.selected_item + 1}", details, {"hide_btn_d": True})
          

# The records are created by the user with a sequence
class CreateRecordSequence(pt.InputSequence):

    def __init__(self, parent):
        super().__init__("Create new record")

        self.parent = parent
        self.close_on_first_field = True
        self.date_format = "%Y-%m-%d"
        self.sequence = pt.Sequence(SEQUENCE)
        self.update()
        
    # Menu
    def on_btn_b(self):
        pt.MenuDialog.show_dialog("Options", [["Cancel", self.close]])
    
    # When finished
    def on_sequence_end(self):
        new_record = self.sequence.get_entry()
        new_record["timestamp"] = datetime.datetime.now()
        print(new_record)
        
        RECORDS.append(new_record)
        self.parent.update_options()
        self.close()
        

# Create and run app
app = pt.TerminalApp(Sample3)
app.fullscreen = True
app.touchscreen = False
app.run()
