from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap

emptyPixmap = QPixmap(16, 16)
emptyPixmap.fill(Qt.transparent)
emptyPixmap.fill("white")
emptyPixmap.fill(0xFFFFFF)
