#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource editor class module.
"""

import sys
import os.path
import copy
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
from ....util import lang_func

from ....engine.wx import wxbitmap_func
from ....engine.wx import imglib_manager
from ....engine.wx.dlg import wxdlg_func
from ....import components
from .... import project
from .. import clipboard

from . import property_editor_manager
from . import select_component_menu
from . import new_resource_dialog

from ....engine.wx import stored_wx_form_manager
from ....engine.wx import splitter_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqResourceEditor(resource_editor_frm.iqResourceEditorFrameProto,
                       property_editor_manager.iqPropertyEditorManager,
                       imglib_manager.iqImageLibManager,
                       stored_wx_form_manager.iqStoredWxFormsManager,
                       splitter_manager.iqSplitterWindowManager):
    """
    Resource editor class.
    """
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent window object.
        """
        resource_editor_frm.iqResourceEditorFrameProto.__init__(self, parent=parent)
        # the one with the tree in it...
        # self.resource_treeListCtrl.GetMainWindow().SetMainColumn(0)

        bmp = wxbitmap_func.createIconBitmap('fatcow/plugin_edit')
        if bmp:
            self.SetIcon(icon=wx.Icon(bmp))

        self.initImageLib()

        self.res_filename = None

        self.component_icons = dict()

        self.item_context_menu = None
        self.component_menu = None

        save_filename = os.path.join(file_func.getProfilePath(),
                                     self.getClassName() + res_func.PICKLE_RESOURCE_FILE_EXT)
        self.loadCustomProperties(save_filename)

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        """
        Close frame handler.
        """
        save_filename = os.path.join(file_func.getProfilePath(),
                                     self.getClassName() + res_func.PICKLE_RESOURCE_FILE_EXT)
        self.saveCustomProperties(save_filename)
        event.Skip()

    def initComponentIcons(self):
        """
        Initialization component icon image list object.

        :return:
        """
        self.component_icons[None] = self.getImageLibImageIdx(None)

        component_spc_cache = components.getComponentSpcPalette()

        if component_spc_cache:
            for package in list(component_spc_cache.keys()):
                pkg_components = component_spc_cache[package]
                for component_spc in pkg_components:
                    component_type = component_spc.get('type', None)
                    if component_type:
                        icon_name = component_spc.get('__icon__', None)
                        if icon_name:
                            component_icon_idx = self.getImageLibImageIdx(icon_name)
                            self.component_icons[component_type] = component_icon_idx
                            log_func.debug(u'Create icon <%s : %d>' % (icon_name, component_icon_idx))
                        else:
                            log_func.warning(u'Component <%s> specification not define icon' % component_type)
                            log_func.warning(u'Verify __icon__ attribute in specification')
                    else:
                        log_func.error(u'In specification %s not define type' % component_spc)

            self.resource_treeListCtrl.SetImageList(self.getImageLibImageList())
        else:
            log_func.error(u'Empty component specification cache <%s>' % str(component_spc_cache))

    def init(self):
        """
        Initialization frame controls.

        :return:
        """
        self.initImages()

        self.editor_toolBar.EnableTool(self.expand_tool.GetId(), False)

        self.initComponentIcons()
        self.registerCustomEditors(property_editor=self.object_propertyGridManager)

        # self.clearProperties(self.object_propertyGridManager)

    def initImages(self):
        """
        Init control images.
        """
        pass

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
        activate = resource.get('activate', True)
        icon_idx = self.component_icons.get(component_type, None)
        # log_func.debug(u'Add new resource item <%s : %s : %s : %s>' % (component_type, name, description, icon_idx))

        if parent_item is None:
            new_item = self.resource_treeListCtrl.AddRoot(name)
        else:
            new_item = self.resource_treeListCtrl.AppendItem(parent_item, name)
        self.resource_treeListCtrl.SetItemText(new_item, description, 1)
        if icon_idx is not None:
            self.resource_treeListCtrl.SetItemImage(new_item, icon_idx, which=wx.TreeItemIcon_Normal)
        self.resource_treeListCtrl.GetMainWindow().SetItemData(new_item, resource)
        active_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOXTEXT if activate else wx.SYS_COLOUR_GRAYTEXT)
        self.resource_treeListCtrl.GetMainWindow().SetItemTextColour(new_item, active_colour)

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
            log_func.fatal(u'Error load resource in editor')
        return False

    def loadResourceFile(self, res_filename):
        """
        Load resource from resource.

        :param res_filename: Resource filename.
        :return: True/False
        """
        self.res_filename = res_filename
        resource = res_func.loadResourceText(res_filename)
        resource = spc_func.fillAllResourcesBySpc(resource=resource)
        result = self.loadResource(resource)
        if result:
            title = _('Resource editor') + ' <%s>' % os.path.basename(self.res_filename)
            self.SetTitle(title)
        return result

    def onResItemTreelistSelectionChanged(self, event):
        """
        Resource tree list control item selection changes handler.
        """
        try:
            item = event.GetItem()
            resource = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
            self.buildPropertyEditors(property_editor=self.object_propertyGridManager, resource=resource)
        except:
            log_func.fatal(u'Error resource tree list control item selection changes handler')
        event.Skip()

    def getItemResource(self, item=None):
        """
        Get item object resource.

        :param item: Tree list control item.
            If None then get root item.
        :return: Object resource or None if error.
        """
        resource = None
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetRootItem()
        if item and item.IsOk():
            resource = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
        return resource

    def getSelectedResource(self):
        """
        Get selected object resource.

        :return: Object resource or None if not selected.
        """
        selected_item = self.resource_treeListCtrl.GetMainWindow().GetSelection()
        return self.getItemResource(item=selected_item)

    def refreshResourceItem(self, item=None, name='unknown', description='', activate=True):
        """
        Refresh resource tree item.

        :param item: Tree item.
        :param name: Name.
        :param description: Description.
        :param activate: Activity flag.
        :return: True/False.
        """
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetRootItem()

        if item and item.IsOk():
            self.resource_treeListCtrl.GetMainWindow().SetItemText(item, name, 0)
            self.resource_treeListCtrl.GetMainWindow().SetItemText(item, description, 1)
            active_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOXTEXT if activate else wx.SYS_COLOUR_GRAYTEXT)
            self.resource_treeListCtrl.GetMainWindow().SetItemTextColour(item, active_colour)

    def collectItemResource(self, item=None):
        """
        Collect item resource from editor.

        :param item: Current item of resource tree control.
            If None then get root item.
        :return: Resource dictionary.
        """
        resource = dict()
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetRootItem()

        try:
            resource = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
            if self.resource_treeListCtrl.GetMainWindow().HasChildren(item):
                resource[spc_func.CHILDREN_ATTR_NAME] = list()
                child_item, cookie = self.resource_treeListCtrl.GetMainWindow().GetFirstChild(item)
                while child_item and child_item.IsOk():
                    child_resource = self.collectItemResource(child_item)
                    resource[spc_func.CHILDREN_ATTR_NAME].append(child_resource)
                    child_item, cookie = self.resource_treeListCtrl.GetMainWindow().GetNextChild(item, cookie=cookie)
        except:
            log_func.fatal(u'Error get resource from editor')
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

            selected_resource = self.getSelectedResource()
            if selected_resource:
                selected_component_type = selected_resource.get('type', None)
                log_func.debug(u'Selected object type <%s>' % selected_component_type)
                if selected_component_type:
                    spc = components.findComponentSpc(selected_component_type)
                    spc = spc_func.fillSpcByParent(spc)

                    str_value = self.getPropertyValueAsString(wx_property, name, spc)
                    value = self.convertPropertyValue(name, str_value, spc)
                    if self.validatePropertyValue(name, value, spc):
                        selected_resource[name] = value

                        try:
                            editor = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict())
                            if isinstance(editor, dict):
                                on_change = editor.get('on_change', None)
                                if on_change:
                                    on_change(resource_editor=self, resource=selected_resource)
                        except:
                            log_func.fatal(u'Error change attribute <%s>' % name)

                        selected_item = self.resource_treeListCtrl.GetMainWindow().GetSelection()

                        if name in ('name', 'description', 'activate'):
                            self.refreshResourceItem(selected_item,
                                                     name=selected_resource.get('name', 'unknown'),
                                                     description=selected_resource.get('description', ''),
                                                     activate=selected_resource.get('activate', True))
                    else:
                        msg = u'Value <%s> of property [%s] is not valid' % (str_value, name)
                        log_func.error(msg)
                        wxdlg_func.openWarningBox(title=_(u'VALIDATE'),
                                                  prompt_text=msg, parent=self)
                        self.setPropertyValueAsString(wx_property, name, None, spc)
                        selected_resource[name] = None

        # event.Skip()

    def onNewToolClicked(self, event):
        """
        <New> resoure tool button click handler.
        """
        default_res_filename = os.path.join(os.path.dirname(self.res_filename), 'default' + res_func.RESOURCE_FILE_EXT)
        res_filename = new_resource_dialog.createNewResource(parent=self, res_filename=default_res_filename)
        if res_filename is not None:
            self.loadResourceFile(res_filename)
        event.Skip()

    def onSaveToolClicked(self, event):
        """
        <Save> tool button click handler.
        """
        resource = self.collectItemResource()
        resource = spc_func.clearAllResourcesFromSpc(resource)
        if self.res_filename is None:
            self.res_filename = wxdlg_func.getFileDlg(parent=self, title=u'SAVE',
                                                      wildcard_filter='Resource files (*.res)|*.res')
        if self.res_filename:
            result = res_func.saveResourceText(self.res_filename, resource_data=resource)
            if result:
                wxdlg_func.openMsgBox(title=u'EDITOR', prompt_text=u'Resource <%s> saving successful' % self.res_filename)
            else:
                wxdlg_func.openWarningBox(title=u'EDITOR', prompt_text=u'Resource <%s> saving unsuccessful' % self.res_filename)

        else:
            msg = u'Not define resource filename'
            log_func.warning(msg)
            wxdlg_func.openWarningBox(title=u'EDITOR', prompt_text=msg)

        event.Skip()

    def onSaveAsToolClicked(self, event):
        """
        <Save As...> tool button click handler.
        """
        resource = self.collectItemResource()
        resource = spc_func.clearAllResourcesFromSpc(resource)

        res_filename = None
        default_path = file_func.getProjectPath() if file_func.getProjectPath() else file_func.getFrameworkPath()
        save_dirname = wxdlg_func.getDirDlg(parent=self, title=u'SAVE',
                                            default_path=default_path)
        if save_dirname and os.path.exists(save_dirname):
            res_name = wxdlg_func.getTextEntryDlg(parent=self, title=u'SAVE',
                                                  prompt_text=u'Enter a name for the new resource',
                                                  default_value=os.path.splitext(os.path.basename(self.res_filename))[0] + str(wx.NewId()) if self.res_filename else 'Unknown')
            if res_name:
                res_filename = os.path.join(save_dirname, res_name + res_func.RESOURCE_FILE_EXT)

        if res_filename:
            result = res_func.saveResourceText(res_filename, resource_data=resource)
            if result:
                wxdlg_func.openMsgBox(title=u'EDITOR', prompt_text=u'Resource <%s> saving successful' % self.res_filename)
                self.loadResourceFile(res_filename)
            else:
                wxdlg_func.openWarningBox(title=u'EDITOR', prompt_text=u'Resource <%s> saving unsuccessful' % self.res_filename)
        else:
            msg = u'Not define resource filename'
            log_func.warning(msg)
            wxdlg_func.openWarningBox(title=u'EDITOR', prompt_text=msg)

        event.Skip()

    def onOpenToolClicked(self, event):
        """
        <Open> tool button click handler.
        """
        default_path = file_func.getProjectPath() if file_func.getProjectPath() else file_func.getFrameworkPath()
        res_filename = wxdlg_func.getFileDlg(parent=self, title=u'LOAD',
                                             wildcard_filter='Resource files (*.res)|*.res',
                                             default_path=default_path)

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

    def genResourceModule(self, module_filename, resource):
        """
        Generate resource module file.

        :param module_filename: Module filename.
        :param resource: Resource.
        :return: True/False.
        """
        result = False
        if spc_func.GEN_MODULE_FUNC_ATTR_NAME in resource:
            try:
                gen_module_func = resource.get(spc_func.GEN_MODULE_FUNC_ATTR_NAME, None)
                if gen_module_func:
                    result = gen_module_func(module_filename=module_filename,
                                             resource=resource) if gen_module_func is not None else False
                else:
                    log_func.warning(u'Module generation function not defined')
            except:
                log_func.fatal(u'Error generate module function')
        return result

    def onModuleToolClicked(self, event):
        """
        Resource module tool button click handler.
        """
        item_resource = self.getItemResource()

        # Generate resource module file
        result = False
        package_path = os.path.dirname(self.res_filename)
        py_modulename = file_func.setFilenameExt(os.path.basename(self.res_filename), '.py')
        module_filename = os.path.join(package_path, py_modulename)
        if os.path.exists(module_filename):
            if wxdlg_func.openAskBox(title=u'SAVE', prompt_text=u'File <%s> exists. Rewrite it?' % module_filename):
                result = self.genResourceModule(module_filename=module_filename,
                                                resource=item_resource)
        else:
            result = self.genResourceModule(module_filename=module_filename,
                                            resource=item_resource)
        if result and os.path.exists(module_filename):
            item_resource['module'] = os.path.basename(module_filename)
            self.getProperty('module').SetValue(item_resource['module'])
            msg = u'Resource module <%s> is generated' % module_filename
            log_func.info(msg)
            wxdlg_func.openMsgBox(title=u'MODULE', prompt_text=msg)
        else:
            msg = u'Resource module <%s> is not generated' % module_filename
            log_func.error(msg)
            wxdlg_func.openErrBox(title=u'MODULE', prompt_text=msg)

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

    def onCollapseToolClicked(self, event):
        """
        Hide resource tool button click handler.
        """
        self.collapseSplitterWindowPanel(splitter=self.editor_splitter, toolbar=self.editor_toolBar,
                                         collapse_tool=self.collapse_tool, expand_tool=self.expand_tool,
                                         resize_panel=1)
        event.Skip()

    def onExpandToolClicked(self, event):
        """
        Show object inspector tool button click handler.
        """
        self.expandSplitterWindowPanel(splitter=self.editor_splitter, toolbar=self.editor_toolBar,
                                       collapse_tool=self.collapse_tool, expand_tool=self.expand_tool,
                                       resize_panel=1)
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
            log_func.fatal(u'Error popup resource item context menu')

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
            self.component_menu = select_component_menu.iqSelectComponentFlatMenu()
            self.component_menu.init(parent=self.resource_treeListCtrl,
                                     parent_component=resource_item)
            self.component_menu.create(menuitem_handler=self.onSelectComponentMenuItem)
            context_menu.AppendMenu(wx.NewId(), 'Add', self.component_menu)

            context_menu.AppendSeparator()

            menuitem_id = wx.NewId()
            menuitem = flatmenu.FlatMenuItem(context_menu, menuitem_id, label='Copy',
                                             normalBmp=wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_MENU))
            self.Bind(wx.EVT_MENU, self.onCopyResourceMenuitem, id=menuitem_id)
            context_menu.AppendItem(menuitem)

            menuitem_id = wx.NewId()
            menuitem = flatmenu.FlatMenuItem(context_menu, menuitem_id, label='Paste',
                                             normalBmp=wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_MENU))
            self.Bind(wx.EVT_MENU, self.onPasteResourceMenuitem, id=menuitem_id)
            context_menu.AppendItem(menuitem)

            menuitem_id = wx.NewId()
            menuitem = flatmenu.FlatMenuItem(context_menu, menuitem_id, label='Cut',
                                             normalBmp=wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_MENU))
            self.Bind(wx.EVT_MENU, self.onCutResourceMenuitem, id=menuitem_id)
            context_menu.AppendItem(menuitem)

            context_menu.AppendSeparator()
            root_item = self.resource_treeListCtrl.GetMainWindow().GetRootItem()
            parent_item = self.resource_treeListCtrl.GetMainWindow().GetItemParent(item)
            first_child_item = self.resource_treeListCtrl.GetMainWindow().GetFirstChild(parent_item)[0] if parent_item and parent_item.IsOk() else None
            last_child_item = self.resource_treeListCtrl.GetMainWindow().GetLastChild(parent_item) if parent_item and parent_item.IsOk() else None

            menuitem_id = wx.NewId()
            menuitem = flatmenu.FlatMenuItem(context_menu, menuitem_id, label='Move up',
                                             normalBmp=wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_MENU))
            self.Bind(wx.EVT_MENU, self.onMoveUpResourceMenuitem, id=menuitem_id)
            context_menu.AppendItem(menuitem)
            menuitem.Enable(item != root_item and first_child_item and item != first_child_item)

            menuitem_id = wx.NewId()
            menuitem = flatmenu.FlatMenuItem(context_menu, menuitem_id, label='Move down',
                                             normalBmp=wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_MENU))
            self.Bind(wx.EVT_MENU, self.onMoveDownResourceMenuitem, id=menuitem_id)
            context_menu.AppendItem(menuitem)
            menuitem.Enable(item != root_item and last_child_item and item != last_child_item)

            return context_menu
        return None

    def appendResourceItem(self, item=None, resource=None, expand=True, select_new=False):
        """
        Append new child resource in item.

        :param item: Parent tree list treelistctrl item.
            If item is None then get selected item.
        :param resource: Child resource.
        :param expand: Expand item after append?
        :param select_new: Select new item?
        :return: True/False.
        """
        if resource is None:
            resource = dict()
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetSelection()

        try:
            if item and item.IsOk():
                item_resource = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)

                name = resource.get('name', 'Unknown')
                description = resource.get('description', '')
                component_type = resource.get('type', None)
                activate = resource.get('activate', True)

                # Add but only if the name is unique
                children_names = [child_res.get('name', 'Unknown') for child_res in item_resource[spc_func.CHILDREN_ATTR_NAME]]
                if name not in children_names:
                    item_resource[spc_func.CHILDREN_ATTR_NAME].append(resource)

                img_idx = self.component_icons.get(component_type, self.component_icons[None])
                child_item = self.resource_treeListCtrl.GetMainWindow().AppendItem(parentId=item, text=name,
                                                                                   image=img_idx, data=resource)
                self.refreshResourceItem(item=child_item, name=name, description=description, activate=activate)
                if select_new:
                    self.resource_treeListCtrl.GetMainWindow().SelectItem(child_item)

                if resource.get(spc_func.CHILDREN_ATTR_NAME, None):
                    for child_resource in resource[spc_func.CHILDREN_ATTR_NAME]:
                        # log_func.debug(u'Append %s : %s' % (resource['name'], child_resource['name']))
                        self.appendResourceItem(item=child_item, resource=child_resource, expand=False)

                if expand:
                    self.resource_treeListCtrl.GetMainWindow().Expand(item)

                return True
            else:
                log_func.error(u'Item <%s> not correct' % str(item))
        except:
            log_func.fatal(u'Error append new child resource in item')
        return False

    def onSelectComponentMenuItem(self, event):
        """
        Select component menu item handler.
        """
        if self.item_context_menu and self.component_menu:
            menuitem_id = event.GetId()
            selected_component = self.component_menu.menuitem2component_spc.get(menuitem_id, None)
            component_type = selected_component.get('type', 'UndefinedType')
            log_func.info(u'Selected component <%s>' % component_type)
            component_resource = components.findComponentSpc(component_type)
            component_resource = spc_func.fillResourceBySpc(dict(), component_resource)
            component_resource['name'] += str(wx.NewId())
            selected_item = self.resource_treeListCtrl.GetMainWindow().GetSelection()
            self.appendResourceItem(selected_item, component_resource, select_new=True)

            self.item_context_menu = None
            self.component_menu = None
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
        try:
            if item and item.IsOk():
                resource_item = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
                resource_item = copy.deepcopy(resource_item)
                resource_item['name'] = resource_item.get('name', 'default') + str(wx.NewId())
                clipboard.toClipboard(resource_item, do_copy=False)
            else:
                log_func.error(u'Item <%s> not correct' % str(item))
        except:
            log_func.fatal(u'Error copy resource to clipboard')
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
        try:
            if item and item.IsOk():
                resource_item = clipboard.fromClipboard()
                component_type = resource_item.get('type', None)
                item_spc = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
                item_content = item_spc.get(spc_func.CONTENT_ATTR_NAME, list())
                if component_type in item_content:
                    return self.appendResourceItem(item, resource_item, select_new=True)
                else:
                    item_type = item_spc.get('type', 'UnknownType')
                    msg = u'Unable to add component <%s> to <%s>' % (component_type, item_type)
                    log_func.warning(msg)
                    wxdlg_func.openWarningBox(u'PASTE', msg)
            else:
                log_func.error(u'Item <%s> not correct' % str(item))
        except:
            log_func.fatal(u'Error past resource from clipboard')
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
        try:
            if item and item.IsOk():
                resource_item = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
                resource_item = copy.deepcopy(resource_item)
                clipboard.toClipboard(resource_item, do_copy=False)
                self.resource_treeListCtrl.GetMainWindow().Delete(item)
                return resource_item
            else:
                log_func.error(u'Item <%s> not correct' % str(item))
        except:
            log_func.fatal(u'Error cut resource to clipboard')
        return None

    def moveUpResourceItem(self, item=None):
        """
        Move up resource.

        :param item: Resource tree item.
            If None then get selected item.
        :return: True/False.
        """
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetSelection()
        try:
            if item and item.IsOk():
                parent_item = self.resource_treeListCtrl.GetMainWindow().GetItemParent(item)
                if parent_item and parent_item.IsOk():
                    prev_item = self.resource_treeListCtrl.GetMainWindow().GetPrev(item)
                    resource_item = self.resource_treeListCtrl.GetMainWindow().GetItemData(prev_item)
                    name = resource_item.get('name', 'Unknown')
                    description = resource_item.get('description', '')
                    img_idx = self.resource_treeListCtrl.GetMainWindow().GetItemImage(prev_item)
                    new_item = self.resource_treeListCtrl.GetMainWindow().InsertItemByItem(parentId=parent_item,
                                                                                           idPrevious=item,
                                                                                           text=name,
                                                                                           image=img_idx,
                                                                                           data=resource_item)
                    self.resource_treeListCtrl.GetMainWindow().SetItemText(new_item, description, 1)
                    self.resource_treeListCtrl.GetMainWindow().Delete(prev_item)
                    self.resource_treeListCtrl.GetMainWindow().SelectItem(item)
                    return True
            else:
                log_func.error(u'Item <%s> not correct' % str(item))
        except:
            log_func.fatal(u'Error move up resource')
        return False

    def moveDownResourceItem(self, item=None):
        """
        Move down resource.

        :param item: Resource tree item.
            If None then get selected item.
        :return: True/False.
        """
        if item is None:
            item = self.resource_treeListCtrl.GetMainWindow().GetSelection()
        try:
            if item and item.IsOk():
                parent_item = self.resource_treeListCtrl.GetMainWindow().GetItemParent(item)
                if parent_item and parent_item.IsOk():
                    next_item = self.resource_treeListCtrl.GetMainWindow().GetNext(item)
                    resource_item = self.resource_treeListCtrl.GetMainWindow().GetItemData(item)
                    name = resource_item.get('name', 'Unknown')
                    description = resource_item.get('description', '')
                    img_idx = self.resource_treeListCtrl.GetMainWindow().GetItemImage(item)
                    new_item = self.resource_treeListCtrl.GetMainWindow().InsertItemByItem(parentId=parent_item,
                                                                                           idPrevious=next_item,
                                                                                           text=name,
                                                                                           image=img_idx,
                                                                                           data=resource_item)
                    self.resource_treeListCtrl.GetMainWindow().SetItemText(new_item, description, 1)
                    self.resource_treeListCtrl.GetMainWindow().Delete(item)
                    self.resource_treeListCtrl.GetMainWindow().SelectItem(new_item)
                    return True
            else:
                log_func.error(u'Item <%s> not correct' % str(item))
        except:
            log_func.fatal(u'Error move down resource')
        return False

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

    def onMoveUpResourceMenuitem(self, event):
        """
        Move up selected item to clipboard handler.
        """
        self.moveUpResourceItem()
        event.Skip()

    def onMoveDownResourceMenuitem(self, event):
        """
        Move down selected item to clipboard handler.
        """
        self.moveDownResourceItem()
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
        log_func.fatal(u'Error open resource editor')
    return False


def runResourceEditor(res_filename=None):
    """
    Run resource editor.

    :param res_filename: Resource file name.
    :return: True/False.
    """
    log_func.info(u'wxPython version: %s' % wx.VERSION_STRING)

    app = wx.App()
    openResourceEditor(res_filename=res_filename)
    app.MainLoop()


if __name__ == '__main__':
    runResourceEditor(res_filename=sys.argv[1] if len(sys.argv) > 1 else None)
