"""Provide common definitions"""

from collections import namedtuple
from functools import reduce, partial

Item = namedtuple('Item', 'title text url')

def compose(*funcs):
    """Return the composition of funcs as a function of one variable.

The innermost function is the first given, ie:
compose(f, g, h)(x) -> h(g(f(x)))"""
    return partial(reduce, lambda f, g: g(f), funcs)
