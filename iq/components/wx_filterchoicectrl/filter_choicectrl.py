#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter choice ctrl.
"""

import copy
import os
import os.path
import uuid
import operator
import wx

from ...engine.wx.dlg import wxdlg_func 
from ...util import res_func
from ...util import log_func
from ...util import lang_func
from ...util import id_func

from . import filter_choice_dlg
from . import filter_constructor_dlg

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


DEFAULT_LIMIT_LABEL_FMT = _(u'Limit the number of objects') + ': %d'
ERROR_LIMIT_LABEL_FMT = u'(!)' + _(u'Limit exceeded') + ': %d'


class iqFilterChoiceDlg(filter_choice_dlg.iqFilterChoiceDlgProto):
    """
    Filter selection dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        filter_choice_dlg.iqFilterChoiceDlgProto.__init__(self, *args, **kwargs)

        # Filter structure
        self._filters = list()

        self.environment = None

    def setEnvironment(self, env=None):
        """
        Set the environment for the constructor to work.

        :param env: Environment.
            Format: filter_builder_env.FILTER_ENVIRONMENT.
        """
        self.environment = env

    def addFilter(self, new_filter=None):
        """
        Add new filter.

        :param new_filter: New filter structure.
        :return: True/False.
        """
        if new_filter is None:
            # Open filter constructor
            new_filter = filter_constructor_dlg.getFilterConstructorDlg(self, None, self.environment)

            if new_filter:
                filter_id = self._genUUID()
                filter_description = wxdlg_func.getTextEntryDlg(self, _(u'Filter'), _(u'Enter filter name'))
                new_filter['record_id'] = filter_id
                new_filter['description'] = filter_description
            else:
                log_func.warning(u'No filter defined to add')
                return False

        if new_filter:
            self._filters.append(new_filter)
            self.filterCheckList.Append(new_filter['description'], new_filter['record_id'])

    def delFilter(self, filter_name=None):
        """
        Delete filter.

        :param filter_name: Filter name.
        :return: True/False.
        """
        if filter_name is None:
            # If no name is specified remove the selected filter
            i = self.filterCheckList.GetSelection()
            if i >= 0:
                do_del = wxdlg_func.openAskBox(_(u'DELETE'), _(u'Delete filter?'))
                if do_del:
                    del self._filters[i]
                    self.filterCheckList.Delete(i)
                    return True
                return False
        else:
            filters_id = [filter_dict['record_id'] for filter_dict in self._filters]
            try:
                i = filters_id.index(filter_name)
            except IndexError:
                log_func.warning(u'Filter <%s> not found in <%s>' % (filter_name, filters_id))
                return False
            del self._filters[i]
            self.filterCheckList.Delete(i+1)
            return True

    def getFilter(self):
        """
        Get result filter.
        For all filters, the root element must be group.
        """
        filters_list = list()
        checks = [self.filterCheckList.IsChecked(i) for i in range(self.filterCheckList.GetCount())]
        for i, check in enumerate(checks):
            self._filters[i]['check'] = check
            filters_list.append(self._filters[i])

        # For all filters, the root element must be group
        group_dict = dict()
        group_dict['name'] = 'grp'
        group_dict['type'] = 'group'
        group_dict['logic'] = 'AND' if self.logicRadioBox.GetSelection() else 'OR'
        group_dict['description'] = _(u'AND') if self.logicRadioBox.GetSelection() else _(u'OR')
        group_dict['children'] = filters_list
        return group_dict

    def clearFilters(self):
        """
        Clear all filters.

        :return: True/False
        """
        self._filters = []
        self.filterCheckList.Clear()

    def setFilters(self, filter_data=None):
        """
        Set control filters.

        :param filter_data: Filter data.
            If None, then just set the filter list
            without installing a logical bundle.
        :return: True/False.
        """
        if filter_data is not None:
            # Clear
            self.clearFilters()

            # Choosing a filter connection condition
            and_or = filter_data.get('logic', 'OR')
            if and_or == 'OR':
                self.logicRadioBox.SetSelection(0)
            else:
                self.logicRadioBox.SetSelection(1)

            self._filters = filter_data.get('children', [])
        else:
            self.filterCheckList.Clear()

        # Set filter list
        for filter_dict in self._filters:
            name = filter_dict.get('description', filter_dict.get('guid', id_func.genGUID()))
            item = self.filterCheckList.Append(name, name)
            # Mark immediately if items are marked in the filter
            self.filterCheckList.Check(item, filter_dict.get('check', False))
        return True

    def refreshFilters(self):
        """
        Refresh filter control.

        :return: True/False.
        """
        return self.setFilters()

    def sortFilters(self, is_reverse=False):
        """
        Sort filter list by name.

        :param is_reverse: Is reverse sort?
        :return: Sorted filter list.
        """
        self._filters = sorted(self._filters,
                               key=operator.itemgetter('description'))
        if is_reverse:
            self._filters.reverse()

        self.refreshFilters()
        return self._filters

    def moveFilterUp(self, filter_idx=None):
        """
        Move up filter in list by index.

        :param filter_idx: Filter index. If None, then get selected.
        :return: True/False.
        """
        if filter_idx is None:
            filter_idx = self.filterCheckList.GetSelection()
        num_filters = len(self._filters)
        if (filter_idx < 0) or (filter_idx >= num_filters):
            log_func.warning(u'Not valid index <%s>' % filter_idx)
            return False
        elif filter_idx == 0:
            log_func.warning(u'It is not possible to move the filter higher')
            return False
        # Swap filters
        selected_filter = self._filters[filter_idx]
        self._filters[filter_idx] = self._filters[filter_idx - 1]
        self._filters[filter_idx - 1] = selected_filter

        self.refreshFilters()
        # Select filter
        self.filterCheckList.setSelection(filter_idx - 1)
        return True

    def moveFilterDown(self, filter_idx=None):
        """
        Move down filter in list by index.

        :param filter_idx: Filter index. If None, then get selected.
        :return: True/False.
        """
        if filter_idx is None:
            filter_idx = self.filterCheckList.GetSelection()
        num_filters = len(self._filters)
        if (filter_idx < 0) or (filter_idx >= num_filters):
            log_func.warning(u'Not valid index <%s>' % filter_idx)
            return False
        elif filter_idx == num_filters-1:
            log_func.warning(u'It is not possible to move the filter under')
            return False
        # Swap filters
        selected_filter = self._filters[filter_idx]
        self._filters[filter_idx] = self._filters[filter_idx + 1]
        self._filters[filter_idx + 1] = selected_filter

        self.refreshFilters()
        # Select
        self.filterCheckList.setSelection(filter_idx + 1)
        return True

    def setLimitLabel(self, limit=None, over_limit=None):
        """
        Display a message about limiting the number of objects.

        :param limit: Objects limit.
        :param over_limit: The number of objects when the limit is exceeded.
        """
        if over_limit:
            try:
                label = ERROR_LIMIT_LABEL_FMT % int(over_limit)
                self.limit_staticText.SetLabel(label)
                self.limit_staticText.SetForegroundColour(wx.RED)
                return
            except:
                log_func.fatal(u'Error in setLimitLabel method')
        if limit:
            # There is a limit, but not exceeded
            try:
                label = DEFAULT_LIMIT_LABEL_FMT % int(limit)
                self.limit_staticText.SetLabel(label)
                fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
                self.limit_staticText.SetForegroundColour(fg)
                return
            except:
                log_func.fatal(u'Error in setLimitLabel method')
        # No limit
        self.limit_staticText.SetLabel(u'')

    def onAddButtonClick(self, event):
        """
        The handler for the add filter button.
        """
        try:
            self.GetParent().addFilter()
        except AttributeError:
            self.addFilter()
        event.Skip()

    def onDelButtonClick(self, event):
        """
        The handler for the filter delete button.
        """
        try:
            self.GetParent().delFilter()
        except AttributeError:
            self.delFilter()

        event.Skip()

    def onCancelButtonClick(self, event):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onSortToolClick(self, event):
        """
        Button handler for sorting filters.
        """
        try:
            self.GetParent().sortFilters()
        except AttributeError:
            self.sortFilters()
        event.Skip()

    def onSortReverseToolClick(self, event):
        """
        Button handler for reverse filter sorting.
        """
        try:
            self.GetParent().sortFilters(is_reverse=True)
        except AttributeError:
            self.sortFilters(is_reverse=True)
        event.Skip()

    def onMoveUpToolClick(self, event):
        """
        The handler for the button for moving the current filter up the list of filters.
        """
        try:
            self.GetParent().moveFilterUp()
        except AttributeError:
            self.moveFilterUp()
        event.Skip()

    def onMoveDownToolClick(self, event):
        """
        The handler for the button to move the current filter down the filter list.
        """
        try:
            self.GetParent().moveFilterDown()
        except AttributeError:
            self.moveFilterDown()
        event.Skip()


def getFilterChoiceDlg(parent=None, environment=None, cur_filter=None,
                       limit=None, over_limit=None):
    """
    Dialog form for filter selection.

    :param parent: Parent window.
    :param environment: Environment.
        Format: filter_builder_env.FILTER_ENVIRONMENT.
    :param cur_filter: Resulting edited filter.
    :param limit: Limit the number of lines of the filtered object.
    :param over_limit: The number of rows when the limit is exceeded.
    :return: Selected filter or None if error or cancel.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    if cur_filter is None:
        cur_filter = dict()

    result_filter = None
    try:
        dlg = iqFilterChoiceDlg(parent=parent)
        dlg.setEnvironment(environment)
        dlg.setFilters(cur_filter)
        dlg.setLimitLabel(limit, over_limit)
        if dlg.ShowModal() == wx.ID_OK:
            result_filter = dlg.getFilter()
        dlg.Destroy()
        return result_filter
    except:
        log_func.fatal(u'Error choice filter dialog')
    return None


def getFilterAsStr(cur_filter):
    """
    Get filter as string.

    :return: Filter string.
    """
    if cur_filter:
        join_str = u' %s ' % cur_filter.get('description', _(u'OR'))
        return join_str.join([u'<%s>' % fltr.get('description', fltr.get('name', '...')) for fltr in cur_filter.get('children', ()) if fltr.get('check', False)])
    return u''


class iqFilterChoiceCtrlProto(wx.ComboCtrl):
    """
    Filter choice control.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        kwargs['style'] = wx.CB_READONLY | wx.CB_DROPDOWN | kwargs.get('style', 0)

        wx.ComboCtrl.__init__(self, *args, **kwargs)

        # self._uuid = None

        self._initButton()

        # Resulting edited filter
        self._filter = dict()

        # The name of the filter storage file
        self._filter_filename = None

        # Filter environment
        self._environment = None

        # Filter choice dialog
        self._dlg = None

        # Limit the number of lines of the filtered object
        self._limit = None
        # Number of lines when the limit is exceeded
        self._over_limit = None

    def setEnvironment(self, env=None):
        """
        Set environment.

        :param env: Environment.
            Format: filter_builder_env.FILTER_ENVIRONMENT.
        """
        self._environment = env

    def getEnvironment(self):
        """
        Get environment.
        """
        return self._environment

    def _initButton(self):
        """
        Initialization button <...>.
        """
        # make a custom bitmap showing "..."
        bw, bh = 14, 16
        bmp = wx.Bitmap(bw, bh)
        dc = wx.MemoryDC(bmp)

        # clear to a specific background colour
        bgcolor = wx.Colour(255, 255, 255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()

        # draw the label onto the bitmap
        label = '...'
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        tw, th = dc.GetTextExtent(label)
        dc.DrawText(label, (bw-tw)/2, (bw-tw)/2)
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)

        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)

    def getFilter(self):
        """
        Get result filter.
        """
        return self._filter

    def getStructFilter(self):
        """
        Get result filter without not marked.

        :return: Filter or None if error.
        """
        if self._filter:
            struct_filter = copy.deepcopy(self._filter)
            struct_filter['children'] = [fltr for fltr in struct_filter['children'] if fltr['check']]
            return struct_filter
        return None

    def getLimit(self):
        """
        Get limit the number of lines of the filtered object.
        """
        if self._limit < 0:
            self._limit = 0
        return self._limit

    def validLimit(self, obj_count):
        """
        Verification of overcoming restrictions.
        The function automatically signals that the limit has been overcome.

        :param obj_count: Object number.
        :return: True - restriction not overcome / False - limit exceeded.
        """
        valid = obj_count <= self._limit
        if not valid:
            self._over_limit = obj_count
            self.SetBackgroundColour(wx.RED)
        else:
            self._over_limit = None
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        return valid

    def doDlgChoiceFilter(self):
        """
        Calling the filter selection dialog box.

        :return: True - press <OK>, False - press <Cancel>.
        """
        result = False
        self._dlg = iqFilterChoiceDlg(self)
        self._dlg.setEnvironment(self._environment)
        self._dlg.setFilters(self._filter)
        self._dlg.setLimitLabel(self._limit, self._over_limit)
        if self._dlg.ShowModal() == wx.ID_OK:
            self._filter = self._dlg.getFilter()
            self.saveFilter()
            str_filter = self.getStrFilter()
            self.SetValue(str_filter)
            result = True
        self._dlg.Destroy()
        self._dlg = None
        return result

    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.
        """
        self.doDlgChoiceFilter()
        self.SetFocus()

    def getStrFilter(self):
        """
        Get filter as string.

        :return: Filter string.
        """
        if self._filter:
            join_str = u' %s ' % self._filter.get('description', u'ИЛИ')
            return join_str.join([u'<%s>' % fltr.get('description', fltr.get('name', '...')) for fltr in self._filter['children'] if fltr.get('check', False)])
        return u''

    def DoSetPopupControl(self, popup):
        """
        Overridden from ComboCtrl to avoid assert since there is no ComboPopup.
        """
        pass

    def getFilterFileName(self):
        """
        Get filter filename.
        """
        return self._filter_filename

    def setFilterFileName(self, filename):
        """
        Set filter filename.
        """
        log_func.info(u'Control [%s]. Set filter filename <%s>' % (self.getGUID(), filename))
        self._filter_filename = filename

    def saveFilter(self, filter_filename=None):
        """
        Save filter.

        :param filter_filename: Filter filename.
            If None, then generate by UUID.
        :return: True/False.
        """
        if filter_filename:
            filter_filename = os.path.normpath(filter_filename)
        else:
            filter_filename = self._filter_filename

        if filter_filename:
            if os.path.exists(filter_filename):
                # Load filter file
                res = res_func.loadResource(filter_filename)
                if res:
                    # Save filter to file
                    res[self.getGUID()] = self._filter
                    res_func.saveResourcePickle(filter_filename, res)
                else:
                    log_func.warning(u'Error resource file <%s>' % filter_filename)
                    return False
            else:
                # Просто записать в файл
                res = {self.getGUID(): self._filter}
                res_func.saveResourcePickle(filter_filename, res)
        else:
            log_func.warning(u'Filter filename not defined')
            return False
        return True

    def loadFilter(self, filter_filename=None):
        """
        Load filter.

        :param filter_filename: Filter filename.
            If None, then generate by UUID.
        """
        if filter_filename:
            filter_filename = os.path.normpath(filter_filename)
        else:
            filter_filename = self._filter_filename

        if filter_filename and os.path.exists(filter_filename):
            res = res_func.loadResource(filter_filename)
            if res:
                if self.getGUID() not in res:
                    log_func.warning(u'Filter not found for control <%s> in file <%s : %s>' % (self.getGUID(),
                                                                                               filter_filename,
                                                                                               str(res.keys() if res else res)))
                    self.saveFilter(filter_filename)
                    return

                filter_data = res.get(self.getGUID(), None)
                if filter_data:
                    self.setFilter(filter_data)
                else:
                    log_func.warning(u'Filter not defined for control <%s> in file <%s>' % (self.getGUID(),
                                                                                            filter_filename))
        else:
            log_func.warning(u'Filter file <%s> not found' % filter_filename)
            self.saveFilter(filter_filename)

    def setFilter(self, filter_data):
        """
        Set filter.

        :param filter_data: Filter data.
        :return: True/False.
        """
        self._filter = filter_data
        return True

    def getFilterFilename(self):
        return self._filter_filename

    def addFilter(self, *args, **kwargs):
        """
        Add new filter.
        """
        if self._dlg:
            return self._dlg.addFilter(*args, **kwargs)
        return False

    def delFilter(self, *args, **kwargs):
        """
        Delete filter.
        """
        if self._dlg:
            return self._dlg.delFilter(*args, **kwargs)
        return False

    def sortFilters(self, *args, **kwargs):
        """
        Sort filter list by name.
        """
        if self._dlg:
            return self._dlg.sortFilters(*args, **kwargs)
        return False

    def moveFilterUp(self, *args, **kwargs):
        """
        Move up filter in list by index.
        """
        if self._dlg:
            return self._dlg.moveFilterUp(*args, **kwargs)
        return False

    def moveFilterDown(self, *args, **kwargs):
        """
        Move down filter in list by index.
        """
        if self._dlg:
            return self._dlg.moveFilterDown(*args, **kwargs)
        return False
