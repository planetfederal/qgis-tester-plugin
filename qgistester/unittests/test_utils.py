# -*- coding: utf-8 -*-
"""Test utils.py."""
from __future__ import absolute_import
from builtins import map
from builtins import range
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import os
import utilities
import tempfile
try:
    import mock
except ImportError:
    import unittest.mock as mock
import time
import traceback
import threading
from qgistesting import start_app
from qgistesting.mocked import get_iface
from qgis.core import (QgsVectorLayer,
                       QgsProject,
                       QgsVectorFileWriter)
from qgistester.utils import (layerFromName,
                              loadLayerNoCrsDialog,
                              execute)
import qgistester.utils as utils

try:
    from PyQt4.QtCore import QSettings, QObject, pyqtSignal
except ImportError:
    from PyQt5.QtCore import QSettings, QObject, pyqtSignal

__author__ = 'Luigi Pirelli'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'


class UtilsTests(unittest.TestCase):
    """Tests for the utility functions in utils.py."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()
        cls.QGIS_APP = start_app()
        assert cls.QGIS_APP is not None
        cls.IFACE_Mock = get_iface()
        assert cls.IFACE_Mock is not None
        # create test data
        cls.testFile1 = QgsVectorLayer('Point', 'testFile1', 'memory')
        assert cls.testFile1.isValid()
        cls.testFile2 = QgsVectorLayer('Point', 'testFile2', 'memory')
        assert cls.testFile2.isValid()
        cls.testFile3 = QgsVectorLayer('Point', 'testFile3', 'memory')
        assert cls.testFile3.isValid()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testLayerFromName(self):
        """check if giving a layer name it's instance is returned."""
        # test 1: not layer is present
        layer = layerFromName('testFile2')
        self.assertIsNone(layer)

        # preconditions
        QgsProject.instance().addMapLayer(self.testFile1)
        QgsProject.instance().addMapLayer(self.testFile2)
        QgsProject.instance().addMapLayer(self.testFile3)
        # do test 2: look for the 'testFile2' that exists
        layer = layerFromName('testFile2')
        self.assertEqual(self.testFile2, layer)

        # do test 3: look for the 'unexist' that does not exists
        layer = layerFromName('unexist')
        self.assertIsNone(layer)

    @unittest.skip("Skip test tested using testLoadLayerNoCrsDialog")
    def testLoadLayer(self):
        """load a lyer or exception. Tested using testLoadLayerNoCrsDialog."""
        self.assertTrue(False)

    def testLoadLayerNoCrsDialog(self):
        """load a layer file without opening CRS dialog."""
        # preconditions
        tf = tempfile.NamedTemporaryFile()
        tempFileName = tf.name + '.shp'
        tf.close()
        QgsVectorFileWriter.writeAsVectorFormat(self.testFile1, tempFileName,
                                                'utf-8', None)
        basename = os.path.basename(tempFileName)
        name = os.path.splitext(basename)[0]
        # test 1: load vector layer
        settings = QSettings()
        enterSetting = settings.value('/Projections/defaultBehaviour')
        layer = loadLayerNoCrsDialog(tempFileName)
        exitSetting = settings.value('/Projections/defaultBehaviour')
        self.assertEqual(enterSetting, exitSetting)
        self.assertEqual(layer.name(), name)
        # test 2: load a vector layer giving a layer name
        wouldHaveName = "expected layer name"
        layer = loadLayerNoCrsDialog(tempFileName, wouldHaveName)
        self.assertEqual(layer.name(), wouldHaveName)
        # test 3: load raster layer (the plugin png)
        rasterFileName = os.path.abspath(os.path.join(
                                         os.path.dirname(__file__),
                                         os.path.pardir,
                                         'plugin.png'))
        layer = loadLayerNoCrsDialog(rasterFileName)
        self.assertEqual(layer.name(), 'plugin')
        # test 4: load an unexistent layer
        rasterFileName = rasterFileName + '_unexistent'
        try:
            layer = loadLayerNoCrsDialog(rasterFileName)
        except RuntimeError:
            # test success
            pass
        except:
            self.assertTrue(False, msg='Received unexpected exception type')
        else:
            self.assertTrue(False, msg='Expected RuntimeError but not rised')

    def testExecute(self):
        """Test execution of long time task managing"""
        # precondition
        self.lenghtyFuncRunningFailed = False
        self.lenghtyFuncRunningFailedMessage = ''
        self.threadStartedFlag = False
        self.threadTerminatedFlag = False
        self.threadRunningCounter = 0

        def lenghtyFuncStarted():
            self.threadStartedFlag = True

        def lenghtyFuncTerminated():
            self.threadTerminatedFlag = True

        def lenghtyFuncRunning(step):
            self.threadRunningCounter = step

        class RunningClass(QObject):
            '''added signals to check that the function is executed in the
            main thread.'''
            threadStarted = pyqtSignal()
            threadTerminated = pyqtSignal()
            threadRunning = pyqtSignal(int)

            def lenghtyFunc(self):
                if threading.current_thread().name != 'MainThread':
                    self.threadStarted.emit()
                for i in range(1,6):
                    time.sleep(0.5)
                    if threading.current_thread().name != 'MainThread':
                        self.threadRunning.emit(i)
                if threading.current_thread().name != 'MainThread':
                    self.threadTerminated.emit()

        # test4 preconditions
        self.threadStartedFlag = False
        self.threadTerminatedFlag = False
        self.threadRunningCounter = 0
        rc = RunningClass()
        rc.threadStarted.connect(lenghtyFuncStarted)
        rc.threadTerminated.connect(lenghtyFuncTerminated)
        rc.threadRunning.connect(lenghtyFuncRunning)
        # do test4: run function not in a thread
        with mock.patch('qgistester.utils.iface', self.IFACE_Mock):
            execute(rc.lenghtyFunc)
        self.assertFalse(self.threadStartedFlag)
        self.assertFalse(self.threadTerminatedFlag)
        self.assertEqual(self.threadRunningCounter, 0)
        self.assertFalse(self.lenghtyFuncRunningFailed,
                         msg=self.lenghtyFuncRunningFailedMessage)

###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testLayerFromName']
    suite = unittest.TestSuite(list(map(UtilsTests, tests)))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(UtilsTests, 'test'))
    return suite


def run_all():
    """run all tests using unittest => no nose or testplugin."""
    # demo_test = unittest.TestLoader().loadTestsFromTestCase(CatalogTests)
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    """run a subset of tests using unittest > no nose or testplugin."""
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())

if __name__ == "__main__":
    run_all()
