#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Panel manager.
"""

import types
import datetime
import wx
import wx.adv
import wx.gizmos
import wx.dataview
import wx.grid

from ...util import log_func
from ...util import dt_func
from ...util import global_func

from . import wxdatetime_func
# from . import listctrl_manager
# from . import treectrl_manager
# from . import toolbar_manager
from . import validate_manager

from . import key_combins
from . import wxobj_func
from . import wxdatetime_func

__version__ = (0, 0, 2, 2)

SKIP_ACCORD_NAMES = ('Handle', 'EventHandler', 'Parent', 'GrandParent')
SKIP_FUNCTION_TYPES = (types.FunctionType, types.MethodType, types.BuiltinFunctionType, types.BuiltinMethodType)


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
            if value is not None:
                ctrl.SetValue(value)
            result = True
        elif issubclass(ctrl.__class__, wx.RadioButton):
            if value is not None:
                ctrl.SetValue(value)
            result = True
        elif issubclass(ctrl.__class__, wx.StaticText):
            value = u'' if value is None else value
            value = value if isinstance(value, str) else str(value)
            ctrl.SetLabel(value)
            result = True
        elif issubclass(ctrl.__class__, wx.TextCtrl):
            value = u'' if value is None else value
            value = value if isinstance(value, str) else str(value)
            ctrl.SetValue(value)
            result = True
        elif issubclass(ctrl.__class__, wx.adv.DatePickerCtrl):
            try:
                value = datetime.date.min if value is None else value
                wx_dt = None
                if isinstance(value, datetime.datetime):
                    wx_dt = wxdatetime_func.datetime2wxDateTime(value)
                elif isinstance(value, datetime.date):
                    wx_dt = wxdatetime_func.date2wxDateTime(value)
                elif isinstance(value, wx.DateTime):
                    wx_dt = value
                elif isinstance(value, str) and len(value) == 10:
                    dt = datetime.datetime.strptime(value, global_func.getDefaultStrDateFmt())
                    wx_dt = wxdatetime_func.date2wxDateTime(dt)
                elif isinstance(value, str) and len(value) == 18:
                    dt = datetime.datetime.strptime(value, global_func.getDefaultStrDatetimeFmt())
                    wx_dt = wxdatetime_func.date2wxDateTime(dt)
                else:
                    log_func.warning(u'Incorrect date type <%s : %s>' % (value.__class__.__name__, str(value)))
                    result = False
                if wx_dt is not None:
                    ctrl.SetValue(wx_dt)
                    result = True
            except:
                log_func.fatal(u'Error set value <%s : %s> in DatePickerCtrl' % (str(value),
                                                                                 value.__class__.__name__))
                result = False
        elif issubclass(ctrl.__class__, wx.adv.TimePickerCtrl):
            try:
                value = datetime.datetime.min if value is None else value
                wx_dt = None
                if isinstance(value, datetime.datetime):
                    wx_dt = wxdatetime_func.datetime2wxDateTime(value)
                elif isinstance(value, datetime.date):
                    wx_dt = wxdatetime_func.date2wxDateTime(value)
                elif isinstance(value, wx.DateTime):
                    wx_dt = value
                elif isinstance(value, str) and len(value) == 8:
                    dt = datetime.datetime.strptime(value, global_func.getDefaultStrTimeFmt())
                    wx_dt = wxdatetime_func.date2wxDateTime(dt)
                elif isinstance(value, str) and len(value) == 18:
                    dt = datetime.datetime.strptime(value, global_func.getDefaultStrDatetimeFmt())
                    wx_dt = wxdatetime_func.date2wxDateTime(dt)
                else:
                    log_func.warning(u'Incorrect time type <%s : %s>' % (value.__class__.__name__, str(value)))
                    result = False
                if wx_dt is not None:
                    ctrl.SetValue(wx_dt)
                    result = True
            except:
                log_func.fatal(u'Error set value <%s : %s> in TimePickerCtrl' % (str(value),
                                                                                 value.__class__.__name__))
                result = False

        elif issubclass(ctrl.__class__, wx.DirPickerCtrl):
            if value is not None:
                ctrl.SetPath(value)
            result = True
        elif issubclass(ctrl.__class__, wx.SpinCtrl):
            value = 0 if value is None else value
            ctrl.SetValue(int(value))
            result = True
        elif issubclass(ctrl.__class__, wx.SpinCtrlDouble):
            value = 0.0 if value is None else value
            ctrl.SetValue(float(value))
            result = True
        elif issubclass(ctrl.__class__, wx.dataview.DataViewListCtrl):
            self._set_wxDataViewListCtrl_data(ctrl, value)
            result = True
        elif issubclass(ctrl.__class__, wx.RadioBox):
            if value is not None:
                ctrl.SetSelection(int(value))
            result = True
        else:
            log_func.warning(u'Panel manager. Control <%s> not support' % ctrl.__class__.__name__)
        return result

    def getPanelCtrlValue(self, ctrl):
        """
        Get control value.

        :param ctrl: Control object.
        :return: Control value.
        """
        return validate_manager.iqValidateManager.getCtrlValue(self, ctrl=ctrl)

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

        # Checking for the presence of a control with this name
        panel_children_names = dir(panel)
        not_find_ctrl_names = list()
        for ctrl_name in ctrl_names:
            if ctrl_name not in panel_children_names:
                log_func.warning(u'Not find control <%s> in panel %s' % (ctrl_name, str(panel)))
                not_find_ctrl_names.append(ctrl_names)
                continue

            if ctrl_name in SKIP_ACCORD_NAMES:
                continue
            if ctrl_name.startswith('__'):
                continue

            ctrl = getattr(panel, ctrl_name)
            if issubclass(ctrl.__class__, wx.Window):
                value = self.getPanelCtrlValue(ctrl)
                result[ctrl_name] = value
                log_func.debug(u'Get control <%s> value <%s>' % (ctrl_name, value))

        if not_find_ctrl_names:
            # Find controls in children panels
            children_panels = [getattr(panel, child_name) for child_name in panel_children_names if issubclass(getattr(panel, child_name).__class__, wx.Panel)]
            for child_panel in children_panels:
                data = self.getPanelCtrlValues(child_panel, data_dict, *not_find_ctrl_names)
                result.update(data)
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
            log_func.warning(u'Not defined fill dictionary for panel controls')
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

    def getPanelAccordCtrlData(self, panel=None):
        """
        Get consistent data.

        :param panel: Panel object.
        :return: Matching dictionary control values and names.
            Format:
            {'name': 'control value', ...}
        """
        if panel is None:
            panel = self
        accord_values = self.__accord.values()
        ctrl_data = self.getPanelCtrlData(panel, None, *accord_values)
        result_data = {name: ctrl_data.get(ctrl_name, None) for name, ctrl_name in self.__accord.items()}
        return result_data

    def setPanelAccordCtrlData(self, panel=None, **data):
        """
        Set consistent data.

        :param panel: Panel object.
        :return: Matching dictionary control values and names.
            Format:
            {'name': 'control value', ...}
        """
        if panel is None:
            panel = self
        ctrl_data = {self.__accord[name]: data[name] for name in data.keys() if name in self.__accord}
        self.setPanelCtrlData(panel, ctrl_data, *ctrl_data.keys())

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
            elif isinstance(ctrl, wx.SpinCtrlDouble):
                accord[ctrl_name] = ctrl_name
            elif isinstance(ctrl, wx.CheckBox):
                accord[ctrl_name] = ctrl_name
            elif isinstance(ctrl, wx.RadioButton):
                accord[ctrl_name] = ctrl_name
            elif isinstance(ctrl, wx.adv.DatePickerCtrl):
                accord[ctrl_name] = ctrl_name
            elif isinstance(ctrl, wx.adv.TimePickerCtrl):
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
            log_func.warning(u'Not define wx.Notebook object for set page image')
            return False
        elif not issubclass(notebook_ctrl.__class__, wx.Notebook):
            log_func.warning(u'wx.Notebook object type error')
            return False

        if n_page < 0:
            n_page = notebook_ctrl.GetSelection()
        if n_page == wx.NOT_FOUND:
            log_func.warning(u'Not define notebook page')
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
            if issubclass(ctrl.__class__, wx.Window):
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
        elif issubclass(ctrl.__class__, wx.RadioButton):
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
        elif issubclass(ctrl.__class__, wx.adv.TimePickerCtrl):
            if ctrl.GetExtraStyle() & wx.adv.DP_ALLOWNONE:
                ctrl.SetValue(None)
            else:
                wx_date = wxdatetime_func.datetime2wxDateTime(datetime.datetime.now())
                ctrl.SetValue(wx_date)
            result = True
        elif issubclass(ctrl.__class__, wx.DirPickerCtrl):
            ctrl.SetPath('')
            result = True
        elif issubclass(ctrl.__class__, wx.SpinCtrl):
            ctrl.SetValue(0)
            result = True
        elif issubclass(ctrl.__class__, wx.SpinCtrlDouble):
            ctrl.SetValue(0.0)
            result = True
        elif issubclass(ctrl.__class__, wx.dataview.DataViewListCtrl):
            self._set_wxDataViewListCtrl_data(ctrl, ())
            result = True
        elif issubclass(ctrl.__class__, wx.ListCtrl):
            ctrl.DeleteAllItems()
            result = True
        else:
            log_func.warning(u'Panel manager. Unsupported control type <%s> for clear value' % ctrl.__class__.__name__)
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
        :param redraw: Redraw? If True, resizes the panes and redraws the sash and border.
        :return: True/False.
        """
        if not isinstance(splitter, wx.SplitterWindow):
            log_func.warning(u'Error splitter object type <%s>' % str(splitter))
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
            log_func.warning(u'Not valid resized splitter panel index')
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
        :param redraw: Redraw? If True, resizes the panes and redraws the sash and border.
        :return: True/False.
        """
        if not isinstance(splitter, wx.SplitterWindow):
            log_func.warning(u'Error splitter object type <%s>' % str(splitter))
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
            log_func.warning(u'Not valid resized splitter panel index')
            return False

        # splitter.UpdateSize()

        if toolbar:
            if collapse_tool:
                toolbar.EnableTool(collapse_tool.GetId(), True)
            if expand_tool:
                toolbar.EnableTool(expand_tool.GetId(), False)
        return True

    def getPanelCtrlData(self, panel=None, data_dict=None, *ctrl_names):
        """
        Get control values.

        :param panel: Panel object.
        :param data_dict: Data dictionary.
            If None then create new dictionary.
        :param ctrl_names: Take only controls with names...
            If no control names are defined,
            then controls are processed
            indicated in the matches (accord).
        """
        if panel is None:
            panel = self
        return self.getPanelCtrlValues(panel, data_dict, *ctrl_names)

    def setPanelCtrlData(self, panel=None, data_dict=None, *ctrl_names):
        """
        Set control values.

        :param panel: Panel object.
        :param data_dict: Data dictionary.
        :param ctrl_names: Take only controls with names...
            If no control names are defined,
            then controls are processed
            indicated in the matches (accord).
        """
        if panel is None:
            panel = self
        return self.setPanelCtrlValues(panel, data_dict, *ctrl_names)
