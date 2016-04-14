# -*- coding: utf-8 -*-
"""Common functionality used by regression tests."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import sys
import logging
import sip
for api in ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl",
            "QVariant"]:
    sip.setapi(api, 2)
# add current module to pythonpath
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir,
                    os.path.pardir)
sys.path.insert(1, path)

LOGGER = logging.getLogger('QGIS')
QGIS_APP = None  # Static variable used to hold hand to running QGIS app
CANVAS = None
PARENT = None
IFACE = None


def setUpEnv():
    """setup test running env."""
    pass


def cleanUpEnv():
    """cleanup test running env."""
    pass
