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
		module = __import__(modname, fromlist="dummy")
		if "tests" in dir(module):
			_tests.extend(module.tests())
		if "suite" in dir(module):
			for unit in module.suite():
				_tests.append(UnitTestWrapper(modname.split(".")[-1], unit))
	return  _tests
