#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP server query browser component.
"""

from . import spc

from .. import wx_panel

from ...util import log_func

from . import olap_query_browser

__version__ = (0, 0, 0, 1)


class iqWxOLAPQueryBrowser(olap_query_browser.iqOLAPQueryBrowserProto, wx_panel.COMPONENT):
    """
    OLAP server query browser component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        wx_panel.COMPONENT.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        olap_query_browser.iqOLAPQueryBrowserProto.__init__(self, parent=parent, *args, **kwargs)

    def getOLAPServerPsp(self):
        """
        OLAP server object passport.
        """
        psp = self.getAttribute('olap_server')
        log_func.debug(u'%s. OLAP server passport: %s' % (self.__class__.__name__, psp))
        return psp

    def getOLAPServer(self):
        """
        Get OLAP server object.
        """
        if self._OLAP_server is None:
            olap_srv_psp = self.getOLAPServerPsp()
            kernel = self.getKernel()
            self._OLAP_server = kernel.createByPsp(psp=olap_srv_psp)
        return self._OLAP_server


COMPONENT = iqWxOLAPQueryBrowser
