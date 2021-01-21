#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialogue form for testing the UniReader controller.
"""

import wx

from . import test_uni_reader_ctrl_dlg_proto

from ...util import log_func
from ...dialog import dlg_func

from ...engine.wx import form_manager
from ...engine.wx import listctrl_manager

__version__ = (0, 0, 1, 5)


class iqTestUniReaderCtrlDlg(test_uni_reader_ctrl_dlg_proto.iqTestUniReaderControllerDlgProto,
                             form_manager.iqDialogManager,
                             listctrl_manager.iqListCtrlManager):
    """
    Dialogue form for testing the UniReader controller.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        test_uni_reader_ctrl_dlg_proto.iqTestUniReaderControllerDlgProto.__init__(self, *args, **kwargs)

        self.tags = None

        self.controller = None

    def setTags(self, tags=None):
        """
        Set tested tags.

        :param tags: Tags dictionary:
            {'tag_name': 'tag address', ... }
        """
        if isinstance(tags, dict):
            self.tags = tags
        else:
            log_func.warning(u'Tags type error')
            self.tags = dict()

    def setController(self, controller=None):
        """
        Set controller object.

        :param controller: Controller object.
        """
        self.controller = controller
        if self.controller:
            # Set tags
            tags = self.controller.getTags()
            if tags:
                self.setTags(tags)
            else:
                log_func.warning(u'Not define controller tags <%s>' % self.controller.getName())
        else:
            log_func.warning(u'Not define testing controller')

    def initImages(self):
        """
        Init control images.
        """
        pass

    def initControls(self):
        """
        Init controls.
        """
        self.setListCtrlColumns(listctrl=self.tags_listCtrl,
                                cols=(dict(label=u'Name', width=150),
                                      dict(label=u'Address', width=400),
                                      dict(label=u'Value', width=400)))
        if isinstance(self.tags, dict):
            self.updateTags(**self.tags)

    def init(self):
        """
        Init form.
        """
        self.initImages()
        self.initControls()

    def updateTags(self, **tags):
        """
        Update tags.

        :param tags: Tags dictionary:
            {'tag name': 'tag address', ... }
        :return: True/False.
        """
        if tags:
            tag_names = list(tags.keys())
            tag_names.sort()

            tag_values = self.read_tags(**tags)
            if tag_values is not None:
                rows = [(tag_name,
                         tags[tag_name],
                         tag_values[tag_name]) for tag_name in tag_names]
                self.setListCtrlRows(listctrl=self.tags_listCtrl,
                                     rows=rows,
                                     even_background_colour=wx.WHITE,
                                     odd_background_colour=wx.LIGHT_GREY)

    def read_tags(self, **tags):
        """
        Read tags from controller.

        :param tags: Tags dictionary:
            {'tag name': 'tag address', ... }
        :return: Tag values dictionary:
            {'tag name': 'tag value', ... }
            or None if error.
        """
        if self.controller is None:
            msg = u'Not define testing controller'
            log_func.warning(msg)
            dlg_func.openWarningBox(u'ERROR', msg)
            return None

        tag_values = self.controller.readTags(**tags)
        if tags and not tag_values:
            log_func.warning(u'Error read tag values')
        return tag_values

    def onOkButtonClick(self, event):
        """
        Ok button click handler.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onUpdateToolClicked(self, event):
        """
        Update tool click handler.
        """
        if isinstance(self.tags, dict):
            self.updateTags(**self.tags)
        else:
            log_func.warning(u'Not define controller tags')
        event.Skip()

    def onAddToolClicked(self, event):
        """
        Add tag tool click handler.
        """
        tag_name = self.tag_textCtrl.GetValue()
        tag_address = self.address_textCtrl.GetValue()

        if tag_name not in self.tags:
            self.tags[tag_name] = tag_address
            self.updateTags(**self.tags)
        else:
            msg = u'Tag <%s> already on the list' % tag_name
            log_func.warning(msg)
            dlg_func.openWarningBox(u'ERROR', msg)

        event.Skip()

    def onDelToolClicked(self, event):
        """
        Delete tag tool click handler.
        """
        selected_idx = self.getListCtrlSelectedRowIdx(listctrl_or_event=self.tags_listCtrl)
        if selected_idx >= 0:
            tag_name = self.tags_listCtrl.GetItemText(selected_idx)
            log_func.debug(u'Delete tag <%s>' % tag_name)
            del self.tags[tag_name]
            self.updateTags(**self.tags)
        event.Skip()


def viewTestUniReaderCtrlDlg(parent=None, controller=None):
    """
    View uni reader controller test dialog.

    :param parent: Parent window.
    :param controller: Controller object.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        controller.printConnectionParam()
        log_func.info(u'\tTags: %s' % str(controller.getTags().keys() if controller.getTags() else controller.getTags()))

        dlg = iqTestUniReaderCtrlDlg(parent=parent)
        dlg.setController(controller)
        dlg.init()
        dlg.ShowModal()
    except:
        log_func.fatal(u'Error view uni reader controller test dialog')
