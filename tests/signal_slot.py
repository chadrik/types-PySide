import typing

from PySide2.QtCore import Signal, QObject, QMetaObject


class SomeClassWithSignal(QObject):
    signal_no_arg: typing.ClassVar[Signal] = Signal()
    signal_str: typing.ClassVar[Signal] = Signal(str)

    def __init__(self) -> None:
        super().__init__()  # note: this is mandatory for mypy to pickup the class attribute access

    def my_slot_no_arg(self) -> None:
        pass

    def my_slot_str(self, msg: str) -> None:
        pass


instance = SomeClassWithSignal()

connection = True
connection = instance.signal_no_arg.connect(instance.my_slot_no_arg)
instance.signal_no_arg.emit()
assert isinstance(connection, bool)

connection = instance.signal_str.connect(instance.my_slot_str)
instance.signal_str.emit("toto")
assert isinstance(connection, bool)

instance.signal_str.disconnect()

connection = instance.signal_str[str].connect(instance.my_slot_str)
instance.signal_str[str].emit("toto")
assert isinstance(connection, bool)

# instance.signal.disconnect(connection)

# SomeClassWithSignal.signal.__get__
# instance.signal[str].emit
