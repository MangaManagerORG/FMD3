from tkinter import Variable


class KeyPair:
    def __init__(self, title: str, value: str,label=False):
        self.title = title or ""
        self.value = value or ""
        self.label = label

    def is_label(self):
        return self.label

    def __str__(self):
        return self.title

    def ljust(self, __width, __fillchar=" "):
        return self.title.ljust(__width, __fillchar)


class ObjectVar(Variable):
    _object: object = None

    def get(self) -> object:
        return self._object

    def set(self, value: object):
        return self._object


class KeyPairVar(ObjectVar):
    """
    Implements a key-value object that can be saved in a tkinter variable
    """

    def __init__(self, master=None, value=None, name=None):
        """Construct a variable

        MASTER can be given as master widget.
        VALUE is an optional value (defaults to "")
        NAME is an optional Tcl name (defaults to PY_VARnum).

        If NAME matches an existing variable and VALUE is omitted
        then the existing value is retained.
        """

        self._object: KeyPair = value
        super().__init__(master=master, name=name)

    def set(self, value: KeyPair):
        self._object = value

    def get(self) -> KeyPair:
        return self._object


