from __future__ import absolute_import, print_function

from PySide2 import QtCore
ba = QtCore.QByteArray(b'foo')
b: bytes
b = ba[0]
assert isinstance(b, bytes)
b = bytes(ba)
