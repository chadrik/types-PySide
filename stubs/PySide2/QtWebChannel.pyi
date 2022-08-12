from typing import Callable, ClassVar, Dict, Union

import PySide2.QtCore
import typing
T = typing.TypeVar('T')

class QWebChannel(PySide2.QtCore.QObject):
    blockUpdatesChanged: ClassVar[PySide2.QtCore.Signal] = ...
    staticMetaObject: ClassVar[PySide2.QtCore.QMetaObject] = ...
    def __init__(self, parent: typing.Union[PySide2.QtCore.QObject,None] = ..., blockUpdates: bool = ..., blockUpdatesChanged: typing.Callable = ..., destroyed: typing.Callable = ..., objectName: str = ..., objectNameChanged: typing.Callable = ...) -> None: ...
    def blockUpdates(self) -> bool: ...
    def connectTo(self, transport: QWebChannelAbstractTransport) -> None: ...
    def deregisterObject(self, object: PySide2.QtCore.QObject) -> None: ...
    def disconnectFrom(self, transport: QWebChannelAbstractTransport) -> None: ...
    def registerObject(self, id: str, object: PySide2.QtCore.QObject) -> None: ...
    def registerObjects(self, objects: typing.Dict[str,PySide2.QtCore.QObject]) -> None: ...
    def registeredObjects(self) -> typing.Dict[str,PySide2.QtCore.QObject]: ...
    def setBlockUpdates(self, block: bool) -> None: ...

class QWebChannelAbstractTransport(PySide2.QtCore.QObject):
    messageReceived: ClassVar[PySide2.QtCore.Signal] = ...
    staticMetaObject: ClassVar[PySide2.QtCore.QMetaObject] = ...
    def __init__(self, parent: typing.Union[PySide2.QtCore.QObject,None] = ..., destroyed: typing.Callable = ..., objectName: str = ..., objectNameChanged: typing.Callable = ...) -> None: ...
    def sendMessage(self, message: typing.Dict[str,PySide2.QtCore.QJsonValue]) -> None: ...
