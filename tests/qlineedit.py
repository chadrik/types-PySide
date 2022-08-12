"""Tests for QLineEdit."""
from PySide2.QtWidgets import QApplication, QLineEdit

# test that QLineEdit.setText() accepts None as parameter
edit = QLineEdit()
edit.setText(None)
