#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx filter choice control component.
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

from . import filter_tree_ctrl
from ..wx_filterchoicectrl import filter_choicectrl

from ...role import component as role

from ..wx_widget import component

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

EDIT_PERMISSION = dict(name='edit_tree_filter', description=_('Can edit tree filters'), type='DATA')
role.addPermision(**EDIT_PERMISSION)


class iqWxFilterTreeCtrl(filter_tree_ctrl.iqFilterTreeCtrlProto,
                         component.iqWxWidget):
    """
    Wx filter tree control component.
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

        filter_tree_ctrl.iqFilterTreeCtrlProto.__init__(self, parent=parent, id=wx.NewId(),
                                                        pos=self.getPosition(),
                                                        size=self.getSize(),
                                                        style=self.getStyle(),
                                                        name=self.getName())

        foreground_colour = self.getForegroundColour()
        if foreground_colour is not None:
            self.SetForegroundColour(wx.Colour(foreground_colour[0], foreground_colour[1], foreground_colour[2]))

        background_colour = self.getBackgroundColour()
        if background_colour is not None:
            self.SetBackgroundColour(wx.Colour(background_colour[0], background_colour[1], background_colour[2]))

        self.createChildren()

        self._filter_filename = self.getSaveFilename()
        self._environment = self.getEnvironment()
        self._limit = self.getLimit()

        # After you have defined the environment and the name of the filter storage file,
        # you can load the filters
        self.acceptFilters()

        # self.refreshIndicators(visible_items=False)

        # To update the list of objects
        self._cur_item_filter = self.buildItemFilter(self.GetRootItem())
        # self.onChange(None)

        # The flag of the end of the complete initialization of the control
        self._init_flag = True

    def getGUID(self):
        """
        Get component GUID.
        Not changeable depending on editing since passport does not change.

        :return: GUID.
        """
        if self._widget_psp_uuid:
            return self._widget_psp_uuid

        psp = self.getPassport()
        self._widget_psp_uuid = psp.getGUIDCheckSum()
        return self._widget_psp_uuid

    def _canEditFilter(self):
        return role.isPermision('edit_tree_filter')

    def onChange(self, event):
        """
        Change filter handler.
        """
        context = self.getContext()
        context['event'] = event
        function_body = self.getAttribute('on_change')
        if function_body:
            return exec_func.execTxtFunction(function=function_body,
                                             context=context)

    def getSaveFilename(self):
        """
        Filter storage filename.
        """
        if self._save_filename is None:
            save_filename = self.getAttribute('save_filename')
            self._save_filename = file_func.getNormalPath(save_filename) if save_filename else save_filename
        return self._save_filename

    def getEnvironment(self):
        """
        Get environment.
        """
        if self._environment is None:
            if self.isAttributeValue('get_env'):
                context = self.getContext()
                function_body = self.getAttribute('get_env')
                if function_body:
                    self._environment = exec_func.execTxtFunction(function=function_body,
                                                                  context=context)
        return self._environment

    def getLimit(self):
        """
        Get record limit.
        """
        if self._limit is None:
            self._limit = self.getAttribute('limit')
        return self._limit

    def getCurRecords(self, item_filter=None, **kwargs):
        """
        Code for getting a set of records that match the filter for indicators.

        :param item_filter: Data of the element filter.
            If None, no filtering is performed.
        """
        context = self.getContext()
        context['FILTER'] = item_filter
        context['LIMIT'] = self._limit
        context.update(kwargs)

        function_body = self.getAttribute('get_records')
        if function_body:
            result = exec_func.execTxtFunction(function=function_body,
                                               context=context)
            return result
        return None

    def acceptFilters(self):
        """
        Get and set the filter tree in control.

        [NOTE] This function has support for getting an alternative
        filter tree data.
        """
        if self.isAttributeValue('get_filter_tree'):
            # If the function for getting the filter tree is full,
            # then we call it. And get the filter tree data
            function_body = self.getAttribute('get_filter_tree')
            filter_tree_data = None
            if function_body:
                filter_tree_data = exec_func.execTxtFunction(function=function_body,
                                                             context=self.getContext())

            result = False
            if filter_tree_data:
                # Build tree
                # log_func.debug(u'Start build tree...')
                # log_func.debug(str(filter_tree_data.keys()))
                result = self.setTreeCtrlData(treectrl=self, tree_data=filter_tree_data, label='label')

                # Set root element caption as filter caption
                root_filter = filter_tree_data.get('__filter__', dict())
                str_filter = filter_choicectrl.getFilterAsStr(root_filter)
                root_label = str_filter if str_filter else filter_tree_ctrl.DEFAULT_ROOT_LABEL
                # self.setRootTitle(tree_ctrl=self, title=root_label)
                self.setTreeCtrlRootTitle(treectrl=self, title=root_label)

            if result:
                # If it was not possible to determine the tree for some reason,
                # then we take data from the file
                return result
            else:
                log_func.warning(u'Error build filter tree. Loading data from a file...')

        # If there was an error receiving or an alternative method is not defined,
        # then load from the default storage file
        return self.loadFilters()


COMPONENT = iqWxFilterTreeCtrl
