#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP cubes query tree control component.
"""

try:
    import wx
except ImportError:
    print(u'Import error wx')

from . import spc

from ...util import log_func
from ...util import lang_func
from ...util import exec_func
from ...util import file_func

from . import olap_query_tree_ctrl
# from ..wx_filterchoicectrl import filter_choicectrl

from ...role import component as role

from ..wx_widget import component

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

EDIT_PERMISSION = dict(name='edit_olap_query', description=_('Can edit OLAP tree queries'), type='DATA')
role.addPermision(**EDIT_PERMISSION)


class iqWxOLAPQueryTreeCtrl(olap_query_tree_ctrl.iqOLAPQueryTreeCtrlProto,
                            component.iqWxWidget):
    """
    OLAP cubes query tree control component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        component.iqWxWidget.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        olap_query_tree_ctrl.iqOLAPQueryTreeCtrlProto.__init__(self, parent=parent, id=wx.NewId(),
                                                               pos=self.getPosition(),
                                                               size=self.getSize(),
                                                               style=self.getStyle(),
                                                               name=self.getName())

        self._save_filename = self.getSaveFilename()
        log_func.debug(u'Set save filename <%s> in <%s : %s>' % (self._save_filename,
                                                                 self.getName(),
                                                                 self.getType()))

        # After defining the environment and the name of the filter storage file,
        # you can load the filters
        self.loadRequests()

    def _canEditOLAPQuery(self):
        return role.isPermision('edit_olap_query')

    def getSaveFilename(self):
        """
        The name of the storage file for the contents of the query tree.
        """
        save_filename = self.getAttribute('save_filename')
        if save_filename:
            save_filename = file_func.getNormalPath(save_filename)
        return save_filename

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

    def onChange(self, event):
        """
        Change item.
        """
        if self.isAttributeValue('on_change'):
            context = self.getContext()
            function_body = self.getAttribute('on_change')
            exec_func.execTxtFunction(function=function_body, context=context, show_debug=True)
        if event:
            event.Skip()


COMPONENT = iqWxOLAPQueryTreeCtrl
