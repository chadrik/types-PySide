from PySide2 import QtWidgets

a: QtWidgets.QDialogButtonBox.StandardButtons
a = (
    QtWidgets.QDialogButtonBox.StandardButton.Ok
    | QtWidgets.QDialogButtonBox.StandardButton.Ok
)
assert isinstance(a, QtWidgets.QDialogButtonBox.StandardButtons)
d = (
    a | QtWidgets.QDialogButtonBox.StandardButton.Ok
)
assert isinstance(d, QtWidgets.QDialogButtonBox.StandardButtons)
e = a | a
