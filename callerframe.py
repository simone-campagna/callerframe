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
The callerframe decorator adds a <__caller_frame__> global attribute to the
decorated function's globals; this attribute refers to the caller's frame
information:

>>> @callerframe
... def log(kind, message):
...     print("{}: function {}: {}".format(kind, __caller_frame__.function_name, message))
...
>>> def foo():
...     log("error", "lost connection")
...
>>> def main():
...     return foo()
...
>>> main()
error: function foo: lost connection

The log function receives information about it's direct caller; but what if we want
to have an error() function based on log()?

>>> def error(message):
...     log("error", message)
...
>>> def foo():
...     error("lost connection")
...
>>> def main():
...     return foo()
...
>>> main()
error: function error: lost connection

This is correct, since error() is the direct caller of the log() function; but we would
like to show the information about the error's caller instead. In this case it is possible
to decorate error() too:

>>> @callerframe
... def error(message):
...     log("error", message)
...
>>> def foo():
...     error("lost connection")
...
>>> def main():
...     return foo()
...
>>> main()
error: function foo: lost connection

In other words, the first decorated function found in the call stack sets the
caller information.

The attribute name can be choosen:

>>> @callerframe("CALLERFRAME")
... def show_caller():
...     print(CALLERFRAME.function_name)
...
>>> def foo():
...     show_caller()
...
>>> foo()
foo

"""

__all__ = [
    'FrameInfo',
    'callerframe',
]
__version__ = "1.0.1"

import collections
import contextlib
import functools
import inspect


FrameInfo = collections.namedtuple("FrameInfo", ("frame", "filename", "line_number",
                                                 "function_name", "context", "index"))


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
        glb[attr_name] = FrameInfo(*inspect.getouterframes(frame)[depth])
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
