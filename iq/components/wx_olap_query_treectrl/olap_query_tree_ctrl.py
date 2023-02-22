#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP cubes query tree control.
"""

import copy
import os.path
import wx
import wx.gizmos
from wx.lib.agw import flatmenu

from ...util import log_func
from ...util import file_func
from ...util import lang_func
from ...dialog import dlg_func

from ...engine.wx import wxbitmap_func
from ...engine.wx import treectrl_manager
from ...engine import stored_manager

from ..wx_filtertreectrl import tree_item_indicator
from . import edit_cubes_pivot_table_request_dlg

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

DEFAULT_ROOT_LABEL = u'...'
DEFAULT_NODE_LABEL = _(u'New node')
DEFAULT_NODE_IMAGE_FILENAME = 'table.png'

# An empty entry attached to a node
EMPTY_NODE_RECORD = {'__request__': None, '__indicator__': None, 'label': u''}


class iqOLAPQueryTreeCtrlProto(wx.TreeCtrl,
                               tree_item_indicator.iqTreeItemIndicator,
                               treectrl_manager.iqTreeCtrlManager,
                               stored_manager.iqStoredManager):
    """
    OLAP cubes query tree control prototype class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.TreeCtrl.__init__(self, *args, **kwargs)

        tree_item_indicator.iqTreeItemIndicator.__init__(self)

        # By default, we create the root element
        self.AddRoot(DEFAULT_ROOT_LABEL)
        root_data = copy.deepcopy(EMPTY_NODE_RECORD)
        root_data['label'] = DEFAULT_ROOT_LABEL
        self.setTreeCtrlItemData(treectrl=self, data=root_data)

        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onItemRightClick)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onItemDoubleClick)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onItemSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onItemExpanded)

        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

        # OLAP server
        self._OLAP_server = None

        # self._uuid = None

        # Name of the query tree storage file
        self._save_filename = None

        # Current query of the selected item
        self._cur_item_request = None

    def setOLAPServer(self, olap_server):
        """
        Set OLAP server.

        :param olap_server: OLAP server object.
        """
        self._OLAP_server = olap_server

    def getOLAPServer(self):
        """
        Get OLAP server object.
        """
        return self._OLAP_server

    def _canEditOLAPRequest(self):
        return True

    def onDestroy(self, event):
        """
        If you need to remove / release
        resources when deleting a control, then you need to use
        event wx.EVT_WINDOW_DESTROY.
        """
        self.saveRequests()
        event.Skip()

    def getCurItemRequest(self):
        """
        Get current query.
        """
        if self._cur_item_request is None:
            # Full request is not defined
            # We believe that this is a request for the root element
            self._cur_item_request = self.getItemRequest()
        return self._cur_item_request

    def getItemRequest(self, item=None):
        """
        The request attached to the item.

        :param item: Current item.
            If None, then the root element is taken.
        :return: The structure of the request, or None if the request is not defined.
        """
        if item is None:
            item = self.GetRootItem()

        item_data = self.getTreeCtrlItemData(treectrl=self, item=item)
        return item_data.get('__request__', None) if item_data else None

    def getItemIndicator(self, item=None):
        """
        Indicator attached to an element.

        :param item: Current item.
            If None, then the root element is taken.
        :return: The structure of the indicator, or None if the request is not defined.
        """
        if item is None:
            item = self.GetRootItem()

        item_data = self.getTreeCtrlItemData(treectrl=self, item=item)
        return item_data.get('__indicator__', None) if item_data else None

    def onItemRightClick(self, event):
        """
        Right click handler.
        """
        menu = self.createPopupMenu()
        if menu:
            menu.Popup(wx.GetMousePosition(), self)
        # select_component_menu.popup_component_flatmenu(parent=self)
        event.Skip()

    def editRootRequest(self, root_item=None):
        """
        Editing the query of the root element.

        :param root_item: Root item.
            If not specified, then it is taken automatically.
        :return: True/False.
        """
        if root_item is None:
            root_item = self.GetRootItem()
        if not self.isTreeCtrlRootItem(treectrl=self, item=root_item):
            # If not the root element, then skip processing
            return False

        return self.editRequestItem(root_item)

    def onItemDoubleClick(self, event):
        """
        Handler for double-clicking on a tree element.
        """
        item = event.GetItem()
        self.editRootRequest(root_item=item)
        self.refreshRootItemTitle()

        # To update the list of objects
        self._cur_item_request = self.getItemRequest(item)
        self.onChange(event)

        # event.Skip()

    def onChange(self, event):
        """
        Смена запроса.
        """
        log_func.error(u'Method <onChange> not defined in <%s>' % self.__class__.__name__)

    def onItemSelectChanged(self, event):
        """
        Handler for changing the selection of a tree element.
        """
        item = event.GetItem()
        self._cur_item_request = self.getItemRequest(item)

        # Transfer processing to the component
        self.onChange(event)

        event.Skip()

    def createPopupMenu(self):
        """
        Create a pop-up menu for managing the query tree.

        :return: wx.Menu object.
        """
        try:
            cur_item = self.GetSelection()
            if not cur_item:
                log_func.warning(u'No tree item selected ')
                return None
            item_data = self.getTreeCtrlItemData(treectrl=self, item=cur_item)

            menu = flatmenu.FlatMenu()

            rename_menuitem_id = wx.NewId()
            bmp = wxbitmap_func.createIconBitmap('fatcow/textfield_rename')
            menuitem = flatmenu.FlatMenuItem(menu, rename_menuitem_id, _(u'Rename'),
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onRenameMenuItem, id=rename_menuitem_id)

            moveup_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, moveup_menuitem_id, _(u'Move up'),
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onMoveUpMenuItem, id=moveup_menuitem_id)
            menuitem.Enable(not self.isTreeCtrlFirstItem(treectrl=self, item=cur_item))

            movedown_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, movedown_menuitem_id, _(u'Move down'),
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onMoveDownMenuItem, id=movedown_menuitem_id)
            menuitem.Enable(not self.isTreeCtrlLastItem(treectrl=self, item=cur_item))

            menu.AppendSeparator()

            add_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, add_menuitem_id, _(u'Add'),
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onAddMenuItem, id=add_menuitem_id)
            menuitem.Enable(self._canEditOLAPRequest())

            del_menuitem_id = wx.NewId()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_MENU,
                                           (treectrl_manager.DEFAULT_ITEM_IMAGE_WIDTH,
                                            treectrl_manager.DEFAULT_ITEM_IMAGE_HEIGHT))
            menuitem = flatmenu.FlatMenuItem(menu, del_menuitem_id, _(u'Delete'),
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onDelMenuItem, id=del_menuitem_id)
            menuitem.Enable(self._canEditOLAPRequest())

            request_menuitem_id = wx.NewId()
            bmp = wxbitmap_func.createIconBitmap('fatcow/table_lightning')
            # cur_request = item_data.get('__request__', None) if item_data else None
            label = u'%s: %s' % (_(u'Query'),
                                 item_data.get('label', DEFAULT_ROOT_LABEL) if item_data else _(u'Query'))
            menuitem = flatmenu.FlatMenuItem(menu, request_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onRequestMenuItem, id=request_menuitem_id)
            menuitem.Enable(self._canEditOLAPRequest())

            indicator_menuitem_id = wx.NewId()
            bmp = wxbitmap_func.createIconBitmap('fugue/traffic-light')
            cur_indicator = item_data.get('__indicator__', None) if item_data else None
            label = u'%s: %s' % (_(u'Indicator'),
                                 self.getLabelIndicator(cur_indicator) if cur_indicator else _(u'Indicator'))
            menuitem = flatmenu.FlatMenuItem(menu, indicator_menuitem_id, label,
                                             normalBmp=bmp)
            menu.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.onIndicatorMenuItem, id=indicator_menuitem_id)
            menuitem.Enable(self._canEditOLAPRequest())

            return menu
        except:
            log_func.fatal(u'Error creating menu for managing query tree')
        return None

    def renameItem(self, cur_item=None):
        """
        Rename node.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            if cur_item:
                cur_label = self.GetItemText(cur_item)
                label = dlg_func.getTextEntryDlg(self, _(u'RENAME'), _(u'New name'),
                                                 cur_label)

                if label:
                    bmp = None
                    # bmp = ic_bmp.createLibraryBitmap(DEFAULT_NODE_IMAGE_FILENAME)
                    data_record = self.getTreeCtrlItemData(treectrl=self, item=cur_item)
                    data_record['label'] = label
                    self.SetItemText(cur_item, label)
                    return self.setTreeCtrlItemData(treectrl=self, item=cur_item, data=data_record)
            else:
                log_func.warning(u'The current tree element is not defined')
        except:
            log_func.fatal(u'Rename node error')
        return False

    def onRenameMenuItem(self, event):
        """
        Rename node. Handler.
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
        Move the node down the list.

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

    def addRequestItem(self, cur_item=None):
        """
        Add OLAP query.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            if cur_item:
                label = dlg_func.getTextEntryDlg(self, _(u'ADD'), _(u'New name'),
                                                 DEFAULT_NODE_LABEL)

                if label:
                    bmp = None
                    # bmp = ic_bmp.createLibraryBitmap(DEFAULT_NODE_IMAGE_FILENAME)
                    data_record = copy.deepcopy(EMPTY_NODE_RECORD)
                    data_record['label'] = label
                    new_item = self.appendTreeCtrlChildItem(treectrl=self, parent_item=cur_item, label=label,
                                                            image=bmp, data=data_record, select=True)
                    return True
            else:
                log_func.warning(u'The current tree element is not defined')
        except:
            log_func.fatal(u'Error adding request')
        return False

    def onAddMenuItem(self, event):
        """
        Add request. Handler.
        """
        self.addRequestItem()
        # event.Skip()

    def delRequestItem(self, cur_item=None):
        """
        Delete request.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()

            return self.deleteTreeCtrlItem(treectrl=self, item=cur_item, ask=True)
        except:
            log_func.fatal(u'Error deleting request')
        return False

    def onDelMenuItem(self, event):
        """
        Delete request. Handler.
        """
        self.delRequestItem()
        # event.Skip()

    def editRequestItem(self, cur_item=None):
        """
        Edit request.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
            item_data = self.getTreeCtrlItemData(treectrl=self, item=cur_item)
            cur_request = item_data.get('__request__', None)
            cur_request = edit_cubes_pivot_table_request_dlg.editCubesPivotTableRequestDlg(parent=self,
                                                                                           olap_srv=self.getOLAPServer(),
                                                                                           olap_srv_request=cur_request)
            if cur_request:
                item_data['__request__'] = cur_request
                return True
        except:
            log_func.fatal(u'Error edit request')
        return False

    def refreshRootItemTitle(self):
        """
        Update the label of the root element according to the selected query.

        :return: True/False.
        """
        item = self.GetRootItem()
        item_data = self.getTreeCtrlItemData(treectrl=self, item=item)
        label = item_data.get('label', None)
        if not label:
            label = DEFAULT_ROOT_LABEL
        self.setTreeCtrlRootTitle(treectrl=self, title=label)
        return True

    def onRequestMenuItem(self, event):
        """
        Customize your request. Handler.
        """
        self.editRequestItem()

        # After editing the request, if it is a root element,
        # then change the label of the root element
        cur_item = self.GetSelection()
        if self.isTreeCtrlRootItem(treectrl=self, item=cur_item):
            self.refreshRootItemTitle()

        # To update the list of objects
        self._cur_item_filter = self.getItemRequest(cur_item)
        self.onChange(event)

        # event.Skip()

    def editRequestIndicatorItem(self, cur_item=None):
        """
        Edit indicator.

        :return: True/False.
        """
        try:
            if cur_item is None:
                cur_item = self.GetSelection()
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
        self.editRequestIndicatorItem()
        # event.Skip()

    def saveRequests(self, save_filename=None):
        """
        Save request details to a file.

        :param save_filename: The name of the query tree storage file.
            If not specified, then generated by GUID.
        :return:
        """
        if save_filename is None:
            save_filename = self._save_filename

        if save_filename:
            save_filename = os.path.normpath(save_filename)
        else:
            widget_guid = self.getGUID()
            save_filename = os.path.join(file_func.getProjectProfilePath(),
                                         widget_guid + '.dat')

        request_tree_data = self.getTreeCtrlData(treectrl=self)
        return self.saveCustomData(save_filename=save_filename, save_data=request_tree_data)

    def loadRequests(self, save_filename=None):
        """
        Load request data.

        :param save_filename: The name of the query tree storage file.
            If not specified, then generated by GUID.
        """
        if save_filename is None:
            save_filename = self._save_filename

        if save_filename:
            save_filename = os.path.normpath(save_filename)
        else:
            widget_guid = self.getGUID()
            print(widget_guid, type(widget_guid))
            save_filename = os.path.join(file_func.getProjectProfilePath(),
                                         widget_guid + '.dat')

        request_tree_data = self.loadCustomData(save_filename=save_filename)
        # Build
        result = self.setTreeCtrlData(treectrl=self, tree_data=request_tree_data, label='label')

        # Set root item label as query label
        if request_tree_data is None:
            request_tree_data = copy.deepcopy(EMPTY_NODE_RECORD)
        str_request = request_tree_data.get('label', DEFAULT_ROOT_LABEL)
        root_label = str_request if str_request else DEFAULT_ROOT_LABEL
        self.setTreeCtrlRootTitle(treectrl=self, title=root_label)

        return result

    def refreshIndicators(self, visible_items=True, item=None):
        """
        Refresh indicators of tree elements.
        
        :param visible_items: Refresh indicators of visible tree elements?
            If not, then the indicators of all elements are refreshed.
        :param item: Current item.
            If is None, then root item taken.
        :return: True/False.
        """
        try:
            return self._refreshIndicators(visible_items, item=item)
        except:
            log_func.fatal(u'Error updating query tree indicators')
        return False

    def _refreshIndicators(self, visible_items=True, item=None):
        """
        Refresh indicators of tree elements.

        :param visible_items: Refresh indicators of visible tree elements?
            If not, then the indicators of all elements are refreshed.
        :param item: Current item.
            If is None, then root item taken.
        :return: True/False.
        """
        if item is None:
            item = self.GetRootItem()

        item_indicator = self.getItemIndicator(item=item)
        if item_indicator:
            if visible_items:
                if self.IsVisible(item):
                    self.refreshIndicator(item_indicator, item=item)
                else:
                    # If we process only visible elements and the current element is not visible,
                    # then there is no need to process child elements
                    return True
            else:
                self.refreshIndicator(item_indicator, item=item)

        # Handling child elements
        if self.IsExpanded(item):
            children = self.getTreeCtrlItemChildren(treectrl=self, item=item)
            for child in children:
                self._refreshIndicators(visible_items, item=child)

        return True

    def refreshIndicator(self, indicator, item=None):
        """
        Refresh the indicator of the tree element.

        :param indicator: Indicator description structure.
        :param item: Current item.
            If is None, then root item taken.
        :return: True/False.
        """
        try:
            return self._refreshIndicator(indicator=indicator, item=item)
        except:
            log_func.fatal(u'Error refreshing the tree element indicator')
        return False

    def _refreshIndicator(self, indicator, item=None):
        """
        Refresh the indicator of the tree element.

        :param indicator: Indicator description structure.
        :param item: Current item.
            If is None, then root item taken.
        :return: True/False.
        """
        if not indicator:
            # Indicator not defined. No need to refresh
            return False

        if item is None:
            item = self.GetRootItem()

        # First, we get the node recordset corresponding to the element
        cur_request = self.getItemRequest(item=item)
        records = self.getCurRecords(item_filter=cur_request)

        # Then we get the indicator objects
        name, bmp, txt_colour, bg_colour = self.getStateIndicatorObjects(records=records, indicator=indicator)

        # Setting the parameters of the element
        if bmp:
            self.setTreeCtrlItemImage(treectrl=self, item=item, image=bmp)

        if txt_colour:
            self.setTreeCtrlItemForegroundColour(treectrl=self, item=item, colour=txt_colour)
        if bg_colour:
            self.setTreeCtrlItemBackgroundColour(treectrl=self, item=item, colour=bg_colour)

        return True

    def onItemExpanded(self, event):
        """
        A handler for expanding a tree item.
        """
        item = event.GetItem()
        self.refreshIndicators(item=item)
