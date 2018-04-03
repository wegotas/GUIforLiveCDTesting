class InfoHolderClass:
    _title = ""
    _value = ""

    def __init__(self, title="", value=""):
        if title:
            self._title = title.lstrip()
        else:
            self._title = title
        if value:
            self._value = value.lstrip()
        else:
            self._value = value

    def set_value(self, value):
        self._value = value

    def get_title(self):
        return str(self._title)

    def get_value(self):
        return str(self._value)

    def toString(self):
        return str(self._title) + ": " + str(self._value)