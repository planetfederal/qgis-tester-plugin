'''
Tests to ensure that a QGIS installation contains Processing dependencies
and they are correctly configured by default
'''
import unittest
import sys
from processing.algs.saga.SagaUtils import *
from processing.core.ProcessingConfig import ProcessingConfig
from processing.algs.grass.GrassUtils import GrassUtils
from processing.algs.otb.OTBUtils import *
from qgis.utils import active_plugins

class PackageTests(unittest.TestCase):

    def testSaga(self):
        folder = ProcessingConfig.getSetting(SAGA_FOLDER)
        hasSetting = True
        try:
            ProcessingConfig.removeSetting(SAGA_FOLDER)
        except:
            hasSetting = False
        self.assertTrue(getSagaInstalledVersion(True) in ["2.1.2", "2.1.3", "2.1.4", "2.2.0"])
        if hasSetting:
            ProcessingConfig.setSettingValue(SAGA_FOLDER, folder)

    def testGrass(self):
        folder = ProcessingConfig.getSetting(GrassUtils.GRASS_FOLDER)
        ProcessingConfig.removeSetting(GrassUtils.GRASS_FOLDER)
        msg = GrassUtils.checkGrassIsInstalled()
        self.assertIsNone(msg)
        ProcessingConfig.setSettingValue(GrassUtils.GRASS_FOLDER, folder)

    def testOtb(self):
        folder = findOtbPath()
        self.assertIsNotNone(folder)

    def testCorePluginsAreLoaded(self):
        corePlugins = ['processing', 'GdalTools', 'MetaSearch', 'db_manager']
        for p in corePlugins:
            self.assertTrue(p in active_plugins)

def unitTests():
    return unittest.makeSuite(PackageTests, 'test')
    