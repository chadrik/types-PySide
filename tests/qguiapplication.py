from typing import cast

from PySide2.QtGui import QGuiApplication
from PySide2.QtCore import Qt

app = cast(QGuiApplication, QGuiApplication.instance())
app.setOverrideCursor(Qt.CursorShape.WaitCursor)
