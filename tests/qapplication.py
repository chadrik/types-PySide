from typing import Any, cast, overload

from PySide2.QtWidgets import QApplication


def slotAppStateChanged(*args: Any) -> None:
    pass


app = cast(QApplication, QApplication.instance())
app.applicationStateChanged.connect(slotAppStateChanged)
QApplication.processEvents()

# deactivated because of mypy bug: https://github.com/python/mypy/issues/7781
# app.processEvents()
