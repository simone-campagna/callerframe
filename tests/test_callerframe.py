#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from callerframe import callerframe


@callerframe
def fun0():
    return __caller_frame__

def caller0_0():
    return fun0()

def caller0_1():
    return caller0_0()

def caller0_2():
    return caller0_1()

@pytest.fixture(params=[caller0_0, caller0_1, caller0_2])
def caller0(request):
    return request.param

def test_callerframe_caller0(caller0):
    frame, filename, line_number, function_name, context, index = caller0()
    assert filename == __file__
    assert function_name == "caller0_0"

@callerframe
def caller1_0():
    return fun0()

def caller1_1():
    return caller1_0()

def caller1_2():
    return caller1_1()

@pytest.fixture(params=[caller1_1, caller1_2])
def caller1(request):
    return request.param

def test_callerframe_caller1(caller1):
    frame, filename, line_number, function_name, context, index = caller1()
    assert filename == __file__
    assert function_name == "caller1_1"

@callerframe("__cf__")
def fun2():
    return __cf__

@callerframe("__cf__")
def caller2_0():
    return fun2()

def caller2_1():
    return caller2_0()

def caller2_2():
    return caller2_1()

@pytest.fixture(params=[caller2_1, caller2_2])
def caller2(request):
    return request.param

def test_callerframe_caller1(caller2):
    frame, filename, line_number, function_name, context, index = caller2()
    assert filename == __file__
    assert function_name == "caller2_1"

