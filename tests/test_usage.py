# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import pytest
from magic_parameter import *  # noqa


def test_function_parameter():

    @function_parameter([
        ('a', int),
        ('b', float),
    ])
    def example(args):
        assert args.a == 1
        assert args.b == 1.0

    example(1, 1.0)
    example(b=1.0, a=1)
    with pytest.raises(AssertionError):
        example(2, 1.0)

    with pytest.raises(TypeError):
        example(1)
    with pytest.raises(TypeError):
        example(1.0)
    with pytest.raises(TypeError):
        example(1, a=1)


def test_method_parameter():

    class Case1(object):

        @classmethod
        @method_parameter(
            [
                ('a', int),
            ],
            pass_by_cls_or_self_attributes=True,
        )
        def test_cls(cls):
            assert cls.a == 1

        @method_parameter(
            [
                ('a', int),
            ],
            pass_by_cls_or_self_attributes=True,
            no_warning_on_cls_or_self_attributes=False,
        )
        def test_self1(self):
            assert self.a == 1

        @method_parameter(
            [
                ('a', int),
            ],
            pass_by_function_argument=True,
        )
        def test_self2(self, args):
            assert args.a == 1

    Case1.test_cls(1)
    Case1.test_cls(a=1)
    with pytest.raises(AssertionError):
        Case1.test_cls(2)

    case1 = Case1()
    case1.test_self1(1)
    case1.test_self2(1)

    with pytest.raises(TypeError):
        case1.test_self1(1)
    case1.test_self2(1)

    with pytest.raises(SyntaxError):

        class Case2(object):

            @classmethod
            @method_parameter(
                [
                    ('a', int),
                ],
                # pass_by_cls_or_self_attributes=True,
            )
            def test_cls(cls):
                pass

    with pytest.raises(TypeError):
        method_parameter([], pass_by_function_argument=True)(1)


def test_method_init_parameter():

    class Case1(object):

        @method_init_parameter([
            ('a', int),
        ])
        def __init__(self):
            assert self.a == 1

    Case1(1)
    Case1(a=1)
    with pytest.raises(AssertionError):
        Case1(2)

    with pytest.raises(TypeError):
        Case1(b=1)
    with pytest.raises(TypeError):
        Case1(1.0)


def test_class_init_parameter():

    @class_init_parameter
    class Case1(object):

        PARAMETERS = [
            ('a', int),
        ]

        def __init__(self):
            assert self.a == 1

    Case1(1)
    Case1(a=1)
    with pytest.raises(AssertionError):
        Case1(2)

    @class_init_parameter
    class Case2(object):

        PARAMETERS = [
            ('a', int),
        ]

    Case2(1)
    Case2(a=1)

    with pytest.raises(SyntaxError):
        class_init_parameter(1)


def test_nested_type():

    @function_parameter([
        ('a', list_t(int)),
        ('b', list_t(or_t(int, float)), None),
    ])
    def func1(args):
        return args.a, args.b

    r1, r2 = func1([1, 2])
    assert r1 == [1, 2]
    assert r2 is None
    assert [1, 2], [1, 2.0] == func1([1, 2], [1, 2.0])

    with pytest.raises(TypeError):
        func1([1.0, 2.0])

    with pytest.raises(TypeError):
        func1(a=[1], b=['test'])

    @function_parameter([
        ('a', dict_t(str, int)),
    ])
    def func2(args):
        return args.a

    assert {'a': 1, 'b': 2} == func2({'b': 2, 'a': 1})

    with pytest.raises(TypeError):
        func2({'a': 1.0})

    with pytest.raises(TypeError):
        func2({1: 1})
