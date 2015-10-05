#!/usr/bin/env python
# -*- coding: utf-8 -*-

_glb0 = globals().copy()
from callerframe import *
_glb1 = globals().copy()

def test_import0():
    assert 'callerframe' in globals()
    assert 'FrameInfo' in globals()

def test_import1():
    g1 = set(_glb1.keys())
    g1.remove('_glb0')
    for key in g1.difference(_glb0.keys()):
        assert key in {'callerframe', 'FrameInfo'}
