from typing import Optional

from PySide2 import QtCore, QtWidgets

t = QtWidgets.QTreeWidget()
item = t.topLevelItem(400)
assert item is None
# default type returned by topLevelItem() should allow None value
item = None
