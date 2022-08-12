from typing import Any, Callable, ClassVar, List, Union

from typing import overload
import PySide2.QtCore
import PySide2.QtNetwork
import shiboken2
import typing
T = typing.TypeVar('T')

class QMaskGenerator(PySide2.QtCore.QObject):
    destroyed: ClassVar[PySide2.QtCore.Signal] = ...
    objectNameChanged: ClassVar[PySide2.QtCore.Signal] = ...
    staticMetaObject: ClassVar[PySide2.QtCore.QMetaObject] = ...
    def __init__(self, parent: typing.Union[PySide2.QtCore.QObject,None] = ..., destroyed: typing.Callable = ..., objectName: str = ..., objectNameChanged: typing.Callable = ...) -> None: ...
    def nextMask(self) -> int: ...
    def seed(self) -> bool: ...

class QWebSocket(PySide2.QtCore.QObject):
    aboutToClose: ClassVar[PySide2.QtCore.Signal] = ...
    binaryFrameReceived: ClassVar[PySide2.QtCore.Signal] = ...
    binaryMessageReceived: ClassVar[PySide2.QtCore.Signal] = ...
    bytesWritten: ClassVar[PySide2.QtCore.Signal] = ...
    connected: ClassVar[PySide2.QtCore.Signal] = ...
    disconnected: ClassVar[PySide2.QtCore.Signal] = ...
    error: ClassVar[PySide2.QtCore.Signal] = ...
    pong: ClassVar[PySide2.QtCore.Signal] = ...
    preSharedKeyAuthenticationRequired: ClassVar[PySide2.QtCore.Signal] = ...
    proxyAuthenticationRequired: ClassVar[PySide2.QtCore.Signal] = ...
    readChannelFinished: ClassVar[PySide2.QtCore.Signal] = ...
    sslErrors: ClassVar[PySide2.QtCore.Signal] = ...
    stateChanged: ClassVar[PySide2.QtCore.Signal] = ...
    staticMetaObject: ClassVar[PySide2.QtCore.QMetaObject] = ...
    textFrameReceived: ClassVar[PySide2.QtCore.Signal] = ...
    textMessageReceived: ClassVar[PySide2.QtCore.Signal] = ...
    def __init__(self, origin: str = ..., version: QWebSocketProtocol.Version = ..., parent: typing.Union[PySide2.QtCore.QObject,None] = ..., aboutToClose: typing.Callable = ..., binaryFrameReceived: typing.Callable = ..., binaryMessageReceived: typing.Callable = ..., bytesWritten: typing.Callable = ..., connected: typing.Callable = ..., destroyed: typing.Callable = ..., disconnected: typing.Callable = ..., error: typing.Callable = ..., objectName: str = ..., objectNameChanged: typing.Callable = ..., pong: typing.Callable = ..., preSharedKeyAuthenticationRequired: typing.Callable = ..., proxyAuthenticationRequired: typing.Callable = ..., readChannelFinished: typing.Callable = ..., sslErrors: typing.Callable = ..., stateChanged: typing.Callable = ..., textFrameReceived: typing.Callable = ..., textMessageReceived: typing.Callable = ...) -> None: ...
    def abort(self) -> None: ...
    def bytesToWrite(self) -> int: ...
    def close(self, closeCode: QWebSocketProtocol.CloseCode = ..., reason: str = ...) -> None: ...
    def closeCode(self) -> QWebSocketProtocol.CloseCode: ...
    def closeReason(self) -> str: ...
    def errorString(self) -> str: ...
    def flush(self) -> bool: ...
    def isValid(self) -> bool: ...
    def localAddress(self) -> PySide2.QtNetwork.QHostAddress: ...
    def localPort(self) -> int: ...
    def maskGenerator(self) -> QMaskGenerator: ...
    def maxAllowedIncomingFrameSize(self) -> int: ...
    def maxAllowedIncomingMessageSize(self) -> int: ...
    @classmethod
    def maxIncomingFrameSize(cls) -> int: ...
    @classmethod
    def maxIncomingMessageSize(cls) -> int: ...
    @classmethod
    def maxOutgoingFrameSize(cls) -> int: ...
    @overload
    def open(self, request: PySide2.QtNetwork.QNetworkRequest) -> None: ...
    @overload
    def open(self, url: PySide2.QtCore.QUrl) -> None: ...
    def origin(self) -> str: ...
    def outgoingFrameSize(self) -> int: ...
    def pauseMode(self) -> typing.Union[PySide2.QtNetwork.QAbstractSocket.PauseModes,PySide2.QtNetwork.QAbstractSocket.PauseMode]: ...
    def peerAddress(self) -> PySide2.QtNetwork.QHostAddress: ...
    def peerName(self) -> str: ...
    def peerPort(self) -> int: ...
    def ping(self, payload: typing.Union[PySide2.QtCore.QByteArray,bytes] = ...) -> None: ...
    def proxy(self) -> PySide2.QtNetwork.QNetworkProxy: ...
    def readBufferSize(self) -> int: ...
    def request(self) -> PySide2.QtNetwork.QNetworkRequest: ...
    def requestUrl(self) -> PySide2.QtCore.QUrl: ...
    def resourceName(self) -> str: ...
    def resume(self) -> None: ...
    def sendBinaryMessage(self, data: typing.Union[PySide2.QtCore.QByteArray,bytes]) -> int: ...
    def sendTextMessage(self, message: str) -> int: ...
    def setMaskGenerator(self, maskGenerator: QMaskGenerator) -> None: ...
    def setMaxAllowedIncomingFrameSize(self, maxAllowedIncomingFrameSize: int) -> None: ...
    def setMaxAllowedIncomingMessageSize(self, maxAllowedIncomingMessageSize: int) -> None: ...
    def setOutgoingFrameSize(self, outgoingFrameSize: int) -> None: ...
    def setPauseMode(self, pauseMode: typing.Union[PySide2.QtNetwork.QAbstractSocket.PauseModes,PySide2.QtNetwork.QAbstractSocket.PauseMode]) -> None: ...
    def setProxy(self, networkProxy: PySide2.QtNetwork.QNetworkProxy) -> None: ...
    def setReadBufferSize(self, size: int) -> None: ...
    def state(self) -> PySide2.QtNetwork.QAbstractSocket.SocketState: ...
    def version(self) -> QWebSocketProtocol.Version: ...

class QWebSocketCorsAuthenticator(shiboken2.Object):
    @overload
    def __init__(self, origin: str) -> None: ...
    @overload
    def __init__(self, other: QWebSocketCorsAuthenticator) -> None: ...
    def allowed(self) -> bool: ...
    def origin(self) -> str: ...
    def setAllowed(self, allowed: bool) -> None: ...
    def swap(self, other: QWebSocketCorsAuthenticator) -> None: ...

class QWebSocketProtocol(shiboken2.Object):
    class CloseCode:
        CloseCodeAbnormalDisconnection: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeBadOperation: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeDatatypeNotSupported: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeGoingAway: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeMissingExtension: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeMissingStatusCode: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeNormal: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodePolicyViolated: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeProtocolError: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeReserved1004: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeTlsHandshakeFailed: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeTooMuchData: ClassVar[QWebSocketProtocol.CloseCode] = ...
        CloseCodeWrongDatatype: ClassVar[QWebSocketProtocol.CloseCode] = ...
        values: ClassVar[dict] = ...
        name: Any
        @classmethod
        def __init__(cls, *args, **kwargs) -> None: ...
        def __add__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __and__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __bool__(self) -> bool: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> Any: ...
        def __int__(self) -> int: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __mul__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __pos__(self) -> Any: ...
        def __radd__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __rand__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __rmul__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __ror__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __rsub__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __rxor__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __sub__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...
        def __xor__(self, other: typing.SupportsInt) -> QWebSocketProtocol.CloseCode: ...

    class Version:
        Version0: ClassVar[QWebSocketProtocol.Version] = ...
        Version13: ClassVar[QWebSocketProtocol.Version] = ...
        Version4: ClassVar[QWebSocketProtocol.Version] = ...
        Version5: ClassVar[QWebSocketProtocol.Version] = ...
        Version6: ClassVar[QWebSocketProtocol.Version] = ...
        Version7: ClassVar[QWebSocketProtocol.Version] = ...
        Version8: ClassVar[QWebSocketProtocol.Version] = ...
        VersionLatest: ClassVar[QWebSocketProtocol.Version] = ...
        VersionUnknown: ClassVar[QWebSocketProtocol.Version] = ...
        values: ClassVar[dict] = ...
        name: Any
        @classmethod
        def __init__(cls, *args, **kwargs) -> None: ...
        def __add__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __and__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __bool__(self) -> bool: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> Any: ...
        def __int__(self) -> int: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __mul__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __pos__(self) -> Any: ...
        def __radd__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __rand__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __rmul__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __ror__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __rsub__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __rxor__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __sub__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
        def __xor__(self, other: typing.SupportsInt) -> QWebSocketProtocol.Version: ...
    CloseCodeAbnormalDisconnection: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeBadOperation: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeDatatypeNotSupported: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeGoingAway: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeMissingExtension: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeMissingStatusCode: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeNormal: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodePolicyViolated: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeProtocolError: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeReserved1004: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeTlsHandshakeFailed: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeTooMuchData: ClassVar[QWebSocketProtocol.CloseCode] = ...
    CloseCodeWrongDatatype: ClassVar[QWebSocketProtocol.CloseCode] = ...
    Version0: ClassVar[QWebSocketProtocol.Version] = ...
    Version13: ClassVar[QWebSocketProtocol.Version] = ...
    Version4: ClassVar[QWebSocketProtocol.Version] = ...
    Version5: ClassVar[QWebSocketProtocol.Version] = ...
    Version6: ClassVar[QWebSocketProtocol.Version] = ...
    Version7: ClassVar[QWebSocketProtocol.Version] = ...
    Version8: ClassVar[QWebSocketProtocol.Version] = ...
    VersionLatest: ClassVar[QWebSocketProtocol.Version] = ...
    VersionUnknown: ClassVar[QWebSocketProtocol.Version] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None: ...

class QWebSocketServer(PySide2.QtCore.QObject):
    class SslMode:
        NonSecureMode: ClassVar[QWebSocketServer.SslMode] = ...
        SecureMode: ClassVar[QWebSocketServer.SslMode] = ...
        values: ClassVar[dict] = ...
        name: Any
        @classmethod
        def __init__(cls, *args, **kwargs) -> None: ...
        def __add__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __and__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __bool__(self) -> bool: ...
        def __eq__(self, other: object) -> bool: ...
        def __ge__(self, other: object) -> bool: ...
        def __gt__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> Any: ...
        def __int__(self) -> int: ...
        def __le__(self, other: object) -> bool: ...
        def __lt__(self, other: object) -> bool: ...
        def __mul__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __ne__(self, other: object) -> bool: ...
        def __or__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __pos__(self) -> Any: ...
        def __radd__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __rand__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __rmul__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __ror__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __rsub__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __rxor__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __sub__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
        def __xor__(self, other: typing.SupportsInt) -> QWebSocketServer.SslMode: ...
    NonSecureMode: ClassVar[QWebSocketServer.SslMode] = ...
    SecureMode: ClassVar[QWebSocketServer.SslMode] = ...
    acceptError: ClassVar[PySide2.QtCore.Signal] = ...
    closed: ClassVar[PySide2.QtCore.Signal] = ...
    newConnection: ClassVar[PySide2.QtCore.Signal] = ...
    originAuthenticationRequired: ClassVar[PySide2.QtCore.Signal] = ...
    peerVerifyError: ClassVar[PySide2.QtCore.Signal] = ...
    preSharedKeyAuthenticationRequired: ClassVar[PySide2.QtCore.Signal] = ...
    serverError: ClassVar[PySide2.QtCore.Signal] = ...
    sslErrors: ClassVar[PySide2.QtCore.Signal] = ...
    staticMetaObject: ClassVar[PySide2.QtCore.QMetaObject] = ...
    def __init__(self, serverName: str, secureMode: QWebSocketServer.SslMode, parent: typing.Union[PySide2.QtCore.QObject,None] = ..., destroyed: typing.Callable = ..., objectName: str = ..., objectNameChanged: typing.Callable = ...) -> None: ...
    def close(self) -> None: ...
    def error(self) -> QWebSocketProtocol.CloseCode: ...
    def errorString(self) -> str: ...
    def handleConnection(self, socket: PySide2.QtNetwork.QTcpSocket) -> None: ...
    def handshakeTimeoutMS(self) -> int: ...
    def hasPendingConnections(self) -> bool: ...
    def isListening(self) -> bool: ...
    def listen(self, address: PySide2.QtNetwork.QHostAddress = ..., port: int = ...) -> bool: ...
    def maxPendingConnections(self) -> int: ...
    def nativeDescriptor(self) -> int: ...
    def nextPendingConnection(self) -> QWebSocket: ...
    def pauseAccepting(self) -> None: ...
    def proxy(self) -> PySide2.QtNetwork.QNetworkProxy: ...
    def resumeAccepting(self) -> None: ...
    def secureMode(self) -> QWebSocketServer.SslMode: ...
    def serverAddress(self) -> PySide2.QtNetwork.QHostAddress: ...
    def serverName(self) -> str: ...
    def serverPort(self) -> int: ...
    def serverUrl(self) -> PySide2.QtCore.QUrl: ...
    def setHandshakeTimeout(self, msec: int) -> None: ...
    def setMaxPendingConnections(self, numConnections: int) -> None: ...
    def setNativeDescriptor(self, descriptor: int) -> bool: ...
    def setProxy(self, networkProxy: PySide2.QtNetwork.QNetworkProxy) -> None: ...
    def setServerName(self, serverName: str) -> None: ...
    def setSocketDescriptor(self, socketDescriptor: int) -> bool: ...
    def socketDescriptor(self) -> int: ...
    def supportedVersions(self) -> typing.List[QWebSocketProtocol.Version]: ...
