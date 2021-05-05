#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PieCtrl component.
"""

import wx
import wx.lib.agw.piectrl

from ..wx_widget import component

from . import spc

from ...util import log_func
# from ...util import exec_func

# from ...engine.wx import wxbitmap_func

__version__ = (0, 0, 0, 1)


class iqWxPieCtrl(wx.lib.agw.piectrl.PieCtrl, component.iqWxWidget):
    """
    Wx PieCtrl component.
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

        wx.lib.agw.piectrl.PieCtrl.__init__(self, parent, wx.NewId(), *args, **kwargs)


COMPONENT = iqWxPieCtrl
