import datetime


class InputHelper:

    def __init__(self, input_type="", date_format="%d/%m/%y", options={}):
        self.type = input_type  # int, float, date, options, time, generic

        # Only useful if type == date
        self.date_format = date_format

        # Only options if type == options
        if isinstance(options, list): options = {x: x for x in options}
        self.options = options
        self.options_keys = list(options.keys())

        if input_type == "date": self.value = self.today()
        elif input_type == "time": self.value = self.current_time()
        elif input_type == "int": self.value = "0"
        elif input_type == "float": self.value = "0"
        elif input_type == "options" and len(options) > 0: self.value = self.options_keys[0]
        else: self.value = ""

    def set_date_format(self, date_format):
        self.date_format = date_format
        if self.type == "date": self.value = self.today()

    def get_value(self):
        if not self.validate(): return None

        if self.type == "int": return int(self.value)
        elif self.type == "float": return float(self.value)
        elif self.type == "options": return self.options[self.value]
        elif self.type == "time": return self.value
        return self.value

    def write(self, text):
        text = str(text)

        # Decimal separator
        if text == ".":
            if self.type != "date" and self.type != "time" and self.type != "int":
                self.value += "."

        # Number
        elif text.isdigit():
            if self.type == "date":
                if "_" not in self.value:
                    t = self.today()
                    for i in "0123456789": t = t.replace(i, "_")
                    self.value = t

                t = list(self.value)
                i = t.index("_")
                t[i] = text
                self.value = "".join(t)

            elif self.type == "time":
                if "_" not in self.value: self.value = "__:__:__"
                t = list(self.value)
                i = t.index("_")
                t[i] = text
                self.value = "".join(t)

            elif self.type in ["int", "float"] and self.value == "0":
                self.value = text

            elif self.type == "options":
                if len(self.options) == 0:
                    pass
                elif self.value not in self.options:
                    self.value = self.options_keys[0]
                else:
                    if text == "2":
                        idx = self.options_keys.index(self.value)
                        if idx + 1 < len(self.options_keys): self.value = self.options_keys[idx + 1]
                        else: self.value = self.options_keys[0]

                    elif text == "8":
                        idx = self.options_keys.index(self.value)
                        if idx < 0: idx = 0
                        self.value = self.options_keys[idx - 1]

            else:
                self.value += text

        # Other text
        else:
            if self.type not in ["int", "float", "date", "time", "options"]:
                self.value += text

        return self.value

    def clear(self):
        if self.type == "date":
            self.value = self.today()

        elif self.type == "time":
            self.value = self.current_time()

        elif self.type == "options":
            self.value = self.options_keys[0]

        elif len(self.value) > 0:
            self.value = self.value[0:-1]

        return self.value

    def validate(self):
        if self.type == "date":
            try: datetime.datetime.strptime(self.value, self.date_format)
            except: return False

        elif self.type == "time":
            try: datetime.datetime.strptime(self.value, "%H:%M:%S")
            except: return False

        elif self.type == "int":
            try: int(self.value)
            except: return False

        elif self.type == "float":
            try: float(self.value)
            except: return False

        elif self.type == "options":
            if self.value not in self.options: return False

        return True

    def today(self):
        return datetime.datetime.today().strftime(self.date_format)

    def current_time(self):
        return datetime.datetime.today().strftime("%H:%M:%S")
