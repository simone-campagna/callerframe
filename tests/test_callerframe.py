#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import inspect

import pytest

from callerframe import callerframe, FrameInfo


class SourceLine(object):
    def __init__(self):
        self.info = {}

    def tag(self, tag, expr_value):
        self.info[tag] = FrameInfo(*inspect.getouterframes(inspect.currentframe())[1])
        return expr_value

    def get_info(self, tag):
        return self.info[tag]

SOURCE_LINE = SourceLine()

@callerframe
def fun0():
    return __caller_frame__

def test_no_globals():
    assert '__caller_frame__' not in globals()
    SOURCE_LINE.tag("fun0", fun0())
    assert '__caller_frame__' not in globals()

def test_no_globals_1():
    @callerframe
    def funX():
        return __caller_frame__
    assert '__caller_frame__' not in globals()
    SOURCE_LINE.tag("funX", funX())
    assert '__caller_frame__' not in globals()
    
def caller0_0():
    return SOURCE_LINE.tag("caller0_0", fun0())

def caller0_1():
    return SOURCE_LINE.tag("caller0_1", caller0_0())

def caller0_2():
    return SOURCE_LINE.tag("caller0_2", caller0_1())

@pytest.fixture(params=[caller0_0, caller0_1, caller0_2])
def caller0(request):
    return request.param

def test_callerframe_caller0(caller0):
    frame_info = caller0()
    ref_frame_info = SOURCE_LINE.get_info("caller0_0")
    assert frame_info == ref_frame_info

@callerframe
def caller1_0():
    return SOURCE_LINE.tag("caller1_0", fun0())

def caller1_1():
    return SOURCE_LINE.tag("caller1_1", caller1_0())

def caller1_2():
    return SOURCE_LINE.tag("caller1_2", caller1_1())

@pytest.fixture(params=[caller1_1, caller1_2])
def caller1(request):
    return request.param

def test_callerframe_caller1(caller1):
    frame_info = caller1()
    ref_frame_info = SOURCE_LINE.get_info("caller1_1")
    assert frame_info == ref_frame_info

@callerframe("__cf__")
def fun2():
    return __cf__

@callerframe("__cf__")
def caller2_0():
    return SOURCE_LINE.tag("caller2_0", fun2())

def caller2_1():
    return SOURCE_LINE.tag("caller2_1", caller2_0())

def caller2_2():
    return SOURCE_LINE.tag("caller2_2", caller2_1())

@pytest.fixture(params=[caller2_1, caller2_2])
def caller2(request):
    return request.param

def test_callerframe_caller2(caller2):
    frame_info = caller2()
    ref_frame_info = SOURCE_LINE.get_info("caller2_1")
    assert frame_info == ref_frame_info

