from __future__ import absolute_import, print_function

import importlib
import inspect
import itertools
import pydoc
import re
import typing
from functools import lru_cache, total_ordering
from types import ModuleType
from typing import Any, List, Optional, Iterable, Mapping, NamedTuple, Tuple, Union

import mypy.stubgen
import mypy.stubgenc
from mypy.stubgenc import get_type_fullname

from PySide2 import QtCore, QtWidgets

cache = lru_cache(maxsize=None)

_orig_get_sig_generators = mypy.stubgen.get_sig_generators
_orig_is_skipped_attribute = mypy.stubgenc.is_skipped_attribute
_orig_is_c_method = mypy.stubgenc.is_c_method
_orig_strip_or_import = mypy.stubgenc.strip_or_import
_orig_generate_stub_for_c_module = mypy.stubgenc.generate_stub_for_c_module
# _orig_infer_sig_from_docstring = mypy.stubdoc.infer_sig_from_docstring
_orig_add_typing_import = mypy.stubgenc.add_typing_import
_orig_get_members = mypy.stubgenc.get_members

# TODO: support PySide6
PYSIDE = 'PySide2'

Optionality = NamedTuple(
    'Optionality', [('accepts_none', bool), ('has_default', bool)])


def pyside(type_name: str) -> str:
    return type_name.replace('PySide*', PYSIDE)


def is_pyside_obj(typ: type) -> bool:
    return typ.__module__.split('.')[0] in PYSIDE


@cache
def is_flag(typ: type) -> bool:
    return hasattr(typ, '__pos__') and not hasattr(typ, '__invert__') and is_pyside_obj(typ) \
           and typ.__bases__ == (object,)


@cache
def is_flag_group(typ: type) -> bool:
    return hasattr(typ, '__invert__') and not hasattr(typ, 'values') and is_pyside_obj(typ) \
           and typ.__bases__ == (object,)


@cache
def is_flag_item(typ: type) -> bool:
    return hasattr(typ, '__invert__') and hasattr(typ, 'values') and is_pyside_obj(typ) \
           and typ.__bases__ == (object,)


_flag_group_to_item = {}

@cache
def get_group_from_flag_item(item_type: type) -> type:
    group_type = type(item_type() | item_type())
    _flag_group_to_item[get_type_fullname(group_type)] = get_type_fullname(item_type)
    return group_type


@cache
def get_properties(typ) -> Mapping[str, str]:
    """
    Get a mapping of property/signal name to type.
    """
    if not isinstance(typ, type) or not issubclass(typ, QtCore.QObject):
        return {}

    if typ.__bases__:
        base_props = get_properties(typ.__bases__[0])
    else:
        base_props = {}

    try:
        obj = typ()
    except Exception:
        return base_props

    try:
        meta = obj.metaObject()
    except AttributeError:
        return base_props

    def getsig(prop: QtCore.QMetaProperty) -> Tuple[str, str]:
        name = decode(prop.name())
        fallback_type = prop.type()
        # for some reason QtCore.Qt.GlobalColor is returned for many properties even though it's
        # wrong
        if fallback_type is QtCore.Qt.GlobalColor:
            # see if the property has a method since the signature return value can be used to
            # infer the property type.
            func = getattr(obj, name, None)
            if func is not None:
                sig = getattr(func, '__signature__', None)
                if isinstance(sig, inspect.Signature) and sig.return_annotation:
                    return name, typing._type_repr(sig.return_annotation)

            if prop.isEnumType():
                c_type_name = prop.typeName()
                maybe_type_name = c_type_name.replace('::', '.')
                if maybe_type_name.startswith('Qt.'):
                    maybe_type_name = 'PySide2.QtCore.' + maybe_type_name
                # elif maybe_type_name.startswith('Qt'):
                #     maybe_type_name = 'PySide2.' + maybe_type_name
                else:
                    maybe_type_name = typing._type_repr(typ) + '.' + maybe_type_name

                # check that it's real
                if pydoc.locate(maybe_type_name) is None:
                    # FIXME: this could be improved with a more exhaustive search. seems like there
                    #  should be a better way.
                    print("{}.{}: Could not determine type of property".format(typing._type_repr(typ), name))
                    print("  {}".format(c_type_name))
                    print("  {}".format(maybe_type_name))
                    type_name = 'typing.Any'
                else:
                    type_name = maybe_type_name
            else:
                type_name = 'typing.Any'
            return name, type_name
        return name, typing._type_repr(fallback_type)

    def decode(x):
        if isinstance(x, QtCore.QByteArray):
            return bytes(x).decode()
        elif isinstance(x, bytes):
            return x.decode()
        else:
            return x

    result = dict(base_props)
    props = [meta.property(i) for i in range(meta.propertyCount())]
    result.update(getsig(prop) for prop in props)

    methods = [meta.method(i) for i in range(meta.methodCount())]
    signals = [decode(meth.name()) for meth in methods
               if meth.methodType() == QtCore.QMetaMethod.MethodType.Signal]

    result.update((name, 'typing.Callable') for name in signals)
    obj.deleteLater()

    return result


def add_property_args(typ: type, sigs: List[mypy.stubgenc.FunctionSig]) -> None:
    """
    Extend the signatures to include keyword arguments for properties and signals.
    """
    properties = get_properties(typ)
    if properties:
        property_names = set(properties)
        for inferred in sigs:
            arg_names = set([arg.name for arg in inferred.args])
            missing = property_names.difference(arg_names)
            if missing:
                # FIXME: add '*' arg
                inferred.args.extend([
                    mypy.stubgenc.ArgSig(name=name, type=properties[name],
                                         default=True)
                    for name in sorted(missing)
                ])


def format_signature(signature: mypy.stubgenc.FunctionSig,
                     class_name: Optional[str] = None) -> str:
    """
    Only used for debugging
    """
    sig = []
    for arg in signature.args:
        arg_def = arg.name
        if arg.type:
            arg_def += ": " + arg.type

        if arg.default:
            arg_def += " = ..."

        sig.append(arg_def)
    result = '{}({}) -> {}'.format(
        '__init__' if signature.name == class_name else signature.name,
        ', '.join(sig), signature.ret_type)
    if class_name:
        result = class_name + '.' + result
    return result


def short_name(type_name: str) -> str:
    return type_name.split('.')[-1]


def reduce_overloads(sigs: List[mypy.stubgenc.FunctionSig]) -> List[mypy.stubgenc.FunctionSig]:
    """
    Remove unsupported and redundant overloads.

    - Some overloads are a subset of other overloads and can be pruned.
    - Some methods implement both classmethod and instancemethod overloads, and mypy prevents
      mixing these and does not correctly analyze them: so we have to drop one, and we've chosen
      to remove classmethods.  It is possible to implement a "universalmethod" decorator, but
      we could not use overloads to distinguish their arguments.
    """
    # remove dups (FunctionSig is not hashable, so it's a bit cumbersome)
    new_sigs = []
    classmethods = []
    instancmethods = []
    for sig in sigs:
        if sig not in new_sigs:
            if sig.args and sig.args[0].name == 'self':
                instancmethods.append(sig)
            else:
                classmethods.append(sig)
            new_sigs.append(sig)
    if classmethods and instancmethods:
        if sigs[0].name == 'moveToTrash':
            print(classmethods)
            print(instancmethods)
        new_sigs = instancmethods

    if len(new_sigs) <= 1:
        return new_sigs

    sigs = sorted(new_sigs, key=lambda x: len(x.args), reverse=True)
    redundant = []
    for a, b in itertools.combinations(sigs, 2):
        if contains_other_overload(a, b):
            redundant.append(b)
        elif contains_other_overload(b, a):
            redundant.append(a)
    results = [sig for sig in sigs if sig not in redundant]
    if not results:
        print("removed too much")
        for x in sigs:
            print(x)
        raise ValueError
    return results


def contains_other_overload(sig: mypy.stubgenc.FunctionSig,
                            other: mypy.stubgenc.FunctionSig) -> bool:
    """
    Return whether an overload is fully covered by another overload, and thus redundant.
    """
    if other.ret_type != sig.ret_type:
        # not compatible
        return False
    num_other_args = len(other.args)
    if len(sig.args) < num_other_args:
        # other has more args, sig cannot contain other
        return False
    if sig.args[:num_other_args] == other.args and all(a.default for a in sig.args[num_other_args:]):
        # sig contains all of other's args, and the remaining sig args all have defaults
        return True
    return False


@total_ordering
class OptionalKey:
    """
    Util to simplify optional hierarchical keys.

    Allows this to be true:
        OptionalKey('foo') == OptionalKey(None)
    """
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return 'OptionalKey({})'.format(repr(self.s))

    def __hash__(self):
        # Use the same hash as None, so that we get a chance to run __eq__ when
        # compared to None as a dictionary key
        return hash(None)

    def __eq__(self, other):
        if isinstance(other, OptionalKey):
            other = other.s
        if self.s is None or other is None:
            return True
        return other == self.s

    def __lt__(self, other):
        if isinstance(other, OptionalKey):
            other = other.s
        return other < self.s


# constant for clarity
ANY = None


class PySideSignatureGenerator(mypy.stubgenc.SignatureGenerator):
    docstring = mypy.stubgenc.DocstringSignatureGenerator()

    # Full signature replacements.
    # The class name can be ANY, in which case it will match any class
    _signature_overrides = {
        # these docstring sigs are malformed
        ('VolatileBool', 'get'):
            '(self) -> bool',
        ('VolatileBool', 'set'):
            '(self, a: object) -> None',

        # * Add all signals and make all new-style signal patterns work.  e.g.
        # `myobject.mysignal.connect(func) and `myobject.mysignal[type].connect(func)`
        ('Signal', '__get__'):
            [
                '(self, instance: None, owner: typing.Type[QObject]) -> Signal',
                '(self, instance: QObject, owner: typing.Type[QObject]) -> SignalInstance',
            ],
        ('Signal', '__getitem__'):
            '(self, index) -> SignalInstance',
        ('SignalInstance', '__getitem__'):
            '(self, index) -> SignalInstance',

        # * Fix slot arg of `SignalInstance.connect()` to be `typing.Callable` instead of `object`
        ('SignalInstance', 'connect'):
            '(self, slot: typing.Callable, type: typing.Union[type,None] = ...) -> bool',
        ('SignalInstance', 'disconnect'):
            '(self, slot: typing.Union[typing.Callable,None] = ...) -> None',
        ('QObject', 'disconnect'):
            [
                '(cls, arg__1: PySide2.QtCore.QObject, arg__2: str = ..., arg__3: typing.Callable = ...) -> bool',
                '(cls, arg__1: PySide2.QtCore.QMetaObject.Connection) -> bool',
                '(cls, sender: PySide2.QtCore.QObject, signal: PySide2.QtCore.QMetaMethod, receiver: PySide2.QtCore.QObject = ..., member: PySide2.QtCore.QMetaMethod = ...) -> bool',
            ],

        ('QWidget', 'setParent'):
            '(self, parent: typing.Union[PySide2.QtCore.QObject,None], f: PySide2.QtCore.Qt.WindowFlags = ...) -> None',

        # * Correct numerous annotations from `bytes` to `str`
        ('QObject', 'setProperty'):
            '(self, name: str, value: typing.Any) -> bool',
        ('QObject', 'property'):
            '(self, name: str) -> typing.Any',
        ('QState', 'assignProperty'):
            '(self, object: QObject, name: str, value: typing.Any) -> None',
        # (ANY, 'propertyName'):
        #     '(self) -> str',
        ('QCoreApplication', 'translate'):
            '(cls, context: str, key: str, disambiguation: typing.Union[str,NoneType] = ..., n: int = ...) -> str',

        # * Fix `QTreeWidgetItemIterator.__iter__()` to iterate over `QTreeWidgetItemIterator`
        ('QTreeWidgetItemIterator', '__iter__'):
            # Add result type
            '(self) -> typing.Iterator[QTreeWidgetItemIterator]',
        ('QTreeWidgetItemIterator', '__next__'):
            # Add result type
            '(self) -> QTreeWidgetItemIterator',

        # * Make result optional
        ('QLayout', 'itemAt'):
            '(self, index: int) -> typing.Optional[PySide*.QtWidgets.QLayoutItem]',
        ('QLayout', 'takeAt'):
            '(self, index: int) -> typing.Optional[PySide*.QtWidgets.QLayoutItem]',

        # * Fix QPolygon special methods
        ('QPolygon', '__lshift__'):
            # first and third overloads should return QPolygon
            [
                '(self, l: typing.List[PySide2.QtCore.QPoint]) -> PySide2.QtGui.QPolygon',
                '(self, stream: PySide2.QtCore.QDataStream) -> PySide2.QtCore.QDataStream',
                '(self, t: PySide2.QtCore.QPoint) -> PySide2.QtGui.QPolygon',
            ],
        ('QPolygon', '__iadd__'):
            # should return QPolygon
            '(self, t: PySide2.QtCore.QPoint) -> PySide2.QtGui.QPolygon',

        # * Fix `QByteArray(b'foo')[0]` to return `bytes`
        ('QByteArray', '__getitem__'):
            # missing index and return.
            '(self, index: int) -> bytes',

        # * Fix `QByteArray.__iter__()` to iterate over `bytes`
        ('QByteArray', '__iter__'):
            # __iter__ is implied by __len__ and __getitem__, but it's not enough to satisfy mypy
            '(self) -> typing.Iterator[bytes]',

        # * Fix support for `bytes(QByteArray(b'foo'))`
        ('QByteArray', '__bytes__'):
            '(self) -> bytes',

        # FIXME: make this a general rule
        # * Replace `object` with `typing.Any` in return types
        ('QSettings', 'value'):
            '(self, arg__1: str, defaultValue: typing.Union[typing.Any, None] = ..., '
            'type: typing.Union[typing.Any, None] = ...) -> typing.Any',
        ('QModelIndex', 'internalPointer'):
            '(self) -> typing.Any',
        ('QPersistentModelIndex', 'internalPointer'):
            '(self) -> typing.Any',

        # Fix other flags:
        ('QSortFilterProxyModel', 'filterRole'):
            '(self) -> PySide*.QtCore.Qt.ItemDataRole',
        ('QStandardItem', 'type'):
            '(self) -> PySide*.QtGui.QStandardItem.ItemType',
        ('QTableWidgetItem', 'setTextAlignment'):
            '(self, alignment: PySide*.QtCore.Qt.Alignment) -> None',
        ('QFrame', 'setFrameStyle'):
            '(self, arg__1: typing.Union[PySide*.QtWidgets.QFrame.Shape, PySide*.QtWidgets.QFrame.Shadow, typing.SupportsInt]) -> None',

        # in PySide2 these take int, and in PySide6 it takes Weight, but both seem valid
        ('QFont', 'setWeight'):
            '(self, arg__1: typing.Union[int, PySide*.QtGui.QFont.Weight]) -> None',
        ('QTextEdit', 'setFontWeight'):
            '(self, w: typing.Union[int, PySide*.QtGui.QFont.Weight]) -> None',
        # ('QFont', 'weight'): pyside('(self) -> PySide*.QtGui.QFont.Weight'),  # fixed in PySide6

        # * Fix arguments that accept `QModelIndex` which were typed as `int` in many places
        (ANY, 'selectedIndexes'):
            # known offenders: QAbstractItemView, QItemSelectionModel, QTreeView, QListView
            '(self) -> typing.List[PySide*.QtCore.QModelIndex]',
        ('QItemSelectionModel', 'selectedColumns'):
            '(self, row: int = ...) -> typing.List[PySide*.QtCore.QModelIndex]',
        ('QItemSelectionModel', 'selectedRows'):
            '(self, column: int = ...) -> typing.List[PySide*.QtCore.QModelIndex]',
        ('QItemSelection', 'indexes'):
            '(self) -> typing.List[PySide*.QtCore.QModelIndex]',
        ('QItemSelectionRange', 'indexes'):
            '(self) -> typing.List[PySide*.QtCore.QModelIndex]',
        ('QAbstractItemModel', 'mimeData'):
            '(self, indexes: typing.List[PySide*.QtCore.QModelIndex]) -> PySide*.QtCore.QMimeData',
        ('QStandardItemModel', 'mimeData'):
            '(self, indexes: typing.List[PySide*.QtCore.QModelIndex]) -> PySide*.QtCore.QMimeData',

        # * Fix return type for `QApplication.instance()` and `QGuiApplication.instance()` :
        ('QCoreApplication', 'instance'):
            '(cls: typing.Type[T]) -> T',

        # * Fix return type for `QObject.findChild()` and `QObject.findChildren()` :
        ('QObject', 'findChild'):
            '(self, arg__1: typing.Type[T], arg__2: str = ...) -> T',
        ('QObject', 'findChildren'): [
            '(self, arg__1: typing.Type[T], arg__2: QRegExp = ...) -> typing.List[T]',
            '(self, arg__1: typing.Type[T], arg__2: QRegularExpression = ...) -> typing.List[T]',
            '(self, arg__1: typing.Type[T], arg__2: str = ...) -> typing.List[T]',
        ],

        # signatures for these special methods include many inaccurate overloads
        (ANY, '__ne__'): '(self, other: object) -> bool',
        (ANY, '__eq__'): '(self, other: object) -> bool',
        (ANY, '__lt__'): '(self, other: object) -> bool',
        (ANY, '__gt__'): '(self, other: object) -> bool',
        (ANY, '__le__'): '(self, other: object) -> bool',
        (ANY, '__ge__'): '(self, other: object) -> bool',
    }

    # Special methods for flag enums.
    flag_overrides = {
        # FIXME: QFrame.Shape and QFrame.Shadow are meant to be used with each other and return an int
        '__or__': '(self, other: typing.SupportsInt) -> {}',
        '__ror__': '(self, other: typing.SupportsInt) -> {}',
        '__and__': '(self, other: typing.SupportsInt) -> {}',
        '__rand__': '(self, other: typing.SupportsInt) -> {}',
        '__xor__': '(self, other: typing.SupportsInt) -> {}',
        '__rxor__': '(self, other: typing.SupportsInt) -> {}',
        '__lshift__': '(self, other: typing.SupportsInt) -> {}',
        '__rshift__': '(self, other: typing.SupportsInt) -> {}',
        '__add__': '(self, other: typing.SupportsInt) -> {}',
        '__radd__': '(self, other: typing.SupportsInt) -> {}',
        '__mul__': '(self, other: typing.SupportsInt) -> {}',
        '__rmul__': '(self, other: typing.SupportsInt) -> {}',
        '__sub__': '(self, other: typing.SupportsInt) -> {}',
        '__rsub__': '(self, other: typing.SupportsInt) -> {}',
        '__invert__': '(self) -> {}',
    }

    # Types that have implicit alternatives.
    _implicit_arg_types = {
        'PySide2.QtGui.QKeySequence':
            ['str'],
        'PySide2.QtGui.QColor':
            ['PySide2.QtCore.Qt.GlobalColor',
             'int'],
        'PySide2.QtCore.QByteArray':
            ['bytes'],
        'PySide2.QtGui.QBrush':
            ['PySide2.QtGui.QColor',
             'PySide2.QtCore.Qt.GlobalColor',
             'PySide2.QtGui.QLinearGradient'],
        'PySide2.QtGui.QCursor':
            ['PySide2.QtCore.Qt.CursorShape'],
        'PySide2.QtCore.QEasingCurve':
            ['PySide2.QtCore.QEasingCurve.Type'],
    }

    # Override argument types
    _arg_type_overrides = {
        # (class, method, arg, type)
        (ANY, ANY, 'flags', 'int'): 'typing.SupportsInt',
        (ANY, ANY, 'weight', 'int'): 'typing.SupportsInt',
        (ANY, ANY, 'format', 'typing.Union[bytes,NoneType]'): 'typing.Optional[str]',
        (ANY, ANY, 'role', 'int'): 'PySide*.QtCore.Qt.ItemDataRole',
        (ANY, 'addAction', ANY, 'object'): 'typing.Callable[[], typing.Any]',
    }

    # Find and replace argument names
    _arg_name_replacements = {
        # (class, method, arg, type)
    }

    # Values which should be made Optional[].
    _optional_args = {
        # (class, method, arg, type)
        ('QPainter', 'drawText', 'br', ANY):
            Optionality(accepts_none=True, has_default=True),
        ('QPainter', 'drawPolygon', 'arg__2', ANY):
            Optionality(accepts_none=True, has_default=True),
        ('QProgressDialog', 'setCancelButton', 'button', ANY):
            Optionality(accepts_none=True, has_default=False),
        (ANY, 'setModel', 'model', ANY):
            Optionality(accepts_none=True, has_default=False),
        ('QLabel', 'setPixmap', 'arg__1', ANY):
            Optionality(accepts_none=True, has_default=False),
        (ANY, ANY, 'parent', 'PySide2.QtWidgets.QWidget'):
            Optionality(accepts_none=True, has_default=False),
        (ANY, ANY, 'parent', 'PySide2.QtCore.QObject'):
            Optionality(accepts_none=True, has_default=False),
        ('QInputDialog', 'getText', 'echo', ANY):
            Optionality(accepts_none=False, has_default=True),
    }

    # Add new overloads to existing functions.
    new_overloads = {
        # * Fix support for initializing `QDate` from `datetime.date`
        ('QDate', '__init__'):
            '(self, date: datetime.date) -> None',
        # * Fix support for initializing `QDateTime` from `datetime.datetime`
        ('QDateTime', '__init__'):
            '(self, datetime: datetime.datetime) -> None',

        # * Add `QSpacerItem.__init__/changeSize` overloads that use alternate names: `hData`->`hPolicy`, `vData`->`vPolicy`
        ('QSpacerItem', '__init__'):
            '(self, w:int, h:int, hPolicy:PySide2.QtWidgets.QSizePolicy.Policy=..., vPolicy:PySide2.QtWidgets.QSizePolicy.Policy=...) -> None',
        ('QSpacerItem', 'changeSize'):
            '(self, w:int, h:int, hPolicy:PySide2.QtWidgets.QSizePolicy.Policy=..., vPolicy:PySide2.QtWidgets.QSizePolicy.Policy=...) -> None',
    }

    new_members = {
        # can use any method as a stand-in.  signatures will come from _signature_overrides
        'QByteArray': [
            ('__iter__', QtCore.QByteArray.__len__),
            ('__bytes__', QtCore.QByteArray.__len__)
        ],
        'QDialog': [
            # this method does not exist at the class-level, and only exists once an instance
            # is created.
            ('exec', QtWidgets.QDialog.exec_),
        ]
    }

    def __init__(self):
        # insert OptionalKeys
        self.signature_overrides = {
            (OptionalKey(key[0]),) + key[1:]: value
            for key, value in self._signature_overrides.items()
        }
        self.optional_args = {
            tuple(OptionalKey(k) for k in key): value
            for key, value in self._optional_args.items()
        }
        self.arg_type_overrides = {
            tuple(OptionalKey(k) for k in key): pyside(value)
            for key, value in self._arg_type_overrides.items()
        }
        self.arg_type_overrides.update({
            tuple(OptionalKey(k) for k in [None, None, None, orig]):
                'typing.Union[{},{}]'.format(orig, ','.join(alt))
            for orig, alt in self._implicit_arg_types.items()
        })
        self.arg_type_overrides.update({
            tuple(OptionalKey(k) for k in [None, None, None, 'typing.Union[{},NoneType]'.format(orig)]):
                'typing.Union[{},{},NoneType]'.format(orig, ','.join(alt))
            for orig, alt in self._implicit_arg_types.items()
        })
        self.arg_name_replacements = {
            tuple(OptionalKey(k) for k in key): pyside(value)
            for key, value in self._arg_name_replacements.items()
        }

    def get_function_sig(self, func: object, module_name: str, name: str
                         ) -> Optional[List[mypy.stubgenc.FunctionSig]]:
        if name == 'qVersion':
            return [mypy.stubgenc.FunctionSig('qVersion', [], 'str')]
        else:
            return None

    def get_method_sig(self, typ: type, func: object, module_name: str, class_name: str, name: str,
                       self_var: str) -> Optional[List[mypy.stubgenc.FunctionSig]]:
        docstr = None
        is_flag_type = False
        if typ is not None and (is_flag(typ) or is_flag_group(typ) or is_flag_item(typ)):
            docstr = self.flag_overrides.get(name)
            if docstr:
                is_flag_type = True
                if is_flag_item(typ):
                    return_type = get_group_from_flag_item(typ)
                else:
                    return_type = typ
                docstr = docstr.format(mypy.stubgenc.get_type_fullname(return_type))

        if not docstr:
            docstr = self.signature_overrides.get((OptionalKey(class_name), name))

        if docstr:
            # process our override
            if isinstance(docstr, list):
                docstr = '\n'.join(name + pyside(d) for d in docstr)
            else:
                docstr = name + pyside(docstr)
            results = mypy.stubgenc.infer_sig_from_docstring(docstr, name)
        else:
            # call the standard docstring-based generator
            results = self.docstring.get_method_sig(typ, func, module_name, class_name, name, self_var)

        if not is_flag_type and results:
            results = reduce_overloads(results)

            if typ and name == '__init__':
                add_property_args(typ, results)

            for i, inferred in enumerate(results):
                for arg in inferred.args:
                    if not arg.type:
                        continue
                    arg_type = arg.type.replace(' ', '')
                    arg_type = re.sub(r'\btyping\.Sequence\b', 'typing.Iterable', arg_type)
                    arg.type = arg_type

                    key = tuple(OptionalKey(k) for k in [class_name, name, arg.name, arg_type])

                    if key in self.arg_name_replacements:
                        arg.name = self.arg_name_replacements[key]

                    if key in self.optional_args:
                        # use Union[{}, NoneType] so that further replacements can be
                        # made by implicit_arg_types
                        optionality = self.optional_args[key]
                        if optionality.has_default:
                            arg.default = True
                        elif optionality.accepts_none:
                            arg.type = 'typing.Union[{},NoneType]'.format(arg_type)

                    if key in self.arg_type_overrides:
                        arg.type = self.arg_type_overrides[key]

                    # arg + type:
                    # note: QDataWidgetMapper.addMapping expects bytes
                    elif name != 'addMapping' and arg.name == 'propertyName' \
                            and short_name(arg_type) == 'QByteArray':
                        arg.type = 'str'
                    else:
                        new_type = get_flag_union(arg.type)
                        if new_type is not None:
                            arg.type = new_type

                new_type = get_flag_union(inferred.ret_type)
                if new_type is not None:
                    results[i] = inferred._replace(ret_type=new_type)
                if name == '__init__' and inferred.ret_type != 'None':
                    results[i] = inferred._replace(ret_type='None')

            new_overloads = self.new_overloads.get((class_name, name))
            if new_overloads:
                docstr = name + new_overloads
                results.extend(mypy.stubgenc.infer_sig_from_docstring(docstr, name))

        return results


def get_sig_generators(doc_dir: str) -> List[mypy.stubgenc.SignatureGenerator]:
    sig_generators = _orig_get_sig_generators(doc_dir)
    sig_generators.insert(0, PySideSignatureGenerator())
    return sig_generators


def is_skipped_attribute(attr: str, value: Any) -> bool:
    if not attr.isidentifier():
        return True
    # these are unecesssary
    if attr in ('__delattr__', '__setattr__', '__reduce__'):
        return True
    # many objects have __hash__ = None which causes mypy errors in the stubs. not sure how best
    # to handle this.  are these objects hashable?
    if attr == '__hash__' and value is None:
        return True
    return False


def is_c_method(obj: object) -> bool:
    # QtCore.Signal gets mistaken for a method descriptor because it has a __get__
    if type(obj).__name__ == 'Signal':
        return False
    return _orig_is_c_method(obj)


def get_flag_union(type_name: str) -> Optional[str]:
    """
    arguments that are group flags should also accept the corresponding item flag
    """
    item_type_name = _flag_group_to_item.get(type_name)
    if item_type_name:
        result = 'typing.Union[{}, {}]'.format(type_name, item_type_name)
        return result
    return None


def strip_or_import(type_name: str, module: ModuleType, known_modules: List[str],
                    imports: List[str]) -> str:
    type_name = type_name.replace('Shiboken.', 'shiboken2.')
    stripped_type = _orig_strip_or_import(type_name, module, known_modules, imports)
    return stripped_type


def walk_objects(obj, seen):
    for attr, child in mypy.stubgenc.get_members(obj):
        if mypy.stubgenc.is_c_type(child):
            if child in seen:
                continue
            seen.add(child)
            # add to the cache
            get_properties(child)
            if is_flag_item(child):
                # add to the cache
                get_group_from_flag_item(child)
            walk_objects(child, seen)


def get_members(obj: Union[type, ModuleType]) -> List[Tuple[str, Any]]:
    members = [x for x in _orig_get_members(obj) if not is_skipped_attribute(x[0], x[1])]
    if isinstance(obj, type):
        return members + PySideSignatureGenerator.new_members.get(obj.__name__, [])
    return members


def generate_stub_for_c_module(module_name: str,
                               target: str,
                               known_modules: Iterable[str],
                               sig_generators: Iterable[mypy.stubgenc.SignatureGenerator]) -> None:
    if not _flag_group_to_item:
        seen = set()
        for known_module_name in known_modules:
            module = importlib.import_module(known_module_name)
            walk_objects(module, seen)
    return _orig_generate_stub_for_c_module(module_name, target, known_modules, sig_generators)


def add_typing_import(output: List[str]) -> List[str]:
    # we don't call the original function because we don't want the standard typing imports:
    # `from tying import Any` causes conflicts in QtNetwork
    for i, line in enumerate(output):
        if line.startswith('import typing'):
            return output[:i] + [line, "T = typing.TypeVar('T')"] + output[i + 1:]
    return output


mypy.stubgenc.is_c_method = is_c_method
mypy.stubgenc.strip_or_import = strip_or_import
mypy.stubgen.get_sig_generators = get_sig_generators
mypy.stubgenc.generate_stub_for_c_module = generate_stub_for_c_module
mypy.stubgen.generate_stub_for_c_module = generate_stub_for_c_module
mypy.stubgenc.add_typing_import = add_typing_import
mypy.stubgenc.get_members = get_members

if __name__ == '__main__':
    # in order to create and inspect object properties we must create an app
    app = QtWidgets.QApplication()

    mypy.stubgen.main()
