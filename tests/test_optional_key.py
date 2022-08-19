from __future__ import absolute_import, print_function

import sys
sys.path.append('..')


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
