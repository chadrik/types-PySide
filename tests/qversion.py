from PySide2.QtCore import qVersion

s = ""  # type: str
s = qVersion()
assert isinstance(s, str)
