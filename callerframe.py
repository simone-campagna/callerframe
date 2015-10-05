# -*- coding: utf-8 -*-
#
# Copyright 2013 Simone Campagna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Python decorator adding a __caller_frame__ attribute to function's globals.

>>> @callerframe
... def foo():
...     frame, filename, line_number, function_name, context, index = __caller_frame__
...     return function_name
...
>>> def fun0():
...     return foo()
...
>>> def fun1():
...     return fun0()
...
>>> fun1()
'fun0'

In the following example fun2 is also decorated with caller frame; in this case,
when called through fun2() -> fun0() -> foo(), the caller frame in foo will be
the caller frame of fun2:

>>> @callerframe
... def fun2():
...     return fun0()
...
>>> def fun3():
...     return fun2()
...
>>> fun3()
'fun3'

"""

__all__ = [
    'callerframe',
]
__version__ = "1.0.0"

import contextlib
import functools
import inspect


class DecoratorMaker(object):  # pylint: disable=too-few-public-methods
    """DecoratorMaker - creates a decorator/decorator factory object"""
    def __init__(self, decorator_factory):
        self.decorator_factory = decorator_factory
        self._default_decorator = None

    @property
    def default_decorator(self):
        """Returns the default decorator

        Returns
        -------
        function
            the default decorator
        """
        if self._default_decorator is None:
            self._default_decorator = self.decorator_factory()
        return self._default_decorator

    def __call__(self, function, *args, **kwargs):
        if len(args) + len(kwargs) == 0 and callable(function):
            # direct call
            return self.default_decorator(function)  # pylint: disable=not-callable
        else:
            # indirect call
            return self.decorator_factory(function, *args, **kwargs)


@contextlib.contextmanager
def _update_globals(glb, frame, depth, attr_name):
    """Updates the globals dictionary with 'attr_name = <caller frame>', if not available
    """
    remove = False
    if glb.get(attr_name) is None:
        glb[attr_name] = inspect.getouterframes(frame)[depth]
        remove = True
    yield glb
    if remove:
        del glb[attr_name]


def callerframe_decorator_factory(attr_name="__caller_frame__"):
    """Returns a callerframe decorator

    Attributes
    ----------
    attr_name: str, optional
        the name of the global attribute to be added to the decorated function
        [defaults to "__caller_frame__"]

    Returns
    -------
    function
        the decorator adding <attr_name> to the decorated function's globals
    """
    def callerframe_decorator(function):
        """Function decorators that insert an 'attr_name = <caller frame>' attribute to the function globals
        """
        @functools.wraps(function)
        def wrap(*args, **kwargs):
            """Decorated function"""
            with _update_globals(function.__globals__, inspect.currentframe(), 1, attr_name):
                return function(*args, **kwargs)
        return wrap
    return callerframe_decorator


callerframe = DecoratorMaker(callerframe_decorator_factory)  # pylint: disable=invalid-name
