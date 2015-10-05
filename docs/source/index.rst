.. callerframe documentation master file, created by
   sphinx-quickstart on Sun Oct  4 21:56:23 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. include:: ../macros.txt

.. testsetup::

    from callerframe import *

.. |inspect| replace:: :py:class:`inspect <python:inspect>`


The callerframe decorator
=========================

The `callerframe` decorator adds to the decorated function information about it's caller. This information can be accessed through the ``__caller_frame__`` attribute, which is inserted into the function's globals. The information is the namedtuple ``FrameInfo`` containing:

* ``frame``: the caller's frame
* ``filename``: the filename
* ``line_number``: the line number
* ``function_name``: the function name
* ``context``: a list of context lines
* ``index``: the index of the line in the ``context`` where the call is done

Motivation
----------
Suppose you want to define a ``log()`` function:

 >>> def log(kind, message):
 ...     print("{}: {}".format(kind, message))
 ...
 >>> log("error", "lost connection")
 error: lost connection
 >>>

You may want to automatically add to the log some information about the caller, for instance:

 >>> def log(kind, message):
 ...     print("{}: function {}: {}".format(kind, function_name, message))

so you need to obtain the callers' function name, and eventually the filename or the line number.

Using |inspect| you can easily obtain such information:

 >>> import inspect
 >>> def log(kind, message):
 ...     frame, filename, line_number, function_name, context, index = inspect.getouterframes(inspect.currentframe())[1]
 ...     print("{}: function {}: {}".format(kind, function_name, message))
 ...
 >>> def foo():
 ...    log("error", "lost connection")
 ...
 >>> foo()
 error: function foo: lost connection

But what if you want to define also an ``error`` function using the log one? In this cast ``log`` should show information about the ``error``'s caller,
and not about it's direct caller:

 >>> def error(message):
 ...     log("error", message)
 ...
 >>> def bar():
 ...    error("lost connection")
 ...
 >>> bar()
 error: function error: lost connection

Notice that the ``log()`` function should behave as above when called directly, showing its direct caller's name. But it should show
the ``error()`` caller's name when called through ``error()``.

Solution
--------
The ``callerframe`` decorator can solve these problems. First of all, it adds to the decorated function's globals a ``__caller_frame__``
attribute containing all the information about the caller:

 >>> @callerframe
 ... def log(kind, message):
 ...     print("{}: function {}: {}".format(kind, __caller_frame__.function_name, message))
 ...
 >>> def foo():
 ...    log("error", "lost connection")
 ...
 >>> foo()
 error: function foo: lost connection

Moreover, it is possible to use the same decorator for the ``error`` function too: in this case, when called through ``error``, ``log`` will
receive the ``error``'s caller:

 >>> @callerframe
 ... def error(message):
 ...     log("error", message)
 ...
 >>> def bar():
 ...    error("lost connection")
 ...
 >>> bar()
 error: function bar: lost connection
 
In general, the first decorated function in a call stack sets the caller's information.

It is possible to change the name of the added attribute:

 >>> @callerframe("CALLERFRAME")
 ... def show_caller():
 ...     print(CALLERFRAME.function_name)
 ...
 >>> def foo():
 ...     show_caller()
 ...
 >>> foo()
 foo

Contents:

.. toctree::
    :maxdepth: 1

    reference/callerframe

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

