#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UniReader controller component.
"""

from ... import object
# from ... import passport

from . import spc
from . import uni_reader_controller

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqUniReaderController(uni_reader_controller.iqUniReaderControllerProto, object.iqObject):
    """
    UniReader controller component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        uni_reader_controller.iqUniReaderControllerProto.__init__(self,
                                                                  host=self.getHost(),
                                                                  port=self.getPort(),
                                                                  server=self.getServer(),
                                                                  node=self.getNode())

    def getHost(self):
        """
        Get server host.
        """
        return self.getAttribute('host')

    def getPort(self):
        """
        Get server port.
        """
        return self.getAttribute('port')

    def getServer(self):
        """
        Get server name.
        """
        return self.getAttribute('server')

    def getNode(self):
        """
        Get node name.
        """
        return self.getAttribute('node')

    def getTags(self):
        """
        Get tags dictionary.
        """
        if self.isAttributeValue('tags'):
            tags_str = self.getAttribute('tags')
            try:
                return eval(tags_str)
            except:
                log_func.fatal(u'Error attribute <tags> in <%s>' % self.getName())
        return None

    def test(self):
        """
        Test function.
        """
        from . import test_uni_reader_ctrl_dlg
        return test_uni_reader_ctrl_dlg.viewTestUniReaderCtrlDlg(controller=self)

    def printConnectionParam(self):
        """
        Display communication parameters UniReader Gateway.
        """
        log_func.info(u'UniReader <%s>. Communication parameters:' % self.getName())
        log_func.info(u'\tHost <%s>' % self.getHost())
        log_func.info(u'\tPort <%s>' % self.getPort())
        log_func.info(u'\tNode <%s>' % self.getNode())
        log_func.info(u'\tServer <%s>' % self.getServer())


COMPONENT = iqUniReaderController
