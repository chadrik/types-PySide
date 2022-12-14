
# Type stubs for PySide2 (and soon PySide6)

The most accurate type stubs for PySide! They have been tested against a code base with many thousands of lines of PySide code.

## Comparison to other PySide stubs

I tried a number of projects before deciding to create my own.  Here's my super-biased assessment:

| Stub Project                                                         | Technique                                                                         | Rating   |
|----------------------------------------------------------------------|-----------------------------------------------------------------------------------|----------|
| Official stubs                                                       | Uses PySide's `generate_pyi` stub generator                                       | abysmal  |
| [PySide2-Stubs-Gen](https://github.com/HareInWeed/PySide2-Stubs-Gen) | Uses a modified version of `generate_pyi`                                         | marginal |
| [PySide2-stubs](https://pypi.org/project/PySide2-stubs/)             | Reprocesses official stubs using [libcst](https://libcst.readthedocs.io/en/latest/) | better   |
| [types-PySide2](https://pypi.org/project/types-PySide2/)             | Uses mypy's [stubgen](https://mypy.readthedocs.io/en/stable/stubgen.html)         | best     |

`python-qt-tools/PySide2-stubs` is pretty good, but it still produced hundreds of errors in our code base.
One thing I really like about the project, however, is the set of tests that serves to both demonstrate PySide runtime behavior _and_ prove that the stubs are accurate, so I've heavily borrowed from that. 
I considered contributing new features to that project, but the approach of using an AST/CST parser to modify
an upstream set of bad official stubs to make them good is convoluted and prone to errors from upstream changes.
This project uses mypy's official `stubgen` tool to directly generate stubs, with a set of corrections applied.
Corrections are primarily defined through a dictionaries that map classes/methods/args to fixes which are applied during stub generation.
In the process of creating these stubs I made a bunch of improvements to mypy's `stubgen` tool which should benefit me and other stub creators in the future, rather than persisting and working around PySide's own mediocre `PySide2.support.generate_pyi` tool.

## Features and fixes

### General fixes

* Fixed an issue where methods/attributes were not detected, due to presence of `QObject.__getattr__()`
* Added all signals and made new-style signal patterns work
  * e.g. `myobject.mysignal.connect(func)` and `myobject.mysignal[type].connect(func)`
  * Fixed slot arg of `SignalInstance.connect()` to be `typing.Callable` instead of `object`
  * Fixed `Signal.emit()`
  * Fixed `Signal.connect()` return value to bool instead of None
  * Fixed `Object.disconnect()`
* Fixed flag classes to Aad all methods: `__or__`, `__xor__`, ...

### Rule-based fixes

* When instantiating subclasses of `QObject` it is possible to pass the values of properties and signals as `**kwargs` to `__init__`.  The stubs have been fix to include these on all relevant `__init__` methods.
* Qt/PySide has special "flag" enumerator classes that work as pairs: one represents a single flag value, while the other represents multiple combined.  The stubs have been fix to allow either type of flag -- single or multiple -- anywhere that one of the would have been accepted, which is the correct behavior (technically `typing.SupportsInt` is the most correct, but using this would undermine the type enforcement provided by the stubs).
* Removed redundant overlapping overloads, so that satisfying mypy/liskov on subclassed methods is easier 
* Fixed all arguments typed as `typing.Sequence` to be `typing.Iterable`.  Tests so far have indicated that this is true as a general rule.  Also note that unlike other projects, `typing.Iterable` includes the subtype, e.g. `typing.Iterable[str]`
* Replaced `object` with `typing.Any` in return types. e.g.:
  * `QSettings.value() -> Any`
  * `QModelIndex.internalPointer() -> Any`
  * `QPersistentModelIndex.internalPointer() -> Any`

### Specific fixes

* Certain argument types implicitly accept alternative types for brevity.  Below are the known fixes so far (Note that I've debated not including these, since one of the advantages of static typing is it gives you the confidence to be explicit rather than ambiguous. I could introduce a strict mode in the future that would disable these):
  * `QKeySequence`: `str`
  * `QColor`: `Qt.GlobalColor`
  * `QBrush`: `QLinearGradient` and `QColor` (and by extension `Qt.GlobalColor`)
  * `QCursor`: `Qt.CursorShape`
  * `QEasingCurve`: `QEasingCurve.Type`
* Corrected numerous annotations from `bytes/QByteArray` to `str`:
  * `QObject.setProperty()`
  * `QObject.property()`
  * `QState.assignProperty()`
  * `QCoreApplication.translate()`
  * `format` args on all methods
* Fixed `QTreeWidgetItemIterator.__iter__()` to return `Iterator[QTreeWidgetItemIterator]`
* Added missing `QDialog.exec()` method
* Fixed numerous methods which accept `None`:
  * `QPainter.drawText(..., br)`
  * `QPainter.drawPolygon(..., arg__2)`
  * `QProgressDialog.setCancelButton(button)`
  * `*.setModel(model)`
  * `QLabel.setPixmap(arg__1)`
* Fixed numerous arguments that accept `QModelIndex` which were typed as `int`
* Fixed return type for `QApplication.instance()` and `QGuiApplication.instance()`
* Fixed return type for `QObject.findChild()` and `QObject.findChildren()`
* Fixed support for initializing `QDate` from `datetime.date`
* Fixed support for initializing `QDateTime` from `datetime.datetime`
* Fixed `QByteArray.__iter__()` to return `Iterator[bytes]`
* Fixed support for `bytes(QByteArray(b'foo'))`
* Added support for all `QSize` and `QSizeF` operations
* Added support for all `QPolygon` operations

## Licensing
As a derived work from PySide2, the stubs are delivered under the LGPL v2.1 . See file LICENSE for more details.

## Installation

Install the latest stub packages from pypi:

    $ pip install types-PySide2

This will add the `PySide2-stubs` and `shiboken2-stubs` packages into your site-packages directory. 

Note, you may need to uninstall other PySide2 stubs first:

    $ pip uninstall PySide2-stubs

## Help improve the stubs

If you notice incorrect or missing typing information (i.e. mypy reports errors even though your code is correct), please report it or make a PR to fix it. 

## TODO

* Get all my stubgen changes merged into mypy
* Build PySide6 stubs
* Merge overloads where a `Union` would do instead of multiple overloads
* Add type enforcement for signal types, to protect against incorrect callables provided to `connect()`
