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
from qgis.utils import active_plugins, plugins, iface
from qgis.core import *
import os
from qgistester.test import Test
from qgistester.utils import layerFromName


def _loadSpatialite():
    uri = QgsDataSourceURI()
    uri.setDatabase(os.path.join(os.path.dirname(__file__), "data", "elk.sqlite"))
    schema = ''
    table = 'elk'
    geom_column = 'the_geom'
    uri.setDataSource(schema, table, geom_column)
    layer = QgsVectorLayer(uri.uri(), "test", 'spatialite')
    assert layer.isValid()
    QgsMapLayerRegistry.instance().addMapLayer(layer)

def _openDBManager():
        plugins["db_manager"].run()

def _openLogMessagesDialog():
    widgets = [el for el in iface.mainWindow().children() if el.objectName() == "MessageLog"]
    widgets[0].setVisible(True)


def _openAboutDialog():
    iface.actionAbout().trigger()

def functionalTests():
    spatialiteTest = Test("Test Spatialite. QGIS-72")
    spatialiteTest.addStep("Load Spatialite layer", _loadSpatialite)
    spatialiteTest.addStep("Open DB Manager", _openDBManager)
    spatialiteTest.addStep("Check that 'elk' layer is available in DB manager")

    aboutTest = Test("Verify dependency versions and providers in About dialog. QGIS-53")
    aboutTest.addStep("Open About dialog", _openAboutDialog)
    if sys.platform == 'darwin':
        descriptionFile = os.path.join(os.path.dirname(__file__), "data", "about.mac")
    else:
        descriptionFile = os.path.join(os.path.dirname(__file__), "data", "about.windows")
    aboutTest.addStep(descriptionFile)

    logTest = Test("Verify in-app message log has no errors for default install. QGIS-54")
    logTest.addStep("Open log messages panel", _openLogMessagesDialog)
    logTest.addStep("Review 'General' tab output", isVerifyStep = True)
    logTest.addStep("Check there are no errors in 'Plugins' tab", isVerifyStep = True)
    logTest.addStep("Check there is no 'Python warning' tab", isVerifyStep = True)
    logTest.addStep("Check there is no 'Qt' tab", isVerifyStep = True)
    logTest.addStep("Check there is no other tab", isVerifyStep = True)

    return [spatialiteTest, aboutTest, logTest]


class PackageTests(unittest.TestCase):

    def testSaga(self):
        '''Test SAGA is installed. QGIS-89 (1)'''
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
        '''Test GRASS is installed QGIS-89 (2)'''
        folder = ProcessingConfig.getSetting(GrassUtils.GRASS_FOLDER)
        ProcessingConfig.removeSetting(GrassUtils.GRASS_FOLDER)
        msg = GrassUtils.checkGrassIsInstalled()
        self.assertIsNone(msg)
        ProcessingConfig.setSettingValue(GrassUtils.GRASS_FOLDER, folder)

    def testOtb(self):
        '''Test OTB is installed QGIS-89 (3)'''
        folder = findOtbPath()
        self.assertIsNotNone(folder)

    def testCorePluginsAreLoaded(self):
        '''Test core plugins are loaded. QGIS-55'''
        corePlugins = ['processing', 'GdalTools', 'MetaSearch', 'db_manager']
        for p in corePlugins:
            self.assertTrue(p in active_plugins)

    def testGDB(self):
        '''Test GDB format. QGIS-62'''
        layernames = ['T_1_DirtyAreas', 'T_1_PointErrors', 'landbnds', 'counties', 'neighcountry',
                      'cities', 'usabln', 'T_1_LineErrors', 'states', 'T_1_PolyErrors', 'us_lakes',
                      'us_rivers', 'intrstat']
        for layername in layernames:
            layer = QgsVectorLayer(os.path.join(os.path.dirname(__file__), "data",
                                    "ESRI_FileGDB-API_sample_Topo.gdb|layername=%s" % layername),
                                    "test", "ogr")
            self.assertTrue(layer.isValid())
            #QgsMapLayerRegistry.instance().addMapLayer(layer)




def unitTests():
    return unittest.makeSuite(PackageTests, 'test')
