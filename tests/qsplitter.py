from PySide2.QtWidgets import QSplitter
from PySide2.QtCore import QByteArray

s = QSplitter()
b = s.saveState()
assert isinstance(b, QByteArray)
