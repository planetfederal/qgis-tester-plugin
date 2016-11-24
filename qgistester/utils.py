from builtins import str
# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

import os

from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtWidgets import QApplication
from qgis.utils import iface
from qgis.core import (QgsMapLayerRegistry,
                       QgsVectorLayer,
                       QgsRasterLayer,
                      )


def layerFromName(name):
    '''
    Returns the layer from the current project with the passed name
    Returns None if no layer with that name is found
    If several layers with that name exist, only the first one is returned
    '''
    layers = list(QgsMapLayerRegistry.instance().mapLayers().values())
    for layer in layers:
        if layer.name() == name:
            return layer


def loadLayer(filename, name = None):
    '''
    Tries to load a layer from the given file

    :param filename: the path to the file to load.

    :param name: the name to use for adding the layer to the current project.
    If not passed or None, it will use the filename basename
    '''
    name = name or os.path.splitext(os.path.basename(filename))[0]
    qgslayer = QgsVectorLayer(filename, name, 'ogr')
    if not qgslayer.isValid():
        qgslayer = QgsRasterLayer(filename, name)
        if not qgslayer.isValid():
            raise RuntimeError('Could not load layer: ' + str(filename))

    return qgslayer


def loadLayerNoCrsDialog(filename, name=None):
    '''
    Tries to load a layer from the given file
    Same as the loadLayer method, but it does not ask for CRS, regardless of current
    configuration in QGIS settings
    '''
    settings = QSettings()
    prjSetting = settings.value('/Projections/defaultBehaviour')
    settings.setValue('/Projections/defaultBehaviour', '')
    try:
        layer = loadLayer(filename, name)
    finally:
        settings.setValue('/Projections/defaultBehaviour', prjSetting)
    return layer


def execute(func):
    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    try:
        return func()
    finally:
        QApplication.restoreOverrideCursor()
