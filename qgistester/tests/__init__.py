# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import glob
import importlib
import pkgutil
import unittest
from qgistester.test import Test, UnitTestWrapper


def findTests():
    _tests = []
    prefix = __name__ + "."
    path = __path__
    for importer, modname, ispkg in pkgutil.iter_modules(path, prefix):
        modtests = []
        group = modname.split(".")[-1]
        module = __import__(modname, fromlist="dummy")
        if "functionalTests" in dir(module):
            modtests.extend(module.functionalTests())
        if "unitTests" in dir(module):
            modtests.extend([UnitTestWrapper(unit) for unit in module.unitTests()])
        for t in modtests:
            t.group = group
        _tests.extend(modtests)
    return  _tests

tests = findTests()

def addTestModule(module, group = None):
    modtests = []
    group = group or module.__name__.split(".")[-1]
    if "functionalTests" in dir(module):
        modtests.extend(module.functionalTests())
    if "unitTests" in dir(module):
        modtests.extend([UnitTestWrapper(unit) for unit in module.unitTests()])
    for t in modtests:
        t.group = group
    tests.extend(modtests)
