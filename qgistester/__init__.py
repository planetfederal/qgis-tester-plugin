# -*- coding: utf-8 -*-


def classFactory(iface):
    from qgistester.plugin import TesterPlugin
    return TesterPlugin(iface)

