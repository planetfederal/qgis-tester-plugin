import os
import glob
import importlib
import pkgutil
import unittest
from qgistester.test import Test, UnitTestWrapper


def tests():
	_tests = []
	prefix = __name__ + "."
	path = __path__
	for importer, modname, ispkg in pkgutil.iter_modules(path, prefix):
		modtests = []
		group = modname.split(".")[-1]
		module = __import__(modname, fromlist="dummy")
		if "tests" in dir(module):
			modtests.extend(module.tests())
		if "suite" in dir(module):
			modtests.extend([UnitTestWrapper(unit) for unit in module.suite()])
		for t in modtests:
			t.group = group
		_tests.extend(modtests)
	return  _tests
