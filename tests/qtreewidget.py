from typing import Optional

from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem

t = QTreeWidget()
item = t.topLevelItem(400)
# default type returned by topLevelItem() should allow None value
item = None
