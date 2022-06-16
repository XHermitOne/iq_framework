#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module <resource_editor_appwin.py>. 
Generated by the iqFramework module the Glade prototype.
"""

import sys
import os
import os.path
import signal
import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk
import gi.repository.GdkPixbuf

from ....util import log_func
from ....util import file_func
from ....util import res_func
from ....util import spc_func
from ....util import lang_func
from ....util import id_func
from ....util import global_func
from ....util import icon_func
from ....util import exec_func

from ....engine.gtk.dlg import gtk_dlg_func

from .... import components
from .... import project

from ....engine.gtk import gtk_handler

from ....engine.gtk import stored_gtk_form_manager
from ....engine.gtk import gtktreeview_manager
from ....engine.gtk import gtkpaned_manager

from . import new_resource_dialog

from . import property_editor_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqResourceEditor(gtk_handler.iqGtkHandler,
                       stored_gtk_form_manager.iqStoredGtkFormsManager,
                       gtktreeview_manager.iqGtkTreeViewManager,
                       gtkpaned_manager.iqGtkPanedManager,
                       property_editor_manager.iqPropertyEditorManager):
    """
    Unknown class.
    """
    def __init__(self, *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), 'resource_editor_win.glade')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='resource_editor_appwin',  
                                          *args, **kwargs)

        self.res_filename = None

        self.component_icons = dict()

        save_filename = os.path.join(file_func.getProfilePath(),
                                     self.getClassName() + res_func.PICKLE_RESOURCE_FILE_EXT)

        self.loadCustomProperties(save_filename)

    def initComponentIcons(self):
        """
        Initialization component icon image list object.

        :return:
        """
        self.component_icons[None] = icon_func.getIconFilename(None)

        component_spc_cache = components.getComponentSpcPalette()

        if component_spc_cache:
            for package in list(component_spc_cache.keys()):
                pkg_components = component_spc_cache[package]
                for component_spc in pkg_components:
                    component_type = component_spc.get('type', None)
                    if component_type:
                        icon_name = component_spc.get('__icon__', None)
                        if icon_name:
                            component_icon_filename = icon_func.getIconFilename(icon_name)
                            self.component_icons[component_type] = component_icon_filename
                            # log_func.debug(u'Create icon <%s : %d>' % (icon_name, component_icon_filename))
                        else:
                            log_func.warning(u'Component <%s> specification not define icon' % component_type)
                            log_func.warning(u'Verify __icon__ attribute in specification')
                    else:
                        log_func.warning(u'In specification %s not define type' % component_spc)

            # self.resource_treeListCtrl.SetImageList(self.getImageLibImageList())
        else:
            log_func.warning(u'Empty component specification cache <%s>' % str(component_spc_cache))

    def init(self):
        """
        Init form.
        """
        self.initImages()
        self.initControls()

        self.initComponentIcons()

    def initImages(self):
        """
        Init images of controls on form.
        """
        pass

    def initControls(self):
        """
        Init controls method.
        """
        self.getGtkObject('expand_toolitem').set_sensitive(False)

    def clearBox(self, box):
        """
        Clear box.

        :return: True/False.
        """
        try:
            for child in box.get_children():
                box.remove(child)
                child.destroy()
            return True
        except:
            log_func.fatal(u'Error clear box <%s>' % box.get_name())
        return False

    def clearProperties(self):
        """
        Clear all properties.
        """
        basic_property_box = self.getGtkObject('basic_property_box')
        self.clearBox(basic_property_box)

        special_property_box = self.getGtkObject('special_property_box')
        self.clearBox(special_property_box)

        method_box = self.getGtkObject('method_box')
        self.clearBox(method_box)

        event_box = self.getGtkObject('event_box')
        self.clearBox(event_box)

    def _loadResource(self, resource, parent_item=None):
        """
        Load resource in editor.

        :param resource: Resource struct.
        :param parent_item: Parent item for append resource.
            If None then append root item.
        :return: True/False.
        """
        name = resource.get('name', u'Unknown')
        guid = resource.get('guid', None)
        if not guid:
            resource['guid'] = id_func.genGUID()

        component_type = resource.get('type', None)
        if component_type == project.COMPONENT_TYPE:
            global_func.setProjectName(name)

        description = resource.get('description', u'')
        activate = resource.get('activate', True)
        icon_filename = self.component_icons.get(component_type, None)
        # log_func.debug(u'Add new resource item <%s : %s : %s : %s>' % (component_type, name, description, icon_idx))

        if icon_filename is None or not os.path.exists(icon_filename):
            img = gi.repository.Gtk.IconTheme.get_default().load_icon('image-missing', gi.repository.Gtk.IconSize.MENU, 0)
        else:
            img = gi.repository.GdkPixbuf.Pixbuf.new_from_file(icon_filename)
        if parent_item is None:
            new_item = self.getGtkObject('res_tree_treestore').append(None, [name, description, img])
        else:
            new_item = self.getGtkObject('res_tree_treestore').append(parent_item, [name, description, img])
        self.setGtkTreeViewItemData(self.getGtkObject('res_treeview'), new_item, resource)

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
            log_func.warning(u'Resource editor. Not define resource for loading')
            return False

        try:
            self.getGtkObject('res_tree_treestore').clear()

            result = self._loadResource(resource)

            # root_item = self.getGtkObject('res_tree_treestore').GetRootItem()
            # if root_item and root_item.IsOk():
            #     # self.resource_treeListCtrl.Expand(root_item)
            #     # resource = self.resource_treeListCtrl.GetMainWindow().GetItemData(root_item)
            #     # self.buildPropertyEditors(property_editor=self.object_propertyGridManager,
            #     #                           resource=resource, parent_resource=None)

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
            self.getGtkTopObject().set_title(title)
        return result

    def getItemResource(self, item=None):
        """
        Get item object resource.

        :param item: Tree list control item.
            If None then get root item.
        :return: Object resource or None if error.
        """
        resource = self.getGtkTreeViewItemData(self.getGtkObject('res_treeview'), item)
        return resource

    def getSelectedResource(self):
        """
        Get selected object resource.

        :return: Object resource or None if not selected.
        """
        return self.getGtkTreeViewSelectedItemData(treeview=self.getGtkObject('res_treeview'))

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
            item = self.getGtkTreeViewRootItem(treeview=self.getGtkObject('res_treeview'))

        if item:
            self.getGtkObject('res_tree_treestore').set_value(item, 0, name)
            self.getGtkObject('res_tree_treestore').set_value(item, 1, description)
            # active_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOXTEXT if activate else wx.SYS_COLOUR_GRAYTEXT)
            # self.resource_treeListCtrl.GetMainWindow().SetItemTextColour(item, active_colour)

    def collectItemResource(self, item=None):
        """
        Collect item resource from editor.

        :param item: Current item of resource tree control.
            If None then get root item.
        :return: Resource dictionary.
        """
        resource = dict()
        if item is None:
            item = self.getGtkTreeViewRootItem(treeview=self.getGtkObject('res_treeview'))

        try:
            resource = self.getGtkTreeViewItemData(treeview=self.getGtkObject('res_treeview'), item=item)
            if self.hasGtkTreeViewItemChildren(treeview=self.getGtkObject('res_treeview'), item=item):
                resource[spc_func.CHILDREN_ATTR_NAME] = list()
                child_item = self.getGtkTreeViewFirstChild(treeview=self.getGtkObject('res_treeview'), item=item)
                while child_item:
                    child_resource = self.collectItemResource(child_item)
                    resource[spc_func.CHILDREN_ATTR_NAME].append(child_resource)
                    child_item = self.getGtkTreeViewNextChild(treeview=self.getGtkObject('res_treeview'), item=child_item)
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

    def onDestroy(self, widget):
        """
        Destroy window handler.
        """
        save_filename = os.path.join(file_func.getProfilePath(),
                                     self.getClassName() + res_func.PICKLE_RESOURCE_FILE_EXT)
        self.saveCustomProperties(save_filename)
        gi.repository.Gtk.main_quit()

    def onNewToolClicked(self, widget):
        """
        <New> resource tool button click handler.
        """
        default_res_filename = os.path.join(os.path.dirname(self.res_filename), 'default' + res_func.RESOURCE_FILE_EXT)
        res_filename = new_resource_dialog.createNewResource(parent=self, res_filename=default_res_filename)
        if res_filename is not None:
            self.loadResourceFile(res_filename)

    def onSaveToolClicked(self, widget):
        """
        <Save> tool button click handler.
        """
        resource = self.collectItemResource()
        resource = spc_func.clearAllResourcesFromSpc(resource)
        if self.res_filename is None:
            self.res_filename = gtk_dlg_func.getFileDlg(parent=self, title=u'SAVE',
                                                        wildcard_filter='Resource files (*.res)|*.res')
        if self.res_filename:
            result = res_func.saveResourceText(self.res_filename, resource_data=resource)
            if result:
                gtk_dlg_func.openMsgBox(title=u'EDITOR', prompt_text=u'Resource <%s> saving successful' % self.res_filename)
            else:
                gtk_dlg_func.openWarningBox(title=u'EDITOR', prompt_text=u'Resource <%s> saving unsuccessful' % self.res_filename)

        else:
            msg = u'Not define resource filename'
            log_func.warning(msg)
            gtk_dlg_func.openWarningBox(title=u'EDITOR', prompt_text=msg)

    def onSaveAsToolClicked(self, widget):
        """
        <Save As...> tool button click handler.
        """
        resource = self.collectItemResource()
        resource = spc_func.clearAllResourcesFromSpc(resource)

        res_filename = None
        default_path = file_func.getProjectPath() if file_func.getProjectPath() else file_func.getFrameworkPath()
        save_dirname = gtk_dlg_func.getDirDlg(parent=self, title=u'SAVE',
                                              default_path=default_path)
        if save_dirname and os.path.exists(save_dirname):
            res_name = gtk_dlg_func.getTextEntryDlg(parent=self, title=u'SAVE',
                                                    prompt_text=u'Enter a name for the new resource',
                                                    default_value=os.path.splitext(os.path.basename(self.res_filename))[0] + id_func.genNewId() if self.res_filename else 'Unknown')
            if res_name:
                res_filename = os.path.join(save_dirname, res_name + res_func.RESOURCE_FILE_EXT)

        if res_filename:
            result = res_func.saveResourceText(res_filename, resource_data=resource)
            if result:
                gtk_dlg_func.openMsgBox(title=u'EDITOR', prompt_text=u'Resource <%s> saving successful' % self.res_filename)
                self.loadResourceFile(res_filename)
            else:
                gtk_dlg_func.openWarningBox(title=u'EDITOR', prompt_text=u'Resource <%s> saving unsuccessful' % self.res_filename)
        else:
            msg = u'Not define resource filename'
            log_func.warning(msg)
            gtk_dlg_func.openWarningBox(title=u'EDITOR', prompt_text=msg)

    def onOpenToolClicked(self, widget):
        """
        <Open> tool button click handler.
        """
        default_path = file_func.getProjectPath() if file_func.getProjectPath() else file_func.getFrameworkPath()
        res_filename = gtk_dlg_func.getFileDlg(parent=self, title=u'LOAD',
                                               wildcard_filter='Resource files (*.res)|*.res',
                                               default_path=default_path)

        if res_filename:
            self.loadResourceFile(res_filename)
        else:
            log_func.warning(u'Not define resource filename')

    def onTestToolClicked(self, widget):
        """
        Test tool button click handler.
        """
        item_resource = self.getSelectedResource()

        test_func = item_resource.get(spc_func.TEST_FUNC_ATTR_NAME, None)
        if test_func:
            test_func(item_resource)
        else:
            log_func.warning(u'Not define TEST function for <%s>' % item_resource.get('type', None))

    def onDesignToolClicked(self, widget):
        """
        Design tool button click handler.
        """
        item_resource = self.getSelectedResource()

        design_func = item_resource.get(spc_func.DESIGN_FUNC_ATTR_NAME, None)
        if design_func:
            design_func(item_resource)
        else:
            log_func.warning(u'Not define DESIGN function for <%s>' % item_resource.get('type', None))

    def onGenModuleToolClicked(self, widget):
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
            if gtk_dlg_func.openAskBox(title=u'SAVE', prompt_text=u'File <%s> exists. Rewrite it?' % module_filename):
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
            gtk_dlg_func.openMsgBox(title=u'MODULE', prompt_text=msg)
        else:
            msg = u'Resource module <%s> is not generated' % module_filename
            log_func.warning(msg)
            gtk_dlg_func.openErrBox(title=u'MODULE', prompt_text=msg)

    def onHelpToolClicked(self, widget):
        """
        Help tool button click handler.
        """
        item_resource = self.getSelectedResource()

        doc = item_resource.get(spc_func.DOC_ATTR_NAME, None)
        if isinstance(doc, str):
            # Document as HTML file
            doc_filename = os.path.join(file_func.getFrameworkPath(), doc)
            if os.path.exists(doc_filename):
                exec_func.openHtmlBrowser(doc_filename)
            else:
                log_func.warning(u'Document filename <%s> not found' % doc_filename)
        elif isinstance(doc, dict):
            # Document as open command
            open_doc_command = doc.get(sys.platform, None)
            if open_doc_command:
                exec_func.execSystemCommand(open_doc_command)
            else:
                log_func.warning(u'Not define DOC open command for platform <%s> in' % sys.platform)
        else:
            log_func.warning(u'Not define DOC for <%s>' % item_resource.get('type', None))

    def onCollapseToolClicked(self, widget):
        """
        Hide resource tool button click handler.
        """
        self.collapseGtkPanedPanel(paned=self.getGtkObject('res_paned'), toolbar=self.getGtkObject('ctrl_toolbar'),
                                   collapse_tool=self.getGtkObject('collapse_toolitem'),
                                   expand_tool=self.getGtkObject('expand_toolitem'),
                                   resize_panel=1)

    def onExpandToolClicked(self, widget):
        """
        Show object inspector tool button click handler.
        """
        self.expandGtkPanedPanel(paned=self.getGtkObject('res_paned'), toolbar=self.getGtkObject('ctrl_toolbar'),
                                 collapse_tool=self.getGtkObject('collapse_toolitem'),
                                 expand_tool=self.getGtkObject('expand_toolitem'),
                                 resize_panel=1)

    def onResTreeViewSelectionChanged(self, widget):
        """
        Resource tree list control item selection changes handler.
        """
        try:
            item = self.getGtkTreeViewSelectedItem(treeview=self.getGtkObject('res_treeview'))
            resource = self.getGtkTreeViewItemData(treeview=self.getGtkObject('res_treeview'), item=item)
            parent_item = self.getGtkTreeViewParentItem(treeview=self.getGtkObject('res_treeview'), item=item)
            parent_resource = self.getGtkTreeViewItemData(treeview=self.getGtkObject('res_treeview'), item=parent_item) if parent_item else None
            self.buildPropertyEditors(property_editor=self, resource=resource, parent_resource=parent_resource)
        except:
            log_func.fatal(u'Error resource tree list control item selection changes handler')


def openResourceEditor(parent=None, res_filename=None):
    """
    Open resource editor frame.

    :param res_filename: Resource file name.
    :return: True/False.
    """
    result = False
    obj = None
    try:
        obj = iqResourceEditor()
        obj.init()
        if res_filename:
            obj.loadResourceFile(res_filename)
        obj.getGtkTopObject().run()
        result = True
    except:
        log_func.fatal(u'Error open window <resource_editor_appwin>')

    if obj and obj.getGtkTopObject() is not None:
        obj.getGtkTopObject().destroy()
    return result                    


def runResourceEditor(res_filename=None):
    """
    Run resource editor.

    :param res_filename: Resource file name.
    :return: True/False.
    """
    log_func.info(u'GTK library version: %s' % gi.__version__)

    result = False
    win = None
    try:
        win = iqResourceEditor()
        win.init()
        if res_filename:
            win.loadResourceFile(res_filename)
        win.getGtkTopObject().show_all()
        result = True
    except:
        log_func.fatal(u'Error open window <Resource Editor>')

    gi.repository.Gtk.main()

    if win and win.getGtkTopObject() is not None:
        win.getGtkTopObject().destroy()
    return result


if __name__ == '__main__':
    runResourceEditor()
