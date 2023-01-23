#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
New resource dialog class module.
"""

import copy
import os.path
import wx

from . import new_resource_dlg

from ....util import log_func
from ....util import file_func
from ....util import res_func
from ....util import spc_func
from ....util import id_func
from ....engine.wx import wxbitmap_func
from .... import components

from . import select_component_menu

__version__ = (0, 0, 0, 1)


class iqNewResourceDialog(new_resource_dlg.iqNewResourceDialogProto):
    """
    New resource dialog class module.
    """
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent window object.
        """
        new_resource_dlg.iqNewResourceDialogProto.__init__(self, parent=parent)

        bmp = wxbitmap_func.createIconBitmap('dots')
        self.component_button.SetBitmap(bmp)

        self.res_filename = None
        self.resource = None

        self.component_menu = None

    def init(self, component_spc=None, component_name=None, res_filename=None):
        """
        Initialization dialog.

        :param component_spc: Resource component specification.
        :param component_name: Component name.
        :param res_filename: Resource filename.
        :return:
        """
        if component_spc:
            component_type = component_spc.get('type', '')
            if component_type:
                self.component_textCtrl.SetValue(component_type)
                icon = component_spc.get(spc_func.ICON_ATTR_NAME, None)
                if icon:
                    bmp = wxbitmap_func.createIconBitmap()
                    if bmp:
                        self.component_bitmap.SetBitmap(bmp)
        if component_name:
            self.name_textCtrl.SetValue(component_name)
        if res_filename:
            self.path_dirPicker.SetPath(os.path.dirname(res_filename))
        else:
            res_filename = self.genResFilename(component_name)
            if res_filename:
                self.path_dirPicker.SetPath(os.path.dirname(res_filename))
        if res_filename:
            self.res_filename = res_filename
        if component_spc:
            self.resource = copy.deepcopy(component_spc)
            if component_name:
                self.resource['name'] = component_name
            if not self.resource.get('guid', None):
                self.resource['guid'] = id_func.genGUID()

        self.ok_button.Enable(bool(component_spc) and bool(component_name) and bool(res_filename))

    def genResFilename(self, component_name):
        """
        Generate resource filename by component_name.

        :param component_name: Component name.
        :return: New resource filename or None if error.
        """
        if component_name:
            res_filename = os.path.join(file_func.getProjectPath(),
                                        component_name + res_func.RESOURCE_FILE_EXT)
            return res_filename
        return None

    def onCancelButtonClick(self, event):
        """
        Button click <Cancel> handler.
        """
        self.res_filename = None
        self.resource = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Button click <OK> handler.
        """
        self.res_filename = os.path.join(self.path_dirPicker.GetPath(),
                                         self.name_textCtrl.GetValue() + res_func.RESOURCE_FILE_EXT)

        component_type = self.component_textCtrl.GetValue()
        component_spc = components.findComponentSpc(component_type)
        self.resource = copy.deepcopy(component_spc)
        self.resource['name'] = self.name_textCtrl.GetValue().strip()
        if not self.resource.get('guid', None):
            self.resource['guid'] = id_func.genGUID()

        self.EndModal(wx.ID_OK)
        event.Skip()

    def onSelectComponentMenuItem(self, event):
        """
        Select component menu item handler.
        """
        if self.component_menu:
            menuitem_id = event.GetId()
            selected_component = self.component_menu.menuitem2component_spc.get(menuitem_id, None)
            component_type = selected_component.get('type', 'UndefinedType')
            bmp = wxbitmap_func.createIconBitmap(selected_component.get(spc_func.ICON_ATTR_NAME, None))
            self.component_textCtrl.SetValue(component_type)
            self.component_bitmap.SetBitmap(bmp)

            name = self.name_textCtrl.GetValue().strip()
            if not name:
                name = selected_component.get('name', 'default') + str(wx.NewId())
                self.name_textCtrl.SetValue(name)

            if name and not self.path_dirPicker.GetPath():
                self.res_filename = self.genResFilename(component_name=name)
                self.path_dirPicker.SetPath(os.path.dirname(self.res_filename))

            log_func.info(u'Selected component <%s>' % component_type)
            self.component_menu = None

        self.ok_button.Enable(bool(self.component_textCtrl.GetValue()) and
                              bool(self.name_textCtrl.GetValue()) and
                              bool(self.path_dirPicker.GetPath()))
        event.Skip()

    def onComponentButtonClick(self, event):
        """
        Component button click handler.
        """
        try:
            self.component_menu = select_component_menu.iqSelectComponentMenu()
            self.component_menu.init(parent=self, parent_component=None)
            self.component_menu.create(menuitem_handler=self.onSelectComponentMenuItem)

            self.component_button.PopupMenu(self.component_menu)
        except:
            log_func.fatal(u'Error component select button')

        event.Skip()

    def onComponentText(self, event):
        """
        Change component type text control handler.
        """
        self.ok_button.Enable(bool(self.component_textCtrl.GetValue()) and
                              bool(self.name_textCtrl.GetValue()) and
                              bool(self.path_dirPicker.GetPath()))
        event.Skip()

    def onNameText(self, event):
        """
        Change resource name text control handler.
        """
        self.ok_button.Enable(bool(self.component_textCtrl.GetValue()) and
                              bool(self.name_textCtrl.GetValue()) and
                              bool(self.path_dirPicker.GetPath()))
        event.Skip()

    def onPathDirChanged(self, event):
        """
        Change resource path dir picker handler.
        """
        self.ok_button.Enable(bool(self.component_textCtrl.GetValue()) and
                              bool(self.name_textCtrl.GetValue()) and
                              bool(self.path_dirPicker.GetPath()))
        event.Skip()


def createNewResource(parent=None, component_spc=None, component_name=None, res_filename=None):
    """
    Create new resource.

    :param parent: Parent frame.
    :param component_spc: Resource component specification.
    :param component_name: Component name.
    :param res_filename: Resource filename.
    :return: New resource filename or None if error or Cancel button pressed.
    """
    dlg = None
    try:
        dlg = iqNewResourceDialog(parent=parent)
        dlg.init(component_spc, component_name, res_filename)
        result = None
        if dlg.ShowModal() == wx.ID_OK:
            resource = spc_func.clearAllResourcesFromSpc(dlg.resource)
            if res_func.saveResourceText(dlg.res_filename, resource):
                result = dlg.res_filename
        dlg.Destroy()
        return result
    except:
        log_func.fatal(u'Error create new resource')
        if dlg:
            dlg.Destroy()
    return None
