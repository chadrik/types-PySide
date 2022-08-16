from PySide2.QtWidgets import QTreeWidgetItem
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor


t = QTreeWidgetItem()

b = True  # type: bool
b = t < t
b = t == t
b = t != t

t.setForeground(3, QColor(Qt.red))
t.setBackground(3, QColor(Qt.red))

t.setData(0, Qt.ItemDataRole(33), "bla")
t.setData(0, Qt.ToolTipRole, "bla")

t.data(0,  Qt.ItemDataRole(33))
t.data(0, Qt.ToolTipRole)
