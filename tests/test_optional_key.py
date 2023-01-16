from __future__ import absolute_import, print_function

import pytest
import PySide2

pyside_version = PySide2.__version_info__


@pytest.mark.skipif(pyside_version < (5, 14), reason="fails in PySide2 < 5.14.2.3")
def test_optiona_key():
    from pyside_stubgen import OptionalKey

    assert OptionalKey('foo') == None
    assert OptionalKey('foo') == 'foo'
    assert OptionalKey('foo') == OptionalKey(None)
    {OptionalKey(None): 'this'}[OptionalKey('foo')]
    {OptionalKey('foo'): 'this'}[OptionalKey('foo')]
    # {(None, 'bar'): 'this'}[(OptionalKey('foo'), 'bar')]
    {OptionalKey(None): 'this'}[OptionalKey('foo')]
    {(OptionalKey(None), 'bar'): 'this'}[(OptionalKey('foo'), 'bar')]
