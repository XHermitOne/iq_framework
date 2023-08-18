#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog form for ref object element / code check selection.
All data is presented in tree view.
"""

import os.path
import wx

from ...util import log_func
from ...util import file_func

# from ...engine.wx import wxbitmap_func
# from ...engine.wx.dlg import wxdlg_func
from ...engine.wx import wxobj_func

from ..data_ref_object import wx_choicetreedlg

__version__ = (0, 0, 0, 1)


class iqRefObjCheckTreeDlg(wx_choicetreedlg.iqRefObjChoiceTreeDlg):
    """
    Dialog form for ref object element / code check selection.
    """
    def __init__(self, ref_obj=None, default_selected_code=None,
                 *args, **kwargs):
        """
        Constructor.

        :param ref_obj: Reference data object.
        :param default_selected_code: Selected default code.
        """
        wx_choicetreedlg.iqRefObjChoiceTreeDlg.__init__(self, ref_obj=ref_obj,
                                                        default_selected_code=default_selected_code,
                                                        *args, **kwargs)


def checkRefObjCodesDlg(parent=None, ref_obj=None, fields=None,
                        default_selected_code=None, search_fields=None,
                        clear_cache=False):
    """
    Function for calling the ref object code selection dialog box.
    Dialogs are cached in the cache dictionary CHOICE_DLG_CACHE.
    Dialogs are created only for the first time, then only their call occurs.

    :param parent: Parent window.
    :param ref_obj: Reference data object.
    :param fields: List of field names that
         must be displayed in the tree control.
         If no fields are specified, only
         <Code> and <Name>.
    :param default_selected_code: The selected code is the default.
         If None, then nothing is selected.
    :param search_fields: Fields to search for.
         If not specified, then the displayed fields are taken.
    :param clear_cache: Clear cache?
    :return: Selected ref object item cod or None if error.
    """
    if ref_obj is None:
        log_func.warning(u'Not define ref object for choice')
        return None

    code = None
    refobj_name = ref_obj.getName()
    try:
        if parent is None:
            app = wx.GetApp()
            main_win = app.GetTopWindow()
            parent = main_win

        global CHOICE_DLG_CACHE
        if clear_cache:
            CHOICE_DLG_CACHE = dict()

        dlg = None
        # Additional data filename
        ext_data_filename = os.path.join(file_func.getProjectProfilePath(),
                                         refobj_name + '_choice_dlg.dat')

        if refobj_name not in CHOICE_DLG_CACHE or wxobj_func.isWxDeadObject(CHOICE_DLG_CACHE[refobj_name]):
            dlg = iqRefObjCheckTreeDlg(ref_obj=ref_obj,
                                       default_selected_code=default_selected_code,
                                       parent=parent)
            # Download additional data
            ext_data = dlg.loadCustomData(save_filename=ext_data_filename)
            dlg.sort_column = ext_data.get('sort_column', None) if ext_data else None

            fields = list() if fields is None else fields
            search_fields = fields if search_fields is None else search_fields
            dlg.init(fields, search_fields)

            CHOICE_DLG_CACHE[refobj_name] = dlg
        elif refobj_name in CHOICE_DLG_CACHE and not wxobj_func.isWxDeadObject(CHOICE_DLG_CACHE[refobj_name]):
            dlg = CHOICE_DLG_CACHE[refobj_name]
            dlg.clearSearch()

        result = None
        if dlg:
            result = dlg.ShowModal()
            dlg.saveCustomData(save_filename=ext_data_filename,
                               save_data=dict(sort_column=dlg.sort_column))

        if result == wx.ID_OK:
            code = dlg.getSelectedCode()

        # dlg.Destroy()
    except:
        log_func.fatal(u'Error choice ref object <%s> code' % refobj_name)
    return code


def checkRefObjRecsDlg(parent=None, ref_obj=None, fields=None,
                       default_selected_code=None, search_fields=None,
                       clear_cache=False):
    """
    Function for calling the ref object record selection dialog box.
    Dialogs are cached in the cache dictionary CHOICE_DLG_CACHE.
    Dialogs are created only for the first time, then only their call occurs.

    :param parent: Parent window.
    :param ref_obj: Reference data object.
    :param fields: List of field names that
         must be displayed in the tree control.
         If no fields are specified, only
         <Code> and <Name>.
    :param default_selected_code: The selected code is the default.
         If None, then nothing is selected.
    :param search_fields: Fields to search for.
         If not specified, then the displayed fields are taken.
    :param clear_cache: Clear cache?
    :return: Selected ref object item record dictionary or None if error.
    """
    if ref_obj is None:
        log_func.warning(u'Not define ref object for choice')
        return None

    selected_rec = None
    refobj_name = ref_obj.getName()
    try:
        if parent is None:
            app = wx.GetApp()
            main_win = app.GetTopWindow()
            parent = main_win

        global CHOICE_DLG_CACHE
        if clear_cache:
            CHOICE_DLG_CACHE = dict()

        dlg = None
        # Additional data filename
        ext_data_filename = os.path.join(file_func.getProjectProfilePath(),
                                         refobj_name + '_choice_dlg.dat')

        if refobj_name not in CHOICE_DLG_CACHE or wxobj_func.isWxDeadObject(CHOICE_DLG_CACHE[refobj_name]):
            dlg = iqRefObjCheckTreeDlg(ref_obj=ref_obj,
                                       default_selected_code=default_selected_code,
                                       parent=parent)
            # Download additional data
            ext_data = dlg.loadCustomData(save_filename=ext_data_filename)
            dlg.sort_column = ext_data.get('sort_column', None) if ext_data else None

            fields = list() if fields is None else fields
            search_fields = fields if search_fields is None else search_fields
            dlg.init(fields, search_fields)

            CHOICE_DLG_CACHE[refobj_name] = dlg
        elif refobj_name in CHOICE_DLG_CACHE and not wxobj_func.isWxDeadObject(CHOICE_DLG_CACHE[refobj_name]):
            dlg = CHOICE_DLG_CACHE[refobj_name]
            dlg.clearSearch()

        result = None
        if dlg:
            result = dlg.ShowModal()
            dlg.saveCustomData(save_filename=ext_data_filename,
                               save_data=dict(sort_column=dlg.sort_column))

        if result == wx.ID_OK:
            code = dlg.getSelectedCode()
            selected_rec = ref_obj.getRecByCod(code)

        # dlg.Destroy()
    except:
        log_func.fatal(u'Error choice ref object <%s> record' % refobj_name)
    return selected_rec


def delCachedCheckRefObjDlg(ref_obj=None):
    """
    Remove the selection dialog box from the cache.

    :param ref_obj: Reference data object.
    :return: True - form removed from cache/False - form not removed from cache for some reason.
    """
    if ref_obj is None:
        log_func.warning(u'Not define ref object for remove choice dialog from cache')
        return False

    global CHOICE_DLG_CACHE

    sprav_name = ref_obj.getName()
    if sprav_name in CHOICE_DLG_CACHE:
        dlg = CHOICE_DLG_CACHE[sprav_name]
        dlg.Destroy()

        del CHOICE_DLG_CACHE[sprav_name]
        return True
    return False
