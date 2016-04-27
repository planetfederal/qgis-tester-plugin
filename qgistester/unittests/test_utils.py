# -*- coding: utf-8 -*-
"""Test utils.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import os
import utilities
import tempfile
import mock
import time
import traceback
from qgistesting import start_app
from qgistesting.mocked import get_iface
from qgis.core import (QgsVectorLayer,
                       QgsMapLayerRegistry,
                       QgsVectorFileWriter)
from qgistester.utils import (layerFromName,
                              loadLayer,
                              loadLayerNoCrsDialog,
                              ExecutorThread,
                              execute)
import qgistester.utils as utils

from PyQt import QtCore, QtGui

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
        QgsMapLayerRegistry.instance().addMapLayer(self.testFile1)
        QgsMapLayerRegistry.instance().addMapLayer(self.testFile2)
        QgsMapLayerRegistry.instance().addMapLayer(self.testFile3)
        # do test 2: look for the 'testFile2' that exists
        layer = layerFromName('testFile2')
        self.assertEqual(self.testFile2, layer)

        # do test 3: look for the 'unexist' that does not exists
        layer = layerFromName('unexist')
        self.assertIsNone(layer)

    def testLoadLayer(self):
        """check load layer from file (raster or vector) returning layer
        instance."""
        # preconditions
        tf = tempfile.NamedTemporaryFile()
        tempFileName = tf.name + '.shp'
        tf.close()
        QgsVectorFileWriter.writeAsVectorFormat(self.testFile1, tempFileName,
                                                'utf-8', None)
        basename = os.path.basename(tempFileName)
        name = os.path.splitext(basename)[0]
        # test 1: load vector layer
        layer = loadLayer(tempFileName)
        self.assertEqual(layer.name(), name)
        # test 2: load a vector layre giving a layer name
        wouldHaveName = "pippo"
        layer = loadLayer(tempFileName, wouldHaveName)
        self.assertEqual(layer.name(), wouldHaveName)
        # test 3: load raster layer (the plugin png)
        rasterFileName = os.path.abspath(os.path.join(
                                         os.path.dirname(__file__),
                                         os.path.pardir,
                                         'plugin.png'))
        layer = loadLayer(rasterFileName)
        self.assertEqual(layer.name(), 'plugin')
        # test 4: load an unexistent layer
        rasterFileName = rasterFileName + '_unexistent'
        try:
            layer = loadLayer(rasterFileName)
        except RuntimeError:
            # test success
            pass
        except:
            self.assertTrue(False, msg='Received unexpected exception type')
        else:
            self.assertTrue(False, msg='Expected RuntimeError but not rised')

    def testLoadLayerNoCrsDialog(self):
        """load a layer file without opening CRS dialog."""
        self.assertTrue(False)

    def testExecutorThread(self):
        """Test wrapper to QThread to manage some vars and events."""
        self.assertTrue(False)

    def testExecute(self):
        """Test execution of long time task managing dialog to show progress.

        It will be created a lenghty task and will be tested if it is run
        thanks to the event it emits"""
        # precondition
        self.lenghtyFuncRunningFailed = False
        self.lenghtyFuncRunningFailedMessage = ''
        self.threadStartedFlag = False
        self.threadTerminatedFlag = False
        self.threadRunningCounter = 0
        self.message1 = 'progess bar message'
        self.message2 = 'new progess bar message'

        def lenghtyFuncStarted():
            self.threadStartedFlag = True

        def lenghtyFuncTerminated():
            self.threadTerminatedFlag = True

        def lenghtyFuncRunning(step):
            self.threadRunningCounter = step

        def lenghtyFuncRunningTest1():
            '''function to do tests when thread is in execution'''
            print "test1 during thread execution"
            try:
                # check the WaitCursor is set
                cursor = QtGui.QApplication.overrideCursor()
                self.assertEqual(cursor.shape(), QtCore.Qt.WaitCursor)
                # check if PrograssBar is available
                mw = self.IFACE_Mock.mainWindow()
                pb = mw.findChildren(QtGui.QProgressDialog)
                self.assertEqual(len(pb), 1)
                self.assertEqual(pb[0].labelText(), self.message1)
            except AssertionError:
                self.lenghtyFuncRunningFailed = True
                self.lenghtyFuncRunningFailedMessage = traceback.format_exc()

        def lenghtyFuncRunningTest2():
            '''function to do tests when thread is in execution'''
            print "test2 during thread execution"
            try:
                # check the WaitCursor is set
                cursor = QtGui.QApplication.overrideCursor()
                self.assertEqual(cursor.shape(), QtCore.Qt.WaitCursor)
                # check if PrograssBar is available
                mw = self.IFACE_Mock.mainWindow()
                pb = mw.findChildren(QtGui.QProgressDialog)
                self.assertEqual(len(pb), 2)  # remained first progress bar not removed with deleteLater()
                self.assertEqual(pb[1].labelText(), self.message2)
            except AssertionError:
                self.lenghtyFuncRunningFailed = True
                self.lenghtyFuncRunningFailedMessage = traceback.format_exc()

        def lenghtyFuncRunningTest3():
            '''function to do tests when thread is in execution'''
            print "test3 during thread execution"
            try:
                # check the WaitCursor is set
                cursor = QtGui.QApplication.overrideCursor()
                self.assertEqual(cursor.shape(), QtCore.Qt.WaitCursor)
                # check if PrograssBar is available
                mw = self.IFACE_Mock.mainWindow()
                pb = mw.findChildren(QtGui.QProgressDialog)
                self.assertEqual(len(pb), 1)  # remained first progress bar not removed with deleteLater()
            except AssertionError:
                self.lenghtyFuncRunningFailed = True
                self.lenghtyFuncRunningFailedMessage = traceback.format_exc()

        class RunningClass(QtCore.QObject):

            threadStarted = QtCore.pyqtSignal()
            threadTerminated = QtCore.pyqtSignal()
            threadRunning = QtCore.pyqtSignal(int)

            def lenghtyFunc(self):
                self.threadStarted.emit()
                for i in range(1,6):
                    time.sleep(0.5)
                    self.threadRunning.emit(i)
                self.threadTerminated.emit()

        # tes1 preconditions
        self.threadStartedFlag = False
        self.threadTerminatedFlag = False
        self.threadRunningCounter = 0
        rc = RunningClass()
        rc.threadStarted.connect(lenghtyFuncStarted)
        rc.threadTerminated.connect(lenghtyFuncTerminated)
        rc.threadRunning.connect(lenghtyFuncRunning)
        rc.threadRunning.connect(lenghtyFuncRunningTest1)
        # do test1: dialog is not present => create it
        self.assertIsNone(utils._dialog)
        with mock.patch('qgistester.utils.iface', self.IFACE_Mock):
            execute(rc.lenghtyFunc, message=self.message1)
        self.assertTrue(self.threadStartedFlag)
        self.assertTrue(self.threadTerminatedFlag)
        self.assertEqual(self.threadRunningCounter, 5)
        self.assertIsNone(utils._dialog)
        self.assertFalse(self.lenghtyFuncRunningFailed,
                         msg=self.lenghtyFuncRunningFailedMessage)

        # tes2 preconditions
        self.threadStartedFlag = False
        self.threadTerminatedFlag = False
        self.threadRunningCounter = 0
        rc = RunningClass()
        rc.threadStarted.connect(lenghtyFuncStarted)
        rc.threadTerminated.connect(lenghtyFuncTerminated)
        rc.threadRunning.connect(lenghtyFuncRunning)
        rc.threadRunning.connect(lenghtyFuncRunningTest2)
        # do test2: dialog is present => avoid to create it and overload the
        # message
        utils._dialog = QtGui.QProgressDialog("old message", "Running", 0, 0,
                                              self.IFACE_Mock.mainWindow())
        utils._dialog.show()
        self.assertIsNotNone(utils._dialog)
        with mock.patch('qgistester.utils.iface', self.IFACE_Mock):
            execute(rc.lenghtyFunc, message=self.message2)
        self.assertTrue(self.threadStartedFlag)
        self.assertTrue(self.threadTerminatedFlag)
        self.assertEqual(self.threadRunningCounter, 5)
        self.assertIsNotNone(utils._dialog)
        self.assertFalse(self.lenghtyFuncRunningFailed,
                         msg=self.lenghtyFuncRunningFailedMessage)

        # tes3 preconditions
        self.threadStartedFlag = False
        self.threadTerminatedFlag = False
        self.threadRunningCounter = 0
        rc = RunningClass()
        rc.threadStarted.connect(lenghtyFuncStarted)
        rc.threadTerminated.connect(lenghtyFuncTerminated)
        rc.threadRunning.connect(lenghtyFuncRunning)
        rc.threadRunning.connect(lenghtyFuncRunningTest3)
        if utils._dialog:
            utils._dialog.deleteLater()
            utils._dialog = None
        # do test2: dialog is present => avoid to create it and overload the
        # message
        self.assertIsNone(utils._dialog)
        with mock.patch('qgistester.utils.iface', self.IFACE_Mock):
            execute(rc.lenghtyFunc)
        self.assertTrue(self.threadStartedFlag)
        self.assertTrue(self.threadTerminatedFlag)
        self.assertEqual(self.threadRunningCounter, 5)
        self.assertIsNone(utils._dialog)
        self.assertFalse(self.lenghtyFuncRunningFailed,
                         msg=self.lenghtyFuncRunningFailedMessage)


###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testExecute']
    suite = unittest.TestSuite(map(UtilsTests, tests))
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
    run_subset()
