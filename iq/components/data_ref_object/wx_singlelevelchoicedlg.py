#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog for code selection from one ref object level.
"""

import wx

from ...util import log_func
from ...util import global_func

from ...engine.wx.dlg import wxdlg_func
from ... import passport

__version__ = (0, 0, 0, 1)


def selectSingleLevelChoiceDlg(parent=None, ref_obj=None, n_level=0, parent_code=None):
    """
    Open dialog for code selection from one ref object level.
    
    :param parent: Parent window.
        If not defined, then the main application window is taken.
    :param ref_obj: Ref object.
        It can be specified by the object passport or directly by the object.
    :param n_level: The index of the level from which the selection is made.
    :param parent_code: Parent code for detailing level values.
        If not defined, then it is considered that this is the very first level.
    :return: Selected code or None if <Cancel> is pressed.
    """
    if passport.isPassport(ref_obj):
        # Справочник задается паспортом. Необходимо создать объект
        ref_obj = global_func.getKernel().getObject(ref_obj)

    if ref_obj is None:
        log_func.warning(u'Undefined ref object to select')
        return None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    selected_code = None
    try:
        sprav_storage = ref_obj.getStorage()
        level_table = sprav_storage.getLevelTable(parent_code) if sprav_storage else list()
        level = ref_obj.getLevelByIdx(n_level)
        records = [sprav_storage.record_tuple2record_dict(rec) for rec in level_table]
        choices = [rec.get('name', u'-')for rec in records]

        select_idx = wxdlg_func.getSingleChoiceIdxDlg(parent, ref_obj.getDescription(), level.getDescription(), choices)
        if select_idx >= 0:
            selected_code = records[select_idx].get(sprav_storage.getCodeFieldName(), None)
        return selected_code
    except:
        log_func.fatal(u'Error choosing code from one level of the ref object.')
    return None
