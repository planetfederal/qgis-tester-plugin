import qgis.utils
from qgistester.test import Test
from geoserverexplorer.geoserver.retry import RetryCatalog
from geoserverexplorer.test.catalogtests import suite
from geoserverexplorer.gui.gsexploreritems import *


def suite():
    return suite()

#Tests assume a standard Geoserver at localhost:8080 and default admin/geoserver credentials


def _getCatalog():
    return RetryCatalog("http://localhost:8080/geoserver/rest", "admin", "geoserver")

def _setUpCatalogAndExplorer(name):
    explorer = qgis.utils.plugins["geoserverexplorer"].explorer
    explorer.show()
    gsItem = explorer.explorerTree.gsItem
    cat = _getCatalog()
    cat.create_workspace(name + "_workspace", "http://test.com")
    geoserverItem = GsCatalogItem(cat, name)
    gsItem.addChild(geoserverItem)
    geoserverItem.populate()
    gsItem.setExpanded(True)

def _checkNewLayer():
    cat = _getCatalog()
    stores = cat.get_stores("drag_test_catalog_workspace")
    assert len(stores) != 0

def _clean():
    pass

dragdropTest = Test("Geoserver", "Drag browser element into workspace")
dragdropTest.addStep("Setting up catalog and explorer", lambda: _setUpCatalogAndExplorer("drag_test_catalog"))
dragdropTest.addStep("Drag layer from browser into testing workspace")
dragdropTest.addStep("Checking new layer", _checkNewLayer)
dragdropTest.addStep("Cleaning", _clean)

def tests():
    return [dragdropTest]

