#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Panel manager.
"""

import datetime
import wx
import wx.adv
import wx.gizmos
import wx.dataview
import wx.grid

from ...util import log_func
from ...util import dt_func

from . import wxdatetime_func
# from . import listctrl_manager
# from . import treectrl_manager
# from . import toolbar_manager
from . import validate_manager

from . import key_combins
from . import wxobj_func
from . import wxdatetime_func

__version__ = (0, 0, 0, 1)

SKIP_ACCORD_NAMES = ('Handle', 'EventHandler', 'Parent', 'GrandParent')


class iqPanelManager(validate_manager.iqValidateManager):
    """
    Panel manager.
    """
    def setPanelCtrlValue(self, ctrl, value):
        """
        Set control value.

        :param ctrl: Control object.
        :param value: Value.
        :return: True/False.
        """
        result = False
        if hasattr(ctrl, 'setValue'):
            ctrl.setValue(value)
            result = True
        elif issubclass(ctrl.__class__, wx.CheckBox):
            ctrl.SetValue(value)
            result = True
        elif issubclass(ctrl.__class__, wx.StaticText):
            value = value if isinstance(value, str) else str(value)
            ctrl.SetLabel(value)
            result = True
        elif issubclass(ctrl.__class__, wx.TextCtrl):
            value = value if isinstance(value, str) else str(value)
            ctrl.SetValue(value)
            result = True
        elif issubclass(ctrl.__class__, wx.adv.DatePickerCtrl):
            try:
                wx_dt = wxdatetime_func.datetime2wxDateTime(value)
                ctrl.SetValue(wx_dt)
                result = True
            except:
                log_func.fatal(u'Error set value <%s : %s> in DatePickerCtrl' % (str(value),
                                                                                 value.__class__.__name__))
        elif issubclass(ctrl.__class__, wx.DirPickerCtrl):
            ctrl.SetPath(value)
            result = True
        elif issubclass(ctrl.__class__, wx.SpinCtrl):
            ctrl.SetValue(int(value))
            result = True
        elif issubclass(ctrl.__class__, wx.dataview.DataViewListCtrl):
            self._set_wxDataViewListCtrl_data(ctrl, value)
            result = True
        else:
            log_func.warning(u'Panel manager. Control <%s> not support' % ctrl.__class__.__name__)
        return result

    def getPanelCtrlValues(self, panel, data_dict=None, *ctrl_names):
        """
        Get control values.

        :param data_dict: Result dictionary.
            If None then create new dictionary.
        :param ctrl_names: Control object names.
            If no control names are defined,
            then controls are processed
            indicated in correspondence (accord).
        """
        result = dict() if data_dict is None else data_dict
        if not ctrl_names:
            ctrl_names = self.__accord.values()

        for ctrlname in dir(panel):
            if ctrl_names and ctrlname not in ctrl_names:
                continue
            if ctrlname in SKIP_ACCORD_NAMES:
                continue

            ctrl = getattr(panel, ctrlname)
            if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
                if issubclass(ctrl.__class__, wx.Panel):
                    data = self.getPanelCtrlValues(ctrl, data_dict, *ctrl_names)
                    result.update(data)
                else:
                    value = self.getPanelCtrlValue(ctrl)
                    result[ctrlname] = value
        return result

    def setPanelCtrlValues(self, panel, data_dict=None, *ctrl_names):
        """
        Set values in controls.

        :param panel: Panel object.
        :param data_dict: Data dictionary.
        :param ctrl_names: Control object names.
            If no control names are defined,
            then controls are processed
            indicated in correspondence (accord).
        """
        if data_dict is None:
            log_func.error(u'Not defined fill dictionary for panel controls')
            return

        for name, value in data_dict.items():
            for ctrlname in dir(panel):
                if ctrl_names and ctrlname not in ctrl_names:
                    continue

                if ctrlname == name:
                    ctrl = getattr(panel, ctrlname)
                    self.setPanelCtrlValue(ctrl, value)
                    break

    def _getPanelCtrlData(self):
        """
        Get panel control values.

        :return: Panel control values dictionary.
        """
        ctrl_data = dict()

        ctrl_data['self'] = dict(pos=tuple(self.GetPosition()),
                                 size=tuple(self.GetSize()))

        for ctrlname in dir(self):
            ctrl = getattr(self, ctrlname)
            if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
                if issubclass(ctrl.__class__, wx.SplitterWindow):
                    ctrl_data[ctrlname] = dict(sash_pos=ctrl.GetSashPosition())
                else:
                    log_func.warning(u'Panel manager. Unsupported control type <%s>' % ctrl.__class__.__name__)

        return ctrl_data

    def _setPanelCtrlData(self, ctrl_data):
        """
        Set panel control values.

        :param ctrl_data: Panel control values dictionary.
        :return: True/False.
        """
        dlg_data = ctrl_data.get('self', dict())
        size = dlg_data.get('size', (-1, -1))
        self.SetSize(*size)
        pos = dlg_data.get('pos', (-1, -1))
        self.SetPosition(*pos)

        for ctrlname, ctrl_value in [item for item in ctrl_data.items() if item[0] != 'self']:
            ctrl = getattr(self, ctrlname)
            if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
                if issubclass(ctrl.__class__, wx.SplitterWindow):
                    ctrl.SetSashPosition(ctrl_value.get('sash_pos', -1))
                else:
                    log_func.warning(u'Panel manager. Unsupported control type <%s>' % ctrl.__class__.__name__)
        return True

    def setPanelAccord(self, **accord):
        """
        Set matching dictionary control values and names.

        :param accord: Matching dictionary control values and names.
            Format:
            {'name': 'control name', ...}
        """
        self.__accord = accord

    def addPanelAccord(self, **accord):
        """
        Add matching dictionary control values and names

        :param accord: Matching dictionary control values and names.
            Format:
            {'name': 'control name', ...}
        """
        if accord:
            self.__accord.update(accord)

    def getPanelAccord(self):
        """
        Get matching dictionary control values and names

        :return: Matching dictionary control values and names.
            Format:
            {'name': 'control name', ...}
        """
        return self.__accord

    def getPanelAccordCtrlData(self):
        """
        Get consistent data.

        :return: Matching dictionary control values and names.
            Format:
            {'name': 'control value', ...}
        """
        ctrl_data = self.getPanelCtrlData(*self.__accord.values())
        result_data = dict([(name, ctrl_data[self.__accord[name]]) for name in self.__accord.keys()])
        return result_data

    def setPanelAccordCtrlData(self, **data):
        """
        Set consistent data.

        :return: Matching dictionary control values and names.
            Format:
            {'name': 'control value', ...}
        """
        ctrl_data = dict([(self.__accord[name], data[name]) for name in data.keys() if name in self.__accord])
        self.setPanelCtrlData(ctrl_data, *ctrl_data.keys())

    def findPanelAccord(self, panel):
        """
        Find panel controls and set as matching dictionary.

        :param panel: Panel object.
        :return: Matching dictionary.
        """
        try:
            return self._findPanelAccord(panel)
        except:
            log_func.fatal(u'Error find panel controls and set as matching dictionary')
        return dict()

    def _findPanelAccord(self, panel):
        """
        Find panel controls and set as matching dictionary.

        :param panel: Panel object.
        :return: Matching dictionary.
        """
        accord = dict()
        if not issubclass(panel.__class__, wx.Window):
            log_func.warning(u'Object <%s> not an heir wx.Windows' % panel.__class__.__name__)
            return accord

        panel_ctrl_names = dir(panel)
        for ctrl_name in panel_ctrl_names:
            if ctrl_name in SKIP_ACCORD_NAMES:
                continue
            ctrl = getattr(panel, ctrl_name)
            if isinstance(ctrl, wx.TextCtrl):
                accord[ctrl_name] = ctrl_name
            elif isinstance(ctrl, wx.SpinCtrl):
                accord[ctrl_name] = ctrl_name
            elif isinstance(ctrl, wx.CheckBox):
                accord[ctrl_name] = ctrl_name
            elif isinstance(ctrl, wx.adv.DatePickerCtrl):
                accord[ctrl_name] = ctrl_name
            elif isinstance(ctrl, wx.DirPickerCtrl):
                accord[ctrl_name] = ctrl_name
            elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
                accord[ctrl_name] = ctrl_name

        return accord

    def setPanelWindowAcceleratorTable(self, win=None, **key_combine_connections):
        """
        Set the accelerator table for the window.

        :param win: Window object. If None then get self.
        :param key_combine_connections: Dictionary of key combinations with
            processing / control controls.
            Format:
                {
                    'key combination': Tool/Menuitem ID,
                    ...
                }
            For example:
                {
                    'CTRL_F1': self.tool1.GetId(), ...
                }
        :return: True/False
        """
        if win is None:
            win = self

        used_key_combins = [(key_combine_name,
                             key_combins.getKeyCombine(key_combine_name)) for key_combine_name in key_combine_connections.keys()]
        used_key_connections = [(combine_key['mode'],
                                 combine_key['key'],
                                 key_combine_connections[name]) for name, combine_key in used_key_combins]
        win._accelerator_table = wx.AcceleratorTable(used_key_connections)
        win.SetAcceleratorTable(win._accelerator_table)

    def getPanelWindowAcceleratorTable(self, win=None):
        """
        Get window accelerator table.

        :param win: Window object. If None then get self.
        :return: Accelerator table object or None if not exists.
        """
        if win is None:
            win = self

        if hasattr(win, '_accelerator_table'):
            return win._accelerator_table
        else:
            log_func.warning(u'In object <%s> accelerator table not exists' % win.__class__.__name__)
        return None

    def setPanelNotebookPageImage(self, notebook_ctrl, n_page=-1, img=None):
        """
        Set wx.Notebook page image.

        :param notebook_ctrl: wx.Notebook object.
        :param n_page: Page index. If < 0 then get selected page.
        :param img: Image. If None then image clear.
        :return: True/False.
        """
        if notebook_ctrl is None:
            log_func.error(u'Not define wx.Notebook object for set page image')
            return False
        elif not issubclass(notebook_ctrl.__class__, wx.Notebook):
            log_func.error(u'wx.Notebook object type error')
            return False

        if n_page < 0:
            n_page = notebook_ctrl.GetSelection()
        if n_page == wx.NOT_FOUND:
            log_func.error(u'Not define notebook page')
            return False

        try:
            if img is None:
                notebook_ctrl.SetPageImage(n_page, wx.NOT_FOUND)
            else:
                notebook_img_list = notebook_ctrl.GetImageList()
                if notebook_img_list:
                    img_idx = notebook_img_list.Add(img)
                else:
                    img_size = img.GetSize()
                    notebook_img_list = wx.ImageList(*img_size)
                    img_idx = notebook_img_list.Add(img)
                    notebook_ctrl.AssignImageList(notebook_img_list)
                notebook_ctrl.SetPageImage(n_page, img_idx)
            return True
        except:
            log_func.fatal(u'Error set notebook page image')
        return False

    def clearPanelData(self, panel):
        """
        Clear control values.

        :param panel: Panel object.
        """
        try:
            return self._clearPanelData(panel)
        except:
            log_func.fatal(u'Error clear control values')

    def _clearPanelData(self, panel):
        """
        Clear control values.

        :param panel: Panel object.
        """
        if not issubclass(panel.__class__, wx.Panel):
            return

        children = panel.GetChildren()

        for ctrl in children:
            if issubclass(ctrl.__class__, wx.Window) and ctrl.IsEnabled():
                if issubclass(ctrl.__class__, wx.Panel) and not wxobj_func.isSameWxObject(ctrl, panel):
                    self._clearPanelData(ctrl)
                else:
                    try:
                        self.clearPanelCtrlValue(ctrl)
                    except:
                        log_func.fatal(u'Error clear control value <%s>' % ctrl.__class__.__name__)

    def clearPanelCtrlValue(self, ctrl):
        """
        Clear control value in panel.

        :param ctrl: Control object.
        :return: True/False.
        """
        result = False
        if hasattr(ctrl, 'setValue'):
            ctrl.setValue(None)
            result = True
        elif issubclass(ctrl.__class__, wx.CheckBox):
            ctrl.SetValue(False)
            result = True
        elif issubclass(ctrl.__class__, wx.TextCtrl):
            ctrl.SetValue('')
            result = True
        elif issubclass(ctrl.__class__, wx.adv.DatePickerCtrl):
            if ctrl.GetExtraStyle() & wx.adv.DP_ALLOWNONE:
                ctrl.SetValue(None)
            else:
                wx_date = wxdatetime_func.date2wxDateTime(datetime.date.today())
                ctrl.SetValue(wx_date)
            result = True
        elif issubclass(ctrl.__class__, wx.DirPickerCtrl):
            ctrl.SetPath('')
            result = True
        elif issubclass(ctrl.__class__, wx.SpinCtrl):
            ctrl.SetValue(0)
            result = True
        elif issubclass(ctrl.__class__, wx.dataview.DataViewListCtrl):
            self._set_wxDataViewListCtrl_data(ctrl, ())
            result = True
        elif issubclass(ctrl.__class__, wx.ListCtrl):
            ctrl.DeleteAllItems()
            result = True
        else:
            log_func.error(u'Panel manager. Unsupported control type <%s> for clear value' % ctrl.__class__.__name__)
        return result

    def collapsePanelSplitter(self, splitter, toolbar=None, collapse_tool=None, expand_tool=None,
                              resize_panel=0, redraw=True):
        """
        Collapse splitter panel.

        :param splitter: wx.SplitterWindow object.
        :param toolbar: ToolBar object.
        :param collapse_tool: Tool button fot collapse.
        :param expand_tool: Tool button fot expand.
        :param resize_panel: Resizable panel index.
            0 - collapses / expands the first panel
            1 - collapses / expands the second panel
        :param redraw: Redraw?
        :return: True/False.
        """
        if not isinstance(splitter, wx.SplitterWindow):
            log_func.error(u'Error splitter object type <%s>' % str(splitter))
            return False

        setattr(self, '_last_sash_position_%s' % splitter.GetId(),
                splitter.GetSashPosition())

        if resize_panel == 0:
            # Can not use 0 as position
            #                        v
            splitter.SetSashPosition(1, redraw=redraw)
        elif resize_panel == 1:
            split_mode = splitter.GetSplitMode()
            sash_pos = splitter.GetSize().GetHeight() if split_mode == wx.SPLIT_HORIZONTAL else splitter.GetSize().GetWidth()
            splitter.SetSashPosition(sash_pos - 1, redraw=redraw)
        else:
            log_func.error(u'Not valid resized splitter panel index')
            return False

        # splitter.UpdateSize()

        if toolbar:
            if collapse_tool:
                toolbar.EnableTool(collapse_tool.GetId(), False)
            if expand_tool:
                toolbar.EnableTool(expand_tool.GetId(), True)
        return True

    def expandPanelSplitter(self, splitter, toolbar=None, collapse_tool=None, expand_tool=None,
                            resize_panel=0, redraw=True):
        """
        Expand splitter panel.

        :param splitter: wx.SplitterWindow object.
        :param toolbar: ToolBar object.
        :param collapse_tool: Tool button fot collapse.
        :param expand_tool: Tool button fot expand.
        :param resize_panel: Resizable panel index.
            0 - collapses / expands the first panel
            1 - collapses / expands the second panel
        :param redraw: Redraw?
        :return: True/False.
        """
        if not isinstance(splitter, wx.SplitterWindow):
            log_func.error(u'Error splitter object type <%s>' % str(splitter))
            return False

        last_sash_position_name = '_last_sash_position_%s' % splitter.GetId()
        if not hasattr(self, last_sash_position_name):
            log_func.warning(u'Not defined last splitter sash position')
            return False

        last_sash_position = getattr(self, last_sash_position_name)

        if resize_panel == 0:
            if last_sash_position != splitter.GetSashPosition():
                splitter.SetSashPosition(last_sash_position, redraw=redraw)
        elif resize_panel == 1:
            if last_sash_position != splitter.GetSashPosition():
                splitter.SetSashPosition(last_sash_position, redraw=redraw)
        else:
            log_func.error(u'Not valid resized splitter panel index')
            return False

        # splitter.UpdateSize()

        if toolbar:
            if collapse_tool:
                toolbar.EnableTool(collapse_tool.GetId(), True)
            if expand_tool:
                toolbar.EnableTool(expand_tool.GetId(), False)
        return True

    def getPanelCtrlData(self, data_dict=None, *ctrl_names):
        """
        Get control values.

        :param data_dict: Data dictionary.
            If None then create new dictionary.
        :param ctrl_names: Take only controls with names...
            If no control names are defined,
            then controls are processed
            indicated in the matches (accord).
        """
        return self.getPanelCtrlValues(self, data_dict, *ctrl_names)

    def setPanelCtrlData(self, data_dict=None, *ctrl_names):
        """
        Set control values.

        :param data_dict: Data dictionary.
        :param ctrl_names: Take only controls with names...
            If no control names are defined,
            then controls are processed
            indicated in the matches (accord).
        """
        return self.setPanelCtrlValues(self, data_dict, *ctrl_names)
