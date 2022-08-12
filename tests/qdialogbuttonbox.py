from PySide2 import QtWidgets

a: QtWidgets.QDialogButtonBox.StandardButtons
a = (
    QtWidgets.QDialogButtonBox.StandardButton.Ok
    | QtWidgets.QDialogButtonBox.StandardButton.Ok
)
d = (
    a | QtWidgets.QDialogButtonBox.StandardButton.Ok
)  # type: QtWidgets.QDialogButtonBox.StandardButtons
e = a | a  # type: QtWidgets.QDialogButtonBox.StandardButtons
