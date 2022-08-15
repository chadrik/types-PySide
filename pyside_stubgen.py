from __future__ import absolute_import, print_function

import inspect
import importlib
import pydoc
import typing
from typing import Any, List, Optional, Iterable, Mapping, Tuple
from types import ModuleType
from functools import lru_cache, total_ordering

import mypy.stubgen
import mypy.stubgenc
import mypy.stubdoc
import mypy.nodes
import mypy.types
import mypy.fastparse
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

# TODO: support PySide6
PYSIDE = 'PySide2'


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


def is_redundant_overload(sig: mypy.stubgenc.FunctionSig, sigs: List[mypy.stubgenc.FunctionSig]):
    if len(sigs) <= 1:
        return False

    num_args = len(sig.args)
    # sort from longest to shortest
    sigs = sorted(sigs, key=lambda x: len(x.args), reverse=True)
    for other in sigs:
        if len(other.args) <= num_args:
            # everyting after this has the same or fewer args
            break
        if other.args[:num_args] == sig.args and all(a.default for a in other.args[num_args:]) \
                and other.ret_type == sig.ret_type:
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


assert OptionalKey('foo') == None
assert OptionalKey('foo') == 'foo'
assert OptionalKey('foo') == OptionalKey(None)
{OptionalKey(None): 'this'}[OptionalKey('foo')]
{OptionalKey('foo'): 'this'}[OptionalKey('foo')]
# {(None, 'bar'): 'this'}[(OptionalKey('foo'), 'bar')]
{OptionalKey(None): 'this'}[OptionalKey('foo')]
{(OptionalKey(None), 'bar'): 'this'}[(OptionalKey('foo'), 'bar')]

ANY = None


class PySideSignatureGenerator(mypy.stubgenc.SignatureGenerator):
    docstring = mypy.stubgenc.DocstringSignatureGenerator()

    # Complete signature replacements.
    # The class name can be None, in which case it will match
    _signature_overrides = {
        # these docstring sigs are malformed
        ('VolatileBool', 'get'):
            '(self) -> bool',
        ('VolatileBool', 'set'):
            '(self, a: object) -> None',

        # add missing type info
        ('Signal', '__get__'):
            [
                '(self, instance: None, owner: typing.Type[QObject]) -> Signal',
                '(self, instance: QObject, owner: typing.Type[QObject]) -> SignalInstance',
            ],
        ('Signal', '__getitem__'):
            '(self, index) -> SignalInstance',
        ('SignalInstance', '__getitem__'):
            '(self, index) -> SignalInstance',

        # slot arg should be typing.Callable instead of object
        ('SignalInstance', 'connect'):
            '(self, slot: typing.Callable, type: typing.Union[type,None] = ...) -> bool',
        ('SignalInstance', 'disconnect'):
            '(self, slot: typing.Union[typing.Callable,None] = ...) -> None',

        # FIXME: QObject.connect overloads use a mixture of methods and classmethods.  does mypy support this?  if not can we use a descriptor?  should these overloads be moved to SignalInstance?
        # docstring sig for these declare name as bytes, which is not correct.
        # not sure how many more issues like this exist.
        ('QObject', 'setProperty'):
            '(self, name: str, value: typing.Any) -> bool',
        ('QObject', 'property'):
            '(self, name: str) -> typing.Any',
        ('QState', 'assignProperty'):
            '(self, object: QObject, name: str, value: typing.Any) -> None',
        (ANY, 'propertyName'):
            '(self) -> str',
        ('QCoreApplication', 'translate'):
            '(cls, context: str, key: str, disambiguation: typing.Union[str,NoneType] = ..., n: int = ...) -> str',
        # Other issues
        ('QTreeWidgetItemIterator', '__iter__'):
            '(self) -> typing.Iterator[QTreeWidgetItemIterator]',
        ('QTreeWidgetItemIterator', '__next__'):
            '(self) -> QTreeWidgetItemIterator',
        ('QLayout', 'itemAt'):
            # make optional
            '(self, index: int) -> typing.Optional[PySide*.QtWidgets.QLayoutItem]',
        ('QLayout', 'takeAt'):
            # make optional
            '(self, index: int) -> typing.Optional[PySide*.QtWidgets.QLayoutItem]',
        ('QPolygon', '__lshift__'):
            # first and third overload should return QPolygon
            [
                '(self, l: typing.List[PySide2.QtCore.QPoint]) -> PySide2.QtCore.QPolygon',
                '(self, stream: PySide2.QtCore.QDataStream) -> PySide2.QtCore.QDataStream',
                '(self, t: PySide2.QtCore.QPoint) -> PySide2.QtCore.QPolygon',
            ],
        ('QPolygon', '__iadd__'):
            # should return QPolygon
            '(self, t: PySide2.QtCore.QPoint) -> PySide2.QtCore.QPolygon',

        # QByteArray
        ('QByteArray', '__getitem__'):
            # missing index and return
            '(self, index: int) -> bytes',

        # Replace object with Any:
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
            '(self, arg__1: typing.Union[PySide*.QtWidgets.QFrame.Shape, '
            'PySide*.QtWidgets.QFrame.Shadow, typing.SupportsInt]) -> None',
        # in PySide2 this takes int, and in PySide6 it takes Weight, but both seem valid
        ('QFont', 'setWeight'):
            '(self, arg__1: typing.Union[int, PySide*.QtGui.QFont.Weight]) -> None',
        # ('QFont', 'weight'): pyside('(self) -> PySide*.QtGui.QFont.Weight'),  # fixed in PySide6

        # Fix QModelIndex typed as int in many places:
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

        # Generics:
        ('QCoreApplication', 'instance'):
            '(cls: typing.Type[T]) -> T',
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
    _arg_type_overrides = {
        'PySide2.QtGui.QKeySequence':
            ['str'],
        'PySide2.QtGui.QColor':
            ['PySide2.QtCore.Qt.GlobalColor'],
        'PySide2.QtCore.QByteArray':
            ['bytes'],
        'PySide2.QtGui.QBrush':
            ['PySide2.QtGui.QColor', 'PySide2.QtCore.Qt.GlobalColor'],
        'PySide2.QtGui.QCursor':
            ['PySide2.QtCore.Qt.CursorShape'],
    }

    # Values which should be made Optional[].
    # the bool indicates if the argument has a default (e.g. arg = ...)
    _optional_args = {
        ('QPainter', 'drawText', 'br'): True,
        ('QPainter', 'drawPolygon', 'arg__2'): True,
        ('QProgressDialog', 'setCancelButton', 'button'): False,
        (ANY, 'setModel', 'model'): False,
        ('QLabel', 'setPixmap', 'arg__1'): False,
    }

    # Add new overloads to existing functions.
    new_overloads = {
        ('QDate', '__init__'):
            '(self, date: datetime.date) -> None',
        ('QDateTime', '__init__'):
            '(self, datetime: datetime.datetime) -> None',
    }

    def __init__(self):
        arg_type_overrides = {
            orig: 'typing.Union[{},{}]'.format(orig, ','.join(alt))
            for orig, alt in self._arg_type_overrides.items()
        }
        arg_type_overrides.update({
            'typing.Union[{},NoneType]'.format(orig):
                 'typing.Union[{},{},NoneType]'.format(orig, ','.join(alt))
            for orig, alt in self._arg_type_overrides.items()
        })
        self.arg_type_overrides = arg_type_overrides

        self.signature_overrides = {
            (OptionalKey(key[0]),) + key[1:]: value
            for key, value in self._signature_overrides.items()
        }
        self.optional_args = {
            (OptionalKey(key[0]),) + key[1:]: value
            for key, value in self._optional_args.items()
        }

    def get_function_sig(self, func: object, module_name: str, name: str
                         ) -> Optional[List[mypy.stubgenc.FunctionSig]]:
        pass

    def get_method_sig(self, func: object, module_name: str, class_name: str, name: str,
                       self_var: str) -> Optional[List[mypy.stubgenc.FunctionSig]]:
        typ = getattr(func, '__objclass__', None)
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
            results = self.docstring.get_method_sig(func, module_name, class_name, name, self_var)

        if not is_flag_type and results:

            # FIXME: make this more efficient: don't check the same combinations twice
            results = [x for x in results if not is_redundant_overload(x, results)]
            if typ and name == '__init__':
                add_property_args(typ, results)

            for i, inferred in enumerate(results):
                for arg in inferred.args:
                    if not arg.type:
                        continue
                    arg_type = arg.type.replace(' ', '')
                    if (OptionalKey(class_name), name, arg.name) in self.optional_args:
                        # use Union[{}, NoneType] so that further replacements can be
                        # made by arg_type_overrides
                        has_default = self.optional_args[(OptionalKey(class_name), name, arg.name)]
                        if has_default:
                            arg.default = True
                        else:
                            arg.type = 'typing.Union[{},NoneType]'.format(arg_type)
                    # FIXME: replace typing.Sequence with typing.Iterable
                    # arg + type:
                    if arg.name == 'parent' and short_name(arg_type) in ('QWidget', 'QObject'):
                        arg.type = 'typing.Optional[{}]'.format(arg_type)
                    elif arg.name in ('flags', 'weight') and arg_type == 'int':
                        arg.type = 'typing.SupportsInt'
                    elif arg.name == 'format' and arg_type == 'typing.Union[bytes,NoneType]':
                        arg.type = 'typing.Optional[str]'
                    elif arg.name == 'role' and arg_type == 'int':
                        arg.type = pyside('PySide*.QtCore.Qt.ItemDataRole')
                    # note: QDataWidgetMapper.addMapping expects bytes
                    elif name != 'addMapping' and arg.name == 'propertyName' \
                            and short_name(arg_type) == 'QByteArray':
                        arg.type = 'str'
                    # method + type:
                    elif name == 'addAction' and arg_type == 'object':
                        arg.type = 'typing.Callable[[], typing.Any]'
                    # type replacements with no arg name requirement:
                    elif arg_type in self.arg_type_overrides:
                        arg.type = self.arg_type_overrides[arg_type]
                    else:
                        new_type = get_flag_union(arg.type)
                        if new_type is not None:
                            arg.type = new_type
                new_type = get_flag_union(inferred.ret_type)
                if new_type is not None:
                    results[i] = inferred._replace(ret_type=new_type)

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
    # these are unecesssary
    if attr in ('__delattr__', '__setattr__', '__reduce__'):
        return True
    # many objects have __hash__ = None which causes mypy errors in the stubs. not sure how best
    # to handle this.  are these objects hashable?
    if attr == '__hash__' and value is None:
        return True
    return _orig_is_skipped_attribute(attr, value)


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


def strip_or_import(type_name: str, module: ModuleType, known_modules: List[str], imports: List[str]
                    ) -> str:
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
    # output = _orig_add_typing_import(output)
    for i, line in enumerate(output):
        if line.startswith('import typing'):
            return output[:i] + [line, "T = typing.TypeVar('T')"] + output[i + 1:]
    return output


mypy.stubgenc.is_skipped_attribute = is_skipped_attribute
mypy.stubgenc.is_c_method = is_c_method
mypy.stubgenc.strip_or_import = strip_or_import
mypy.stubgen.get_sig_generators = get_sig_generators
mypy.stubgenc.generate_stub_for_c_module = generate_stub_for_c_module
mypy.stubgen.generate_stub_for_c_module = generate_stub_for_c_module
mypy.stubgenc.add_typing_import = add_typing_import

# in order to create and inspect object properties we must create an app
app = QtWidgets.QApplication()

mypy.stubgen.main()
print('done')
