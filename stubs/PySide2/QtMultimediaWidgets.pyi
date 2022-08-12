from typing import Any, Callable, ClassVar, Union

import PySide2.QtCore
import PySide2.QtGui
import PySide2.QtMultimedia
import PySide2.QtWidgets
import typing
T = typing.TypeVar('T')

class QCameraViewfinder(QVideoWidget):
    staticMetaObject: ClassVar[PySide2.QtCore.QMetaObject] = ...
    def __init__(self, parent: typing.Union[PySide2.QtWidgets.QWidget,None] = ..., acceptDrops: bool = ..., accessibleDescription: str = ..., accessibleName: str = ..., aspectRatioMode: PySide2.QtCore.Qt.AspectRatioMode = ..., autoFillBackground: bool = ..., baseSize: PySide2.QtCore.QSize = ..., brightness: int = ..., brightnessChanged: typing.Callable = ..., childrenRect: PySide2.QtCore.QRect = ..., childrenRegion: PySide2.QtGui.QRegion = ..., contextMenuPolicy: PySide2.QtCore.Qt.ContextMenuPolicy = ..., contrast: int = ..., contrastChanged: typing.Callable = ..., cursor: PySide2.QtGui.QCursor = ..., customContextMenuRequested: typing.Callable = ..., destroyed: typing.Callable = ..., enabled: bool = ..., focus: bool = ..., focusPolicy: PySide2.QtCore.Qt.FocusPolicy = ..., font: PySide2.QtGui.QFont = ..., frameGeometry: PySide2.QtCore.QRect = ..., frameSize: PySide2.QtCore.QSize = ..., fullScreen: bool = ..., fullScreenChanged: typing.Callable = ..., geometry: PySide2.QtCore.QRect = ..., height: int = ..., hue: int = ..., hueChanged: typing.Callable = ..., inputMethodHints: typing.Union[PySide2.QtCore.Qt.InputMethodHints,PySide2.QtCore.Qt.InputMethodHint] = ..., isActiveWindow: bool = ..., layoutDirection: PySide2.QtCore.Qt.LayoutDirection = ..., locale: PySide2.QtCore.QLocale = ..., maximized: bool = ..., maximumHeight: int = ..., maximumSize: PySide2.QtCore.QSize = ..., maximumWidth: int = ..., mediaObject: PySide2.QtMultimedia.QMediaObject = ..., minimized: bool = ..., minimumHeight: int = ..., minimumSize: PySide2.QtCore.QSize = ..., minimumSizeHint: PySide2.QtCore.QSize = ..., minimumWidth: int = ..., modal: bool = ..., mouseTracking: bool = ..., normalGeometry: PySide2.QtCore.QRect = ..., objectName: str = ..., objectNameChanged: typing.Callable = ..., palette: PySide2.QtGui.QPalette = ..., pos: PySide2.QtCore.QPoint = ..., rect: PySide2.QtCore.QRect = ..., saturation: int = ..., saturationChanged: typing.Callable = ..., size: PySide2.QtCore.QSize = ..., sizeHint: PySide2.QtCore.QSize = ..., sizeIncrement: PySide2.QtCore.QSize = ..., sizePolicy: PySide2.QtWidgets.QSizePolicy = ..., statusTip: str = ..., styleSheet: str = ..., tabletTracking: bool = ..., toolTip: str = ..., toolTipDuration: int = ..., updatesEnabled: bool = ..., videoSurface: typing.Any = ..., visible: bool = ..., whatsThis: str = ..., width: int = ..., windowFilePath: str = ..., windowIcon: PySide2.QtGui.QIcon = ..., windowIconChanged: typing.Callable = ..., windowIconText: str = ..., windowIconTextChanged: typing.Callable = ..., windowModality: PySide2.QtCore.Qt.WindowModality = ..., windowModified: bool = ..., windowOpacity: float = ..., windowTitle: str = ..., windowTitleChanged: typing.Callable = ..., x: int = ..., y: int = ...) -> None: ...
    def mediaObject(self) -> PySide2.QtMultimedia.QMediaObject: ...
    def setMediaObject(self, object: PySide2.QtMultimedia.QMediaObject) -> bool: ...

class QGraphicsVideoItem(PySide2.QtWidgets.QGraphicsObject, PySide2.QtMultimedia.QMediaBindableInterface):
    nativeSizeChanged: ClassVar[PySide2.QtCore.Signal] = ...
    staticMetaObject: ClassVar[PySide2.QtCore.QMetaObject] = ...
    def __init__(self, parent: typing.Union[PySide2.QtWidgets.QGraphicsItem,None] = ..., aspectRatioMode: PySide2.QtCore.Qt.AspectRatioMode = ..., children: typing.Any = ..., childrenChanged: typing.Callable = ..., destroyed: typing.Callable = ..., effect: typing.Any = ..., enabled: bool = ..., enabledChanged: typing.Callable = ..., height: float = ..., heightChanged: typing.Callable = ..., mediaObject: PySide2.QtMultimedia.QMediaObject = ..., nativeSize: PySide2.QtCore.QSizeF = ..., nativeSizeChanged: typing.Callable = ..., objectName: str = ..., objectNameChanged: typing.Callable = ..., offset: PySide2.QtCore.QPointF = ..., opacity: float = ..., opacityChanged: typing.Callable = ..., parentChanged: typing.Callable = ..., pos: PySide2.QtCore.QPointF = ..., rotation: float = ..., rotationChanged: typing.Callable = ..., scale: float = ..., scaleChanged: typing.Callable = ..., size: PySide2.QtCore.QSizeF = ..., transformOriginPoint: PySide2.QtCore.QPointF = ..., videoSurface: PySide2.QtMultimedia.QAbstractVideoSurface = ..., visible: bool = ..., visibleChanged: typing.Callable = ..., width: float = ..., widthChanged: typing.Callable = ..., x: float = ..., xChanged: typing.Callable = ..., y: float = ..., yChanged: typing.Callable = ..., z: float = ..., zChanged: typing.Callable = ...) -> None: ...
    def aspectRatioMode(self) -> PySide2.QtCore.Qt.AspectRatioMode: ...
    def boundingRect(self) -> PySide2.QtCore.QRectF: ...
    def itemChange(self, change: PySide2.QtWidgets.QGraphicsItem.GraphicsItemChange, value: typing.Any) -> typing.Any: ...
    def mediaObject(self) -> PySide2.QtMultimedia.QMediaObject: ...
    def nativeSize(self) -> PySide2.QtCore.QSizeF: ...
    def offset(self) -> PySide2.QtCore.QPointF: ...
    def paint(self, painter: PySide2.QtGui.QPainter, option: PySide2.QtWidgets.QStyleOptionGraphicsItem, widget: typing.Union[PySide2.QtWidgets.QWidget,None] = ...) -> None: ...
    def setAspectRatioMode(self, mode: PySide2.QtCore.Qt.AspectRatioMode) -> None: ...
    def setMediaObject(self, object: PySide2.QtMultimedia.QMediaObject) -> bool: ...
    def setOffset(self, offset: PySide2.QtCore.QPointF) -> None: ...
    def setSize(self, size: PySide2.QtCore.QSizeF) -> None: ...
    def size(self) -> PySide2.QtCore.QSizeF: ...
    def timerEvent(self, event: PySide2.QtCore.QTimerEvent) -> None: ...
    def videoSurface(self) -> PySide2.QtMultimedia.QAbstractVideoSurface: ...

class QVideoWidget(PySide2.QtWidgets.QWidget, PySide2.QtMultimedia.QMediaBindableInterface):
    brightnessChanged: ClassVar[PySide2.QtCore.Signal] = ...
    contrastChanged: ClassVar[PySide2.QtCore.Signal] = ...
    fullScreenChanged: ClassVar[PySide2.QtCore.Signal] = ...
    hueChanged: ClassVar[PySide2.QtCore.Signal] = ...
    saturationChanged: ClassVar[PySide2.QtCore.Signal] = ...
    staticMetaObject: ClassVar[PySide2.QtCore.QMetaObject] = ...
    def __init__(self, parent: typing.Union[PySide2.QtWidgets.QWidget,None] = ..., acceptDrops: bool = ..., accessibleDescription: str = ..., accessibleName: str = ..., aspectRatioMode: PySide2.QtCore.Qt.AspectRatioMode = ..., autoFillBackground: bool = ..., baseSize: PySide2.QtCore.QSize = ..., brightness: int = ..., brightnessChanged: typing.Callable = ..., childrenRect: PySide2.QtCore.QRect = ..., childrenRegion: PySide2.QtGui.QRegion = ..., contextMenuPolicy: PySide2.QtCore.Qt.ContextMenuPolicy = ..., contrast: int = ..., contrastChanged: typing.Callable = ..., cursor: PySide2.QtGui.QCursor = ..., customContextMenuRequested: typing.Callable = ..., destroyed: typing.Callable = ..., enabled: bool = ..., focus: bool = ..., focusPolicy: PySide2.QtCore.Qt.FocusPolicy = ..., font: PySide2.QtGui.QFont = ..., frameGeometry: PySide2.QtCore.QRect = ..., frameSize: PySide2.QtCore.QSize = ..., fullScreen: bool = ..., fullScreenChanged: typing.Callable = ..., geometry: PySide2.QtCore.QRect = ..., height: int = ..., hue: int = ..., hueChanged: typing.Callable = ..., inputMethodHints: typing.Union[PySide2.QtCore.Qt.InputMethodHints,PySide2.QtCore.Qt.InputMethodHint] = ..., isActiveWindow: bool = ..., layoutDirection: PySide2.QtCore.Qt.LayoutDirection = ..., locale: PySide2.QtCore.QLocale = ..., maximized: bool = ..., maximumHeight: int = ..., maximumSize: PySide2.QtCore.QSize = ..., maximumWidth: int = ..., mediaObject: PySide2.QtMultimedia.QMediaObject = ..., minimized: bool = ..., minimumHeight: int = ..., minimumSize: PySide2.QtCore.QSize = ..., minimumSizeHint: PySide2.QtCore.QSize = ..., minimumWidth: int = ..., modal: bool = ..., mouseTracking: bool = ..., normalGeometry: PySide2.QtCore.QRect = ..., objectName: str = ..., objectNameChanged: typing.Callable = ..., palette: PySide2.QtGui.QPalette = ..., pos: PySide2.QtCore.QPoint = ..., rect: PySide2.QtCore.QRect = ..., saturation: int = ..., saturationChanged: typing.Callable = ..., size: PySide2.QtCore.QSize = ..., sizeHint: PySide2.QtCore.QSize = ..., sizeIncrement: PySide2.QtCore.QSize = ..., sizePolicy: PySide2.QtWidgets.QSizePolicy = ..., statusTip: str = ..., styleSheet: str = ..., tabletTracking: bool = ..., toolTip: str = ..., toolTipDuration: int = ..., updatesEnabled: bool = ..., videoSurface: PySide2.QtMultimedia.QAbstractVideoSurface = ..., visible: bool = ..., whatsThis: str = ..., width: int = ..., windowFilePath: str = ..., windowIcon: PySide2.QtGui.QIcon = ..., windowIconChanged: typing.Callable = ..., windowIconText: str = ..., windowIconTextChanged: typing.Callable = ..., windowModality: PySide2.QtCore.Qt.WindowModality = ..., windowModified: bool = ..., windowOpacity: float = ..., windowTitle: str = ..., windowTitleChanged: typing.Callable = ..., x: int = ..., y: int = ...) -> None: ...
    def aspectRatioMode(self) -> PySide2.QtCore.Qt.AspectRatioMode: ...
    def brightness(self) -> int: ...
    def contrast(self) -> int: ...
    def event(self, event: PySide2.QtCore.QEvent) -> bool: ...
    def hideEvent(self, event: PySide2.QtGui.QHideEvent) -> None: ...
    def hue(self) -> int: ...
    def mediaObject(self) -> PySide2.QtMultimedia.QMediaObject: ...
    def moveEvent(self, event: PySide2.QtGui.QMoveEvent) -> None: ...
    def paintEvent(self, event: PySide2.QtGui.QPaintEvent) -> None: ...
    def resizeEvent(self, event: PySide2.QtGui.QResizeEvent) -> None: ...
    def saturation(self) -> int: ...
    def setAspectRatioMode(self, mode: PySide2.QtCore.Qt.AspectRatioMode) -> None: ...
    def setBrightness(self, brightness: int) -> None: ...
    def setContrast(self, contrast: int) -> None: ...
    def setFullScreen(self, fullScreen: bool) -> None: ...
    def setHue(self, hue: int) -> None: ...
    def setMediaObject(self, object: PySide2.QtMultimedia.QMediaObject) -> bool: ...
    def setSaturation(self, saturation: int) -> None: ...
    def showEvent(self, event: PySide2.QtGui.QShowEvent) -> None: ...
    def sizeHint(self) -> PySide2.QtCore.QSize: ...
    def videoSurface(self) -> PySide2.QtMultimedia.QAbstractVideoSurface: ...

class QVideoWidgetControl(PySide2.QtMultimedia.QMediaControl):
    brightnessChanged: ClassVar[PySide2.QtCore.Signal] = ...
    contrastChanged: ClassVar[PySide2.QtCore.Signal] = ...
    fullScreenChanged: ClassVar[PySide2.QtCore.Signal] = ...
    hueChanged: ClassVar[PySide2.QtCore.Signal] = ...
    saturationChanged: ClassVar[PySide2.QtCore.Signal] = ...
    staticMetaObject: ClassVar[PySide2.QtCore.QMetaObject] = ...
    def __init__(self, parent: typing.Union[PySide2.QtCore.QObject,None] = ..., destroyed: typing.Callable = ..., objectName: str = ..., objectNameChanged: typing.Callable = ...) -> None: ...
    def aspectRatioMode(self) -> PySide2.QtCore.Qt.AspectRatioMode: ...
    def brightness(self) -> int: ...
    def contrast(self) -> int: ...
    def hue(self) -> int: ...
    def isFullScreen(self) -> bool: ...
    def saturation(self) -> int: ...
    def setAspectRatioMode(self, mode: PySide2.QtCore.Qt.AspectRatioMode) -> None: ...
    def setBrightness(self, brightness: int) -> None: ...
    def setContrast(self, contrast: int) -> None: ...
    def setFullScreen(self, fullScreen: bool) -> None: ...
    def setHue(self, hue: int) -> None: ...
    def setSaturation(self, saturation: int) -> None: ...
    def videoWidget(self) -> PySide2.QtWidgets.QWidget: ...