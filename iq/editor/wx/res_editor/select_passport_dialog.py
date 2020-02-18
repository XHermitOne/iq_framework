#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select passport dialog.
"""

import os.path
import wx

from . import select_passport_dlg

from ....util import log_func
from ....util import file_func
from ....util import res_func

from ....engine.wx import imglib_manager
from .... import components
from .... import project

__version__ = (0, 0, 0, 1)


class iqSelectPassportDialog(select_passport_dlg.iqSelectPassportDialogProto,
                             imglib_manager.iqImageLibraryManager):
    """
    Select passport dialog.
    """
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent form.
        """
        select_passport_dlg.iqSelectPassportDialogProto.__init__(self, parent=parent, *args, **kwargs)
        imglib_manager.iqImageLibraryManager.__init__(self)

        self.component_icons = dict()

        self.passport = None

    def init(self, prj_name=None):
        """
        Initialization.

        :param prj_name: Project name.
            If None then you can choose from any project.
        """
        self.initComponentIcons()

        self.buildProjects(prj_name=prj_name)

    def initComponentIcons(self):
        """
        Initialization component icon image list object.

        :return:
        """
        self.initImageLibrary()

        self.addBitmap('none', wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_MENU))
        self.component_icons[None] = self.getImageIdx('none')

        # Add framework icon
        self.addBitmap('root', wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_MENU))
        self.component_icons['root'] = self.getImageIdx('root')

        component_spc_cache = components.getComponentSpcPalette()

        if component_spc_cache:
            for package in list(component_spc_cache.keys()):
                pkg_components = component_spc_cache[package]
                for component_spc in pkg_components:
                    component_type = component_spc.get('type', None)
                    if component_type:
                        icon_name = component_spc.get('__icon__', None)
                        if icon_name:
                            component_icon_idx = self.getImageIdx(icon_name)
                            self.component_icons[component_type] = component_icon_idx
                        else:
                            log_func.warning(u'Component <%s> specification not define icon' % component_type)
                            log_func.warning(u'Verify __icon__ attribute in specification')
                    else:
                        log_func.error(u'In specification %s not define type' % component_spc)

            self.prj_treeListCtrl.SetImageList(self.getImageList())
            self.res_treeListCtrl.SetImageList(self.getImageList())
        else:
            log_func.error(u'Empty component specification cache <%s>' % str(component_spc_cache))

    def buildProjects(self, root_path=None, prj_name=None):
        """
        Build project tree.

        :param root_path: Root path.
        :param prj_name: Project name.
            If None then you can choose from any project.
        :return: True/False.
        """
        if root_path is None:
            root_path = file_func.getFrameworkPath()

        # Clear
        self.prj_treeListCtrl.GetMainWindow().DeleteAllItems()

        # Add root item
        root_img_idx = self.component_icons['root']
        root_item = self.prj_treeListCtrl.GetMainWindow().AddRoot(text=u'iQ', image=root_img_idx)

        # Add project
        prj_item = None
        if prj_name:
            dir_path = os.path.join(root_path, prj_name)
            if os.path.exists(dir_path):
                prj_item = self.prj_treeListCtrl.GetMainWindow().AppendItem(parentId=root_item, text=prj_name,
                                                                            image=root_img_idx)
                self._buildFolder(dir_path, parent_item=prj_item, prj_name=prj_name)
            else:
                log_func.error(u'Project directory path <%s> not found' % dir_path)

        # Add another projects
        dir_paths = file_func.getDirectoryPaths(root_path)
        dir_paths = [dir_path for dir_path in dir_paths if os.path.basename(dir_path) not in ('iq', prj_name)]
        dir_paths.sort()
        for dir_path in dir_paths:
            if os.path.exists(dir_path):
                dir_name = os.path.basename(dir_path)
                item = self.prj_treeListCtrl.GetMainWindow().AppendItem(parentId=root_item, text=dir_name,
                                                                        image=root_img_idx)
                self._buildFolder(dir_path, parent_item=item, prj_name=dir_name)
            else:
                log_func.error(u'Project directory path <%s> not found' % dir_path)

        self.prj_treeListCtrl.GetMainWindow().Expand(root_item)
        if prj_item:
            self.prj_treeListCtrl.GetMainWindow().Expand(prj_item)

    def _buildFolder(self, parent_path, parent_item, prj_name='unknown'):
        """
        Build folder tree.

        :param parent_path: Directory path.
        :param parent_item: Parent tree list control item.
        :param prj_name: Project name.
        :return:
        """
        folder_img_idx = self.component_icons['root']
        dir_paths = file_func.getDirectoryPaths(parent_path)
        for dir_path in dir_paths:
            if os.path.exists(dir_path):
                dir_name = os.path.basename(dir_path)
                item = self.prj_treeListCtrl.GetMainWindow().AppendItem(parentId=parent_item, text=dir_name,
                                                                        image=folder_img_idx)
                self._buildFolder(dir_path, parent_item=item, prj_name=prj_name)
            else:
                log_func.error(u'Project directory path <%s> not found' % dir_path)

        res_filenames = file_func.getFilePaths(parent_path)
        res_filenames = [filename for filename in res_filenames if file_func.isFilenameExt(filename, '.res')]
        for res_filename in res_filenames:
            if os.path.exists(res_filename):
                res_name = os.path.splitext(os.path.basename(res_filename))[0]
                resource = res_func.loadResourceText(res_filename)
                resource['__module__'] = res_name
                resource['__project__'] = prj_name
                component_type = resource.get('type', None)
                description = resource.get('description', u'')
                component_img_idx = self.component_icons.get(component_type, self.component_icons[None])
                item = self.prj_treeListCtrl.GetMainWindow().AppendItem(parentId=parent_item, text=res_name,
                                                                        image=component_img_idx, data=resource)
                self.prj_treeListCtrl.GetMainWindow().SetItemText(item=item, text=description, column=1)
            else:
                log_func.error(u'Project resource file <%s> not found' % res_filename)

    def getSelectedPassport(self):
        """
        Get selected passport.
        """
        return self.psp_staticText.GetLabel()

    def onCancelButtonClick(self, event):
        """
        Cancel button click handler.
        """
        self.passport = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Ok button click handler.
        """
        self.passport = self.getSelectedPassport()
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onPrjTreelistSelectionChanged(self, event):
        """
        Projects treelist control item selection changed handler.
        """
        item = event.GetItem()
        resource = self.prj_treeListCtrl.GetMainWindow().GetItemData(item)
        label = '%s.%s.%s.%s' % (resource.get('__project__', 'unknown'),
                                 resource.get('__module__', 'unknown'),
                                 resource.get('type', 'unknown'),
                                 resource.get('name', 'unknown')) if resource else u''
        self.psp_staticText.SetLabel(label)

        event.Skip()

    def onPrjTreelistItemActivated(self, event):
        """
        Projects treelist control item activated handler.
        """
        item = event.GetItem()
        resource = self.prj_treeListCtrl.GetMainWindow().GetItemData(item)

        event.Skip()


def selectPassportDlg(parent=None, prj_name=None):
    """
    Open select passport dialog.

    :param parent: Parent form.
    :param prj_name: Project name.
        If None then you can choose from any project.
    :return: Passport as string or None if Cancel pressed or error.
    """
    dlg = None
    try:
        dlg = iqSelectPassportDialog(parent=parent)
        dlg.init(prj_name)
        result = None
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.passport
        dlg.Destroy()
        return result
    except:
        log_func.fatal(u'Select passport dialog error')
        if dlg:
            dlg.Destroy()
    return None
