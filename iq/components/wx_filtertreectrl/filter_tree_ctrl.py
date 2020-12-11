#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter tree control with node indicators.
"""

# import copy
import uuid
import os.path
# import wx
from wx.lib.agw import flatmenu

from iq.dialog import dlg_func
from iq.util import file_func
from iq.util import spc_func

from iq.engine.wx import treectrl_manager
from iq.engine import stored_ctrl_manager

from ..wx_filterchoicectrl import filter_choicectrl
from .tree_item_indicator import *
from ..wx_filterchoicectrl.filter_generate import *

__version__ = (0, 0, 0, 1)

DEFAULT_ROOT_LABEL = u'...'
DEFAULT_NODE_LABEL = u'New node'
DEFAULT_NODE_IMAGE_FILENAME = 'document.png'

# Empty entry attached to node
EMPTY_NODE_RECORD = {'__filter__': None, '__indicator__': None, 'label': u''}


# Functions for managing the structure of the filter tree
def emptyItem(label=DEFAULT_NODE_LABEL):
    """
    Empty item.

    :param label: Node label.
    :return: Empty node structure.
    """
    item_filter = copy.deepcopy(EMPTY_NODE_RECORD)
    item_filter['label'] = label
    return item_filter


def addChildItemFilter(filter_tree_data, child_item_filter=None):
    """
    Add node as child.

    :param filter_tree_data: Node date.
    :param child_item_filter: Child node data.
        If not specified, an empty node is created.
    :return: Modified node data.
    """
    if child_item_filter is None:
        child_item_filter = emptyItem()

    if spc_func.CHILDREN_ATTR_NAME not in filter_tree_data:
        filter_tree_data[spc_func.CHILDREN_ATTR_NAME] = list()
    filter_tree_data[spc_func.CHILDREN_ATTR_NAME].append(child_item_filter)
    return filter_tree_data


def newItemFilter(filter_tree_data, label=DEFAULT_NODE_LABEL):
    """
    Add a new filter to an existing node.

    :param filter_tree_data: Node data.
    :param label: Node label.
    :return: Modified node data.
    """
    if spc_func.CHILDREN_ATTR_NAME not in filter_tree_data or filter_tree_data[spc_func.CHILDREN_ATTR_NAME] is None:
        filter_tree_data[spc_func.CHILDREN_ATTR_NAME] = list()

    item_filter = emptyItem(label)
    return addChildItemFilter(filter_tree_data, item_filter)


def setFilter(filter_tree_data, item_filter=None):
    """
    Install an existing node filter.

    :param filter_tree_data: Node data.
    :param item_filter: Filter data.
    :return: Modified node data.
    """
    filter_tree_data['__filter__'] = item_filter
    return filter_tree_data


def setIndicator(filter_tree_data, item_indicator=None):
    """
    Set an existing node indicator.

    :param filter_tree_data: Node date.
    :param item_indicator: Indicator data.
    :return: Modified node data.
    """
    filter_tree_data['__indicator__'] = item_indicator
    return filter_tree_data


def getFilter(filter_tree_data):
    """
    Get node filter.

    :param filter_tree_data: Node data.
    :return: Node filter data.
    """
    return filter_tree_data['__filter__']


def getIndicator(filter_tree_data):
    """
    Get node indicator.

    :param filter_tree_data: Node data.
    :return: Node indicator data.
    """
    return filter_tree_data['__indicator__']


def setLabel(filter_tree_data, label=u''):
    """
    Set node label.

    :param filter_tree_data: Node data.
    :param label: Label.
    :return: Modified node data.
    """
    filter_tree_data['label'] = label
    return filter_tree_data


def findLabel(filter_tree_data, label=u''):
    """
    Find node by label.

    :param filter_tree_data: Node data.
    :param label: Label.
    :return: The data of the searched node or None if the node is not found.
    """
    if filter_tree_data.get('label', None) == label:
        return filter_tree_data
    if spc_func.CHILDREN_ATTR_NAME in filter_tree_data and filter_tree_data[spc_func.CHILDREN_ATTR_NAME]:
        for child in filter_tree_data[spc_func.CHILDREN_ATTR_NAME]:
            find_result = findLabel(child, label=label)
            if find_result:
                return find_result
    return None


class iqFilterTreeCtrlProto(wx.TreeCtrl,
                            iqTreeItemIndicator,
                            treectrl_manager.iqTreeCtrlManager,
                            stored_ctrl_manager.iqStoredCtrlManager):
    """
    Controlling the tree view of filters with node indicators.
    Abstract class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        # The flag of the end of the complete initialization of the control
        self._init_flag = False

        wx.TreeCtrl.__init__(self, *args, **kwargs)

        iqTreeItemIndicator.__init__(self)

        # By default, we create the root element
        self.AddRoot(DEFAULT_ROOT_LABEL)
        root_data = copy.deepcopy(EMPTY_NODE_RECORD)
        root_data['label'] = DEFAULT_ROOT_LABEL
        # self.setItemData_tree(ctrl=self, data=root_data)
        self.setTreeCtrlItemData(treectrl=self, data=root_data)

        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onItemRightClick)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onItemDoubleClick)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onItemSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onItemExpanded)
        # [NOTE] If you need to delete / free resources
        # when deleting a control, then you need
        # to use the event wx.EVT_WINDOW_DESTROY
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

        self._uuid = None

        # Filters storage file name
        self._save_filename = None

        # Filter environment
        self._environment = None

        # Limiting the number of lines of the filtered object
        self._limit = None
        # Number of lines when the limit is exceeded
        # self._over_limit = None

        # The current filter of the selected item
        self._cur_item_filter = None

    def _canEditFilter(self):
        return True

    def onDestroy(self, event):
        """
        When removing a panel. Event handler.

        [NOTE] If you need to delete / free resources
        when deleting a control, then you need
        to use the event wx.EVT_WINDOW_DESTROY
        """
        self.saveFilters()
        event.Skip()

    def getUUID(self):
        if not self._uuid:
            self._uuid = self._genUUID()
        return self._uuid

    def _genUUID(self):
        """
        Generate UUID.

        :return: UUID.
        """
        return str(uuid.uuid4())

    def setSaveFilename(self, filename):
        """
        Set the full name of the filter storage file.

        :param filename: File name.
        """
        self._save_filename = filename

    def getSaveFilename(self):
        """
        Get filter storage filename.
        """
        return self._save_filename

    def getLimit(self):
        """
        Limiting the number of lines of the filtered object.
        """
        return self._limit

    def setLimit(self, limit=0):
        """
        Set a limit on the number of lines of the filtered object.

        :param limit: Limit on lines. If not specified, then there is no limit.
        """
        self._limit = limit

    def getCurItemFilter(self):
        """
        Current full filter.
        """
        if self._cur_item_filter is None:
            # Full filter is not defined.We believe it is a root element filter
            self._cur_item_filter = self.getItemFilter()
        return self._cur_item_filter

    def getItemFilter(self, item=None):
        """
        Filter attached to the element.

        :param item: The current item being processed.
             If None, then the root element is taken.
        :return: Filter structure or None if no filter is defined.
        """
        if item is None:
            item = self.GetRootItem()

        # item_data = self.getItemData_tree(ctrl=self, item=item)
        item_data = self.getTreeCtrlItemData(treectrl=self, item=item)
        return item_data.get('__filter__', None) if item_data else None

    def getItemIndicator(self, item=None):
        """
        Get item indicator.

        :param item: The current item being processed.
             If None, then the root element is taken.
        :return: Indicator structure or None if the indicator is not defined.
        """
        if item is None:
            item = self.GetRootItem()

        # item_data = self.getItemData_tree(ctrl=self, item=item)
        item_data = self.getTreeCtrlItemData(treectrl=self, item=item)
        return item_data.get('__indicator__', None) if item_data else None

    def onItemRightClick(self, event):
        """
        Right button click handler.
        """
        menu = self.createPopupMenu()
        if menu:
            menu.Popup(wx.GetMousePosition(), self)
        # select_component_menu.popup_component_flatmenu(parent=self)
        event.Skip()

    def editRootFilter(self, root_item=None):
        """
        Editing the filter of the root element.

        :param root_item: Root item.
            If not specified, then it is taken automatically.
        :return: True/False.
        """
        if root_item is None:
            root_item = self.GetRootItem()

        # if not self.isRootTreeItem(ctrl=self, item=root_item):
        if not self.isTreeCtrlRootItem(treectrl=self, item=root_item):
            # If not the root element, skip processing
            return False

        try:
            # item_data = self.getItemData_tree(ctrl=self, item=root_item)
            item_data = self.getTreeCtrlItemData(treectrl=self, item=root_item)
            cur_filter = item_data.get('__filter__', None)
            cur_filter = filter_choicectrl.get_filter_choice_dlg(parent=self,
                                                                 environment=self._environment,
                                                                 cur_filter=cur_filter)
            if cur_filter:
                item_data['__filter__'] = cur_filter
                return True
        except:
            log_func.fatal(u'Root element filter setting error')
        return False

    def onItemDoubleClick(self, event):
        """
        Handler for double click on a tree element.
        """
        item = event.GetItem()
        self.editRootFilter(root_item=item)
        self.refreshRootItemTitle()

        # To update the list of objects
        self._cur_item_filter = self.buildItemFilter(item)
        self.OnChange(event)

        # event.Skip()

    def OnChange(self, event):
        """
        Filter change.
        """
        log_func.error(u'Not define <OnChange> function in <%s> component' % self.__class__.__name__)

    def onItemSelectChanged(self, event):
        """
        Handler for changing the selection of a tree element.
        """
        item = event.GetItem()
        self._cur_item_filter = self.buildItemFilter(item)

        # Transfer processing to component
        self.OnChange(event)

        event.Skip()

    def _buildFilters(self, cur_filters):
        """
        Internal function of building the structure of filters.

        :param cur_filters: The current filter list being processed.
        :return: Assembled filter structure.
        """
        # Filter not included filters
        filters = [copy.deepcopy(cur_filter) for cur_filter in cur_filters if cur_filter.get('check', True)]

        # Child elements are processed first to exclude empty filters
        result_filters = list()
        for i, cur_filter in enumerate(filters):
            filter_type = cur_filter['type']
            children = cur_filter.get('children', list())
            children = self._buildFilters(children)
            if children and filter_type == 'group':
                cur_filter['children'] = children
                result_filters.append(cur_filter)
            elif filter_type == 'compare':
                result_filters.append(cur_filter)

        return result_filters

    def buildItemFilter(self, item=None):
        """
        Construction of a complete filter corresponding to the specified tree element.

        :param item: Tree item.
            If not specified, the currently selected item is taken.
        :return: The assembled structure of the filter corresponding to the specified tree item.
        """
        if item is None:
            item = self.GetSelection()

        # item_data_path = self.getItemPathData(tree_ctrl=self, item=item)
        item_data_path = self.getTreeCtrlItemPathData(treectrl=self, item=item)

        filters = list()
        if item_data_path:
            filters = [data.get('__filter__', None) for data in item_data_path if data.get('__filter__', None)]
            filters = self._buildFilters(filters)
        else:
            log_func.warning(u'Structural data of the tree element is not defined')
        grp_filter = createFilterGroupAND(*filters)
        return grp_filter

    def createPopupMenu(self):
        """
        Create a pop-up menu for managing the filter tree.

        :return: wx.Menu object.
        """
        try:
            cur_item = self.GetSelection()
            if not cur_item:
                log_func.warning(u'No tree item selected')
                return None
            # item_data = self.getItemData_tree(ctrl=self, item=cur_item)
            item_data = self.getTreeCtrlItemData(treectrl=self, item=cur_item)

            menu = flatmenu.FlatMenu()

            rename_menuitem_id = wx.NewId()
            bmp = wxbitmap_func.createIconBitmap('fatcow/textfield_rename')
            menuitem = flatmenu.FlatMenuItem(menu, rename_menuitem_id, u'Rename',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onRenameMenuItem, id=rename_menuitem_id)

            moveup_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_MENU,
                                           (wxbitmap_func.DEFAULT_ICON_WIDTH,
                                            wxbitmap_func.DEFAULT_ICON_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, moveup_menuitem_id, u'Move up',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onMoveUpMenuItem, id=moveup_menuitem_id)
            menuitem.Enable(not self.isTreeCtrlFirstItem(treectrl=self, item=cur_item))

            movedown_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_MENU,
                                           (wxbitmap_func.DEFAULT_ICON_WIDTH,
                                            wxbitmap_func.DEFAULT_ICON_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, movedown_menuitem_id, u'Move down',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onMoveDownMenuItem, id=movedown_menuitem_id)
            menuitem.Enable(not self.isTreeCtrlLastItem(treectrl=self, item=cur_item))

            menu.AppendSeparator()

            add_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_MENU,
                                           (wxbitmap_func.DEFAULT_ICON_WIDTH,
                                            wxbitmap_func.DEFAULT_ICON_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, add_menuitem_id, u'Add',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onAddMenuItem, id=add_menuitem_id)
            menuitem.Enable(self._canEditFilter())

            del_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_MENU,
                                           (wxbitmap_func.DEFAULT_ICON_WIDTH,
                                            wxbitmap_func.DEFAULT_ICON_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, del_menuitem_id, u'Del',
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onDelMenuItem, id=del_menuitem_id)
            menuitem.Enable(self._canEditFilter())

            filter_menuitem_id = wx.NewId()
            bmp = wxbitmap_func.createIconBitmap('fatcow/filter')
            cur_filter = item_data.get('__filter__', None) if item_data else None
            label = u'Filter: %s' % filter_choicectrl.get_str_filter(cur_filter) if cur_filter else u'Filter'
            menuitem = flatmenu.FlatMenuItem(menu, filter_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onFilterMenuItem, id=filter_menuitem_id)
            menuitem.Enable(self._canEditFilter())

            indicator_menuitem_id = wx.NewId()
            bmp = wxbitmap_func.createIconBitmap('fatcow/traffic_lights')
            cur_indicator = item_data.get('__indicator__', None) if item_data else None
            label = u'Indicator: %s' % self.getLabelIndicator(cur_indicator) if cur_indicator else u'Indicator'
            menuitem = flatmenu.FlatMenuItem(menu, indicator_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onIndicatorMenuItem, id=indicator_menuitem_id)
            menuitem.Enable(self._canEditFilter())

            return menu
        except:
            log_func.fatal(u'Error creating menu for managing filter tree')
        return None

    def renameItem(self, cur_item=None):
        """
        Rename item.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            if cur_item:
                cur_label = self.GetItemText(cur_item)
                label = dlg_func.getTextEntryDlg(self, u'RENAME', u'Name', cur_label)

                if label:
                    bmp = None
                    # bmp = ic_bmp.createLibraryBitmap(DEFAULT_NODE_IMAGE_FILENAME)
                    # data_record = self.getItemData_tree(ctrl=self, item=cur_item)
                    data_record = self.getTreeCtrlItemData(treectrl=self, item=cur_item)
                    data_record['label'] = label
                    self.SetItemText(cur_item, label)
                    # return self.setItemData_tree(ctrl=self, item=cur_item, data=data_record)
                    return self.setTreeCtrlItemData(treectrl=self, item=cur_item, data=data_record)
            else:
                log_func.warning(u'The current tree element is not defined')
        except:
            log_func.fatal(u'Filter rename error')
        return False

    def onRenameMenuItem(self, event):
        """
        Rename the node. Handler.
        """
        self.renameItem()
        # event.Skip()

    def moveUpItem(self, cur_item=None):
        """
        Move the node up the list.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()

            return self.moveUpTreeCtrlItem(treectrl=self, item=cur_item)
        except:
            log_func.fatal(u'Error moving a node up the list')
        return False

    def onMoveUpMenuItem(self, event):
        """
        Move the node up the list. Handler.
        """
        self.moveUpItem()
        # event.Skip()

    def moveDownItem(self, cur_item=None):
        """
        Move a node down the list.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()

            return self.moveDownTreeCtrlItem(treectrl=self, item=cur_item)
        except:
            log_func.fatal(u'Error moving node down the list')
        return False

    def onMoveDownMenuItem(self, event):
        """
        Move the node down the list. Handler.
        """
        self.moveDownItem()
        # event.Skip()

    def addFilterItem(self, cur_item=None):
        """
        Add filter.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            if cur_item:
                label = dlg_func.getTextEntryDlg(self, u'ADD', u'Name',
                                                 DEFAULT_NODE_LABEL)

                if label:
                    bmp = None
                    # bmp = ic_bmp.createLibraryBitmap(DEFAULT_NODE_IMAGE_FILENAME)
                    data_record = copy.deepcopy(EMPTY_NODE_RECORD)
                    data_record['label'] = label
                    # new_item = self.appendChildItem_tree_ctrl(ctrl=self, parent_item=cur_item, label=label,
                    #                                           image=bmp, data=data_record, select=True)
                    new_item = self.appendTreeCtrlChildItem(treectrl=self, parent_item=cur_item, label=label,
                                                            image=bmp, data=data_record, select=True)
                    return True
            else:
                log_func.warning(u'The current tree element is not defined')
        except:
            log_func.fatal(u'Filter adding error')
        return False

    def onAddMenuItem(self, event):
        """
        Add filter. Handler.
        """
        self.addFilterItem()
        # event.Skip()

    def delFilterItem(self, cur_item=None):
        """
        Delete filter.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()

            return self.deleteTreeCtrlItem(treectrl=self, item=cur_item, ask=True)
        except:
            log_func.fatal(u'Error delete filter')
        return False

    def onDelMenuItem(self, event):
        """
        Delete filter. Handler.
        """
        self.delFilterItem()
        # event.Skip()

    def editFilterItem(self, cur_item=None):
        """
        Edit filter.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            # item_data = self.getItemData_tree(ctrl=self, item=cur_item)
            item_data = self.getTreeCtrlItemData(treectrl=self, item=cur_item)
            cur_filter = item_data.get('__filter__', None)
            cur_filter = filter_choicectrl.get_filter_choice_dlg(parent=self,
                                                                 environment=self._environment,
                                                                 cur_filter=cur_filter)
            if cur_filter:
                item_data['__filter__'] = cur_filter
                return True
        except:
            log_func.fatal(u'Error edit filter')
        return False

    def refreshRootItemTitle(self):
        """
        Update the label of the root element according to the selected filter.

        :return: True/False.
        """
        item = self.GetRootItem()
        # item_data = self.getItemData_tree(ctrl=self, item=item)
        item_data = self.getTreeCtrlItemData(treectrl=self, item=item)
        cur_filter = item_data.get('__filter__', None)
        label = filter_choicectrl.get_str_filter(cur_filter) if cur_filter else DEFAULT_ROOT_LABEL
        if not label:
            label = DEFAULT_ROOT_LABEL
        # self.setRootTitle(tree_ctrl=self, title=label)
        self.setTreeCtrlRootTitle(treectrl=self, title=label)
        return True

    def onFilterMenuItem(self, event):
        """
        Edit filter. Handler.
        """
        self.editFilterItem()

        # After editing the filter, if it is a root element,
        # then change the label of the root element
        cur_item = self.GetSelection()
        if self.isTreeCtrlRootItem(treectrl=self, item=cur_item):
            self.refreshRootItemTitle()

        # To update the list of objects
        self._cur_item_filter = self.buildItemFilter(cur_item)
        self.OnChange(event)

        # event.Skip()

    def editIndicatorItem(self, cur_item=None):
        """
        Edit indicator.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            # item_data = self.getItemData_tree(ctrl=self, item=cur_item)
            item_data = self.getTreeCtrlItemData(treectrl=self, item=cur_item)
            cur_indicator = item_data.get('__indicator__', None)
            cur_indicator = self.editIndicator(parent=self, indicator=cur_indicator)
            if cur_indicator:
                item_data['__indicator__'] = cur_indicator
                return True
        except:
            log_func.fatal(u'Error edit indicator')
        return False

    def onIndicatorMenuItem(self, event):
        """
        Edit indicator. Handler.
        """
        self.editIndicatorItem()
        # event.Skip()

    def getCurRecords(self, item_filter=None):
        """
        Code for getting a set of records that match the filter for indicators.

        :param item_filter: Data of the element filter.
            If None, no filtering is performed.
        """
        log_func.error(u'Not define <getCurRecords> function in component <%s>' % self.__class__.__name__)

    def saveFilters(self, save_filename=None):
        """
        Save filter information to file.

        :param save_filename: The name of the filter storage file.
            If not specified, then generated by UUID.
        :return:
        """
        if save_filename is None:
            save_filename = self._save_filename

        if save_filename:
            save_filename = os.path.normpath(save_filename)
        else:
            widget_uuid = self.getUUID()
            save_filename = os.path.join(file_func.getProjectProfilePath(),
                                         widget_uuid + '.dat')

        filter_tree_data = self.getTreeCtrlData(treectrl=self)
        return self.saveCustomData(save_filename=save_filename, save_data=filter_tree_data)

    def loadFilters(self, save_filename=None):
        """
        Load filters.

        :param save_filename: The name of the filter storage file.
            If not specified, then generated by UUID.
        """
        if save_filename is None:
            save_filename = self._save_filename

        if save_filename:
            save_filename = os.path.normpath(save_filename)
        else:
            widget_uuid = self.getUUID()
            save_filename = os.path.join(file_func.getProjectProfilePath(),
                                         widget_uuid + '.dat')

        filter_tree_data = self.loadCustomData(save_filename=save_filename)
        if filter_tree_data:
            # Build tree
            result = self.setTreeCtrlData(treectrl=self, tree_data=filter_tree_data, label='label')

            # Set root element caption as filter caption
            root_filter = filter_tree_data.get('__filter__', dict())
            str_filter = filter_choicectrl.get_str_filter(root_filter)
            root_label = str_filter if str_filter else DEFAULT_ROOT_LABEL
            # self.setRootTitle(tree_ctrl=self, title=root_label)
            self.setTreeCtrlRootTitle(treectrl=self, title=root_label)
        else:
            log_func.warning(u'Empty filter tree data')
            result = False

        return result

    def acceptFilters(self):
        """
        Get and set the filter tree in control.
        """
        return self.loadFilters()

    def refreshIndicators(self, visible_items=True, item=None, restore_dataset=True, progress=False):
        """
        Refresh indicators of tree elements.

        :param visible_items: Refresh indicators of visible tree elements?
            If not, then the indicators of all elements are updated.
        :param item: The current item being processed.
            If None, then the root element is taken.
        :param restore_dataset: Restore the dataset of the selected item?
        :param progress: Display progress dialog when updating?
        :return: True/False.
        """
        result = False
        try:
            if progress:
                if item is None:
                    item = self.GetRootItem()
                children_count = self.getTreeCtrlItemChildrenCount(treectrl=self, item=item)
                dlg_func.openProgressDlg(parent=self,
                                         title=u'INDICATORS',
                                         prompt_text=u'Refresh indicators...',
                                         min_value=0, max_value=children_count)
            # First, remember the selected item
            cur_item = self.GetSelection()
            # Updating all indicators
            result = self._refreshIndicators(visible_items, item=item, progress=progress)

            if restore_dataset:
                # After updating the indicators,
                # you need to restore the record set of the selected item
                cur_filter = self.buildItemFilter(item=cur_item)
                self.getCurRecords(item_filter=cur_filter)
        except:
            log_func.fatal(u'Error updating indicators of the filter tree')
        if progress:
            dlg_func.closeProgressDlg()
        return result

    def _refreshIndicators(self, visible_items=True, item=None, progress=False):
        """
        Refresh indicators of tree elements.

        :param visible_items: Refresh indicators of visible tree elements?
            If not, then the indicators of all elements are updated.
        :param item: The current item being processed.
            If None, then the root element is taken.
        :param progress: Display progress dialog when updating?
        :return: True/False.
        """
        if item is None:
            item = self.GetRootItem()

        item_indicator = self.getItemIndicator(item=item)
        if item_indicator:
            if visible_items:
                if self.IsVisible(item):
                    self._refreshIndicator(item_indicator, item=item)
                else:
                    # If we process only visible elements,
                    # and the current element is not visible,
                    # then there is no need to process child elements
                    return True
            else:
                self._refreshIndicator(item_indicator, item=item)

        # Handling child elements
        if self.IsExpanded(item):
            children = self.getTreeCtrlItemChildren(treectrl=self, item=item)
            for child in children:
                self._refreshIndicators(visible_items, item=child)
                if progress:
                    label = self.GetItemText(child)
                    dlg_func.stepProgressDlg(new_prompt_text=u'Refresh indicator ... %s' % label)

        return True

    def refreshIndicator(self, indicator, item=None):
        """
        Refresh the indicator of the tree element.

        :param indicator: Indicator data.
        :param item: The current item being processed.
            If None, then the root element is taken.
        :return: True/False.
        """
        try:
            return self._refreshIndicator(indicator=indicator, item=item)
        except:
            log_func.fatal(u'Error updating tree element indicator')
        return False

    def _refreshIndicator(self, indicator, item=None):
        """
        Refresh the indicator of the tree element.

        :param indicator: Indicator data.
        :param item: The current item being processed.
            If None, then the root element is taken.
        :return: True/False.
        """
        if not indicator:
            # Indicator not defined. No need to update
            return False

        if item is None:
            item = self.GetRootItem()

        # First, we get the node recordset corresponding to the element
        # ATTENTION! Indicators are updated by the full filter of the item
        cur_filter = self.buildItemFilter(item=item)
        records = self.getCurRecords(item_filter=cur_filter)

        # Then we get the indicator objects
        name, bmp, txt_colour, bg_colour = self.getStateIndicatorObjects(records=records, indicator=indicator)

        # Setting item parameters
        if bmp:
            # self.setItemImage_tree_ctrl(ctrl=self, item=item, image=bmp)
            self.setTreeCtrlItemImage(treectrl=self, item=item, image=bmp)

        if txt_colour:
            # self.setItemForegroundColour(ctrl=self, item=item, colour=txt_colour)
            self.setTreeCtrlItemForegroundColour(treectrl=self, item=item, colour=txt_colour)
        if bg_colour:
            # self.setItemBackgroundColour(ctrl=self, item=item, colour=bg_colour)
            self.setTreeCtrlItemBackgroundColour(treectrl=self, item=item, colour=bg_colour)

        return True

    def onItemExpanded(self, event):
        """
        A handler for expanding a tree item.
        """
        # ATTENTION! Display child elements only if the control is fully initialized
        if self._init_flag:
            item = event.GetItem()
            self.refreshIndicators(item=item, progress=True)

        event.Skip()
