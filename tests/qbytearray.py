from __future__ import absolute_import, print_function

from PySide2 import QtCore
byte_array = QtCore.QByteArray(b'foo')
b: bytes
b = byte_array[0]
assert isinstance(b, bytes)
b = bytes(byte_array)

x: bytes
for x in byte_array:
    assert isinstance(x, bytes)
