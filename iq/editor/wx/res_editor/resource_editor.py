#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource editor class module.
"""

import sys
import wx

try:
    from . import resource_editor_frm
except:
    import resource_editor_frm

from ....util import log_func
from ....util import res_func
from ....util import spc_func
from ....util import global_func
from ....engine.wx import wxbitmap_func
from ....import components
from .... import project

from . import property_editor_manager

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

        self.component_imagelist = None
        self.component_icons = dict()

    def initComponentIcons(self):
        """
        Initialization component icon image list object.

        :return:
        """
        self.component_imagelist = wx.ImageList(wxbitmap_func.DEFAULT_ICON_WIDTH,
                                                wxbitmap_func.DEFAULT_ICON_HEIGHT)
        component_spc_cache = components.getComponentSpcCache()

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
        if component_type == project.PROJECT_COMPONENT_TYPE:
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
                        selected_item = self.resource_treeListCtrl.GetMainWindow().GetSelection()

                        if name in ('name', 'description'):
                            self.refreshResourceItem(selected_item,
                                                     selected_resource.get('name', 'unknown'),
                                                     selected_resource.get('description', ''))
                    else:
                        log_func.error(u'Value <%s> of property [%s] not valid' % (str_value, name))

        # event.Skip()

    def onSaveAsToolClicked(self, event):
        """
        Save tool button click handler.
        """

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
        resource = res_func.loadResourceText(res_filename)
        resource = spc_func.fillResourceBySpc(resource=resource)
        frame.loadResource(resource)
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
