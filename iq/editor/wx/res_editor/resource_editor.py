#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource editor class module.
"""

import sys
import os.path
import wx
from wx.lib.agw import flatmenu

try:
    from . import resource_editor_frm
except:
    import resource_editor_frm

from ....util import log_func
from ....util import res_func
from ....util import spc_func
from ....util import global_func
from ....util import file_func
from ....util import exec_func
from ....engine.wx import wxbitmap_func
from ....engine.wx.dlg import wxdlg_func
from ....import components
from .... import project
from .. import clipboard

from . import property_editor_manager
from . import select_component_menu
from . import new_resource_dialog

__version__ = (0, 0, 0, 1)


class iqResourceEditor(resource_editor_frm.iqResourceEditorFrameProto,
                       property_editor_manager.iqPropertyEditorManager):
    """
    Resource editor class.
    """
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent window object.
        """
        resource_editor_frm.iqResourceEditorFrameProto.__init__(self, parent=parent)

        self.res_filename = None

        self.component_imagelist = None
        self.component_icons = dict()

        self.item_context_menu = None

    def initComponentIcons(self):
        """
        Initialization component icon image list object.

        :return:
        """
        self.component_imagelist = wx.ImageList(wxbitmap_func.DEFAULT_ICON_WIDTH,
                                                wxbitmap_func.DEFAULT_ICON_HEIGHT)
        component_spc_cache = components.getComponentSpcPalette()

        if component_spc_cache:
            for package in list(component_spc_cache.keys()):
                pkg_components = component_spc_cache[package]
                for component_spc in pkg_components:
                    component_type = component_spc.get('type', None)
                    if component_type:
                        icon_name = component_spc.get('__icon__', None)
                        if icon_name:
                            # log_func.debug(u'Create icon <%s>' % icon_name)
                            component_icon_bmp = wxbitmap_func.createIconBitmap(icon_name)
                            if component_icon_bmp:
                                component_icon_idx = self.component_imagelist.Add(component_icon_bmp)
                                self.component_icons[component_type] = component_icon_idx
                            else:
                                log_func.warning(u'Not valid icon name component <%s>' % component_type)
                        else:
                            log_func.warning(u'Component <%s> specification not define icon' % component_type)
                            log_func.warning(u'Verify __icon__ attribute in specification')
                    else:
                        log_func.error(u'In specification %s not define type' % component_spc)

            self.resource_treeListCtrl.SetImageList(self.component_imagelist)
        else:
            log_func.error(u'Empty component specification cache <%s>' % str(component_spc_cache))

    def init(self):
        """
        Initialization frame controls.

        :return:
        """
        self.initComponentIcons()

        # self.clearProperties(self.object_propertyGridManager)

    def _loadResource(self, resource, parent_item=None):
        """
        Load resource in editor.

        :param resource: Resource struct.
        :param parent_item: Parent item for append resource.
            If None then append root item.
        :return: True/False.
        """
        name = resource.get('name', u'Unknown')
        component_type = resource.get('type', None)
        if component_type == project.COMPONENT_TYPE:
            global_func.setProjectName(name)

        description = resource.get('description', u'')
        icon_idx = self.component_icons.get(component_type, None)
        log_func.debug(u'Add new resource item <%s : %s : %s : %s>' % (component_type, name, description, icon_idx))

        if parent_item is None:
            new_item = self.resource_treeListCtrl.AddRoot(name)
        else:
            new_item = self.resource_treeListCtrl.AppendItem(parent_item, name)
        self.resource_treeListCtrl.SetItemText(new_item, description, 1)
        if icon_idx is not None:
            self.resource_treeListCtrl.SetItemImage(new_item, icon_idx, which=wx.TreeItemIcon_Normal)
        self.resource_treeListCtrl.GetMainWindow().SetItemData(new_item, resource)

        result = list()
        children = resource.get(spc_func.CHILDREN_ATTR_NAME, list())
        for child_resource in children:
            result.append(self._loadResource(child_resource, new_item))

        return all(result)

    def loadResource(self, resource):
        """
        Load resource in editor.

        :param resource: Resource struct.
        :return: True/False.
        """
        if resource is None:
            log_func.error(u'Resource editor. Not define resource for loading')
            return False

        try:
            self.resource_treeListCtrl.DeleteAllItems()

            result = self._loadResource(resource)

            root_tem = self.resource_treeListCtrl.GetRootItem()
            if root_tem and root_tem.IsOk():
                self.resource_treeListCtrl.Expand(root_tem)
                resource = self.resource_treeListCtrl.GetMainWindow().GetItemData(root_tem)
                self.buildPropertyEditors(property_editor=self.object_propertyGridManager, resource=resource)
            return result
        except:
            log_func.fatal(u'Load resource in editor error')
        return False

    def loadResourceFile(self, res_filename):
        """
        Load resource from resource.

        :param res_filename: Resource filename.
        :return: True/False
        """
        self.res_filename = res_filename
        resource = res_func.loadResourceText(res_filename)
        resource = spc_func.fillResourceBySpc(resource=resource)
        return self.loadResource(resource)

    def onResItemTreelistSelectionChanged(self, event):
        """
        Resource tree list control item selection changes handler.
        """
        try:
            item = event.GetItem()
            resource = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
            self.buildPropertyEditors(property_editor=self.object_propertyGridManager, resource=resource)
        except:
            log_func.fatal(u'Resource tree list control item selection changes handler error')
        event.Skip()

    def getSelectedResource(self):
        """
        Get selected object resource.

        :return: Object resource or None if not selected.
        """
        resource = None
        selected_item = self.resource_treeListCtrl.GetMainWindow().GetSelection()
        if selected_item and selected_item.IsOk():
            resource = self.resource_treeListCtrl.GetMainWindow().GetItemData(selected_item)
        return resource

    def refreshResourceItem(self, item=None, name='unknown', description=''):
        """
        Refresh resource tree item.

        :param item: Tree item.
        :param name: Name.
        :param description: Description.
        :return: True/False.
        """
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetRootItem()

        if item and item.IsOk():
            self.resource_treeListCtrl.GetMainWindow().SetItemText(item, name, 0)
            self.resource_treeListCtrl.GetMainWindow().SetItemText(item, description, 1)

    def getResourceItem(self, item=None):
        """
        Get resource from editor.

        :param item: Current item of resource tree control.
            If None then get root item.
        :return: Resource dictionary.
        """
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetRootItem()

        resource = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
        if self.resource_treeListCtrl.GetMainWindow().HasChildren(item):
            resource[spc_func.CHILDREN_ATTR_NAME] = list()
            child_item, cookie = self.resource_treeListCtrl.GetMainWindow().GetFirstChild()
            while child_item and child_item.IsOk():
                child_resource = self.getResourceItem(child_item)
                resource[spc_func.CHILDREN_ATTR_NAME].append(child_resource)
                child_item, cookie = self.resource_treeListCtrl.GetMainWindow().GetNextChild(child_item, cookie=cookie)
        return resource

    def getPropertyEditor(self, attribute_name):
        """
        Get attribute/property editor by attribute name.

        :param attribute_name: Attribute name.
        :return: Property editor or None if not found.
        """
        return self.object_propertyGridManager.GetPropertyEditor(attribute_name)

    def getProperty(self, attribute_name):
        """
        Get attribute/property by attribute name.

        :param attribute_name: Attribute name.
        :return: Property editor or None if not found.
        """
        return self.object_propertyGridManager.GetProperty(attribute_name)

    def onObjPropertyGridChanged(self, event):
        """
        Changed attribute value in property grid handler.
        """
        wx_property = event.GetProperty()
        if wx_property:
            name = wx_property.GetName()
            str_value = wx_property.GetValueAsString()
            log_func.info(u'Property [%s]. New value <%s>' % (name, str_value))

            selected_resource = self.getSelectedResource()
            if selected_resource:
                selected_component_type = selected_resource.get('type', None)
                if selected_component_type:
                    spc = components.findComponentSpc(selected_component_type)
                    spc = spc_func.fillSpcByParent(spc)
                    value = self.convertPropertyValue(name, str_value, spc)
                    if self.validatePropertyValue(name, value, spc):
                        selected_resource[name] = value

                        try:
                            on_change = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('on_change', None)
                            if on_change:
                                on_change(resource_editor=self, resource=selected_resource)
                        except:
                            log_func.fatal(u'Change attribute <%s> error' % name)

                        selected_item = self.resource_treeListCtrl.GetMainWindow().GetSelection()

                        if name in ('name', 'description'):
                            self.refreshResourceItem(selected_item,
                                                     selected_resource.get('name', 'unknown'),
                                                     selected_resource.get('description', ''))
                    else:
                        log_func.error(u'Value <%s> of property [%s] not valid' % (str_value, name))

        # event.Skip()

    def onNewToolClicked(self, event):
        """
        New resoure tool button click handler.
        """
        res_filename = new_resource_dialog.createNewResource(parent=self)
        if res_filename is not None:
            self.loadResourceFile(res_filename
                                  )
        event.Skip()

    def onSaveToolClicked(self, event):
        """
        Save tool button click handler.
        """
        resource = self.getResourceItem()
        resource = spc_func.clearResourceFromSpc(resource)
        if self.res_filename is None:
            self.res_filename = wxdlg_func.getFileDlg(parent=self, title=u'SAVE',
                                                      wildcard_filter='Resource files (*.res)|*.res')
        if self.res_filename:
            res_func.saveResourceText(self.res_filename, resource_data=resource)
        else:
            log_func.warning(u'Not define resource filename')

        event.Skip()

    def onSaveAsToolClicked(self, event):
        """
        Save As... tool button click handler.
        """
        resource = self.getResourceItem()
        resource = spc_func.clearResourceFromSpc(resource)
        self.res_filename = wxdlg_func.getFileDlg(parent=self, title=u'SAVE',
                                                  wildcard_filter='Resource files (*.res)|*.res')
        if self.res_filename:
            res_func.saveResourceText(self.res_filename, resource_data=resource)
        else:
            log_func.warning(u'Not define resource filename')

        event.Skip()

    def onOpenToolClicked(self, event):
        """
        Open tool button click handler.
        """
        res_filename = wxdlg_func.getFileDlg(parent=self, title=u'LOAD',
                                             wildcard_filter='Resource files (*.res)|*.res')

        if res_filename:
            self.loadResourceFile(res_filename)
        else:
            log_func.warning(u'Not define resource filename')

        event.Skip()

    def onTestToolClicked(self, event):
        """
        Test tool button click handler.
        """
        item_resource = self.getSelectedResource()

        test_func = item_resource.get(spc_func.TEST_FUNC_ATTR_NAME, None)
        if test_func:
            test_func(item_resource)
        else:
            log_func.warning(u'Not define TEST function for <%s>' % item_resource.get('type', None))

        event.Skip()

    def onDesignToolClicked(self, event):
        """
        Design tool button click handler.
        """
        item_resource = self.getSelectedResource()

        design_func = item_resource.get(spc_func.DESIGN_FUNC_ATTR_NAME, None)
        if design_func:
            design_func(item_resource)
        else:
            log_func.warning(u'Not define DESIGN function for <%s>' % item_resource.get('type', None))

        event.Skip()

    def onHelpToolClicked(self, event):
        """
        Help tool button click handler.
        """
        item_resource = self.getSelectedResource()

        doc_filename = item_resource.get(spc_func.DOC_ATTR_NAME, None)
        if doc_filename:
            doc_filename = os.path.join(file_func.getFrameworkPath(), doc_filename)
            exec_func.openHtmlBrowser(doc_filename)
        else:
            log_func.warning(u'Not define DOC filename for <%s>' % item_resource.get('type', None))

        event.Skip()

    def onResTreelistItemContextMenu(self, event):
        """
        Resource item context menu handler.
        """
        try:
            self.item_context_menu = self.createResourceItemContextMenu()

            parent_pos = self.resource_treeListCtrl.GetMainWindow().GetScreenPosition()
            event_point = event.GetPoint()
            popup_pos = wx.Point(parent_pos.x + event_point.x,
                                 parent_pos.y + event_point.y)
            self.item_context_menu.Popup(popup_pos, self.resource_treeListCtrl)
        except:
            log_func.fatal(u'Popup resource item context menu error')

        event.Skip()

    def createResourceItemContextMenu(self, item=None):
        """
        Create item context menu.

        :param item: Resource tree item.
            If None then get selected item.
        :return: wx.FlatMenu object or None if error.
        """
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetSelection()

        if item and item.IsOk():
            resource_item = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
            context_menu = flatmenu.FlatMenu()
            component_menu = select_component_menu.iqSelectComponentFlatMenu()
            component_menu.init(parent=self.resource_treeListCtrl,
                                parent_component=resource_item)
            component_menu.create(menuitem_handler=self.onSelectComponentMenuItem)
            context_menu.AppendMenu(wx.NewId(), 'Add', component_menu)

            context_menu.AppendSeparator()

            menuitem_id = wx.NewId()
            menuitem = flatmenu.FlatMenuItem(context_menu, menuitem_id, label='Copy',
                                             normalBmp=wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_MENU))
            context_menu.AppendItem(menuitem)

            menuitem_id = wx.NewId()
            menuitem = flatmenu.FlatMenuItem(context_menu, menuitem_id, label='Paste',
                                             normalBmp=wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_MENU))
            context_menu.AppendItem(menuitem)

            menuitem_id = wx.NewId()
            menuitem = flatmenu.FlatMenuItem(context_menu, menuitem_id, label='Cut',
                                             normalBmp=wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_MENU))
            context_menu.AppendItem(menuitem)

            return context_menu
        return None

    def onSelectComponentMenuItem(self, event):
        """
        Select component menu item handler.
        """
        if self.item_context_menu:
            menuitem_id = event.GetId()
            selected_component = self.item_context_menu.menuitem2component_spc.get(menuitem_id, None)
            component_type = selected_component.get('type', 'UndefinedType')
            log_func.info(u'Selected component <%s>' % component_type)

            self.item_context_menu = None
        event.Skip()

    def copyResourceItem(self, item=None):
        """
        Copy resource.

        :param item: Resource tree item.
            If None then get selected item.
        :return: New copy resource struct or None if error.
        """
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetSelection()
        resource_item = None
        if item and item.IsOk():
            resource_item = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
            resource_item['name'] = resource_item.get('name', 'default') + str(wx.NewId())
            clipboard.toClipboard(resource_item)
        return resource_item

    def pasteResourceItem(self, item=None):
        """
        Paste resource in item.

        :param item: Resource tree item.
            If None then get selected item.
        :return: True/False.
        """
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetSelection()
        if item and item.IsOk():
            resource_item = clipboard.fromClipboard()
            component_type = resource_item.get('type', None)
            item_spc = self.resource_treeListCtrl.GetMainWindow().GetItemData()
            item_type = item_spc.get('type', 'Unknown')
            item_content = item_spc.get(spc_func.CONTENT_ATTR_NAME, list())
            if component_type in item_content:
                self._loadResource(resource_item, item)
                return True
            else:
                msg = u'Unable to add component <%s> to <%s>' % (component_type, item_type)
                log_func.warning(msg)
                wxdlg_func.openWarningBox(u'PASTE', msg)
        return False

    def cutResourceItem(self, item=None):
        """
        Cut resource.

        :param item: Resource tree item.
            If None then get selected item.
        :return: New copy resource struct or None if error.
        """
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetSelection()
        if item and item.IsOk():
            resource_item = self.resource_treeListCtrl.GetMainWindow().GetItemData()
            clipboard.toClipboard(resource_item)
            self.resource_treeListCtrl.GetMainWindow().Delete(item)
            return resource_item
        return None

    def onCopyResourceMenuitem(self, event):
        """
        Copy item resource to clipboard handler.
        """
        self.copyResourceItem()
        event.Skip()

    def onPasteResourceMenuitem(self, event):
        """
        Past resource from clipboard to item as child handler.
        """
        self.pasteResourceItem()
        event.Skip()

    def onCutResourceMenuitem(self, event):
        """
        Cut selected item to clipboard handler.
        """
        self.cutResourceItem()
        event.Skip()


def openResourceEditor(parent=None, res_filename=None):
    """
    Open resource editor frame.

    :param res_filename: Resource file name.
    :return: True/False.
    """
    log_func.info(u'Open resource editor. Resource file <%s>' % res_filename)
    frame = None
    try:
        frame = iqResourceEditor(parent=parent)
        frame.init()
        if res_filename:
            frame.loadResourceFile(res_filename)
        frame.Show()
        return True
    except:
        if frame:
            frame.Destroy()
        log_func.fatal(u'Open resource editor error')
    return False


def runResourceEditor(res_filename=None):
    """
    Run resource editor.

    :param res_filename: Resource file name.
    :return: True/False.
    """
    app = wx.App()
    openResourceEditor(res_filename=res_filename)
    app.MainLoop()


if __name__ == '__main__':
    runResourceEditor(res_filename=sys.argv[1] if len(sys.argv) > 1 else None)
