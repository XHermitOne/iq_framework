#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx data object find control component.
"""

try:
    import wx
except ImportError:
    print(u'Import error wx')

from . import spc

from ...util import log_func
from ...util import lang_func
from ...util import exec_func

from ...engine.wx import wxbitmap_func
from ...engine.wx.dlg import wxdlg_func
from ...engine.wx import listctrl_manager
from ...engine.wx import treelistctrl_manager

from . import find_ctrl
from ..wx_widget import component


__version__ = (0, 0, 1, 1)

_ = lang_func.getTranslation().gettext


class iqWxDataObjFindCtrl(find_ctrl.iqDataObjFindCtrlProto,
                          component.iqWxWidget,
                          listctrl_manager.iqListCtrlManager,
                          treelistctrl_manager.iqTreeListCtrlManager):
    """
    Wx data object find control component.
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

        find_ctrl.iqDataObjFindCtrlProto.__init__(self, parent=parent, id=wx.NewId(),
                                                  pos=self.getPosition(),
                                                  size=self.getSize(),
                                                  style=self.getStyle(),
                                                  name=self.getName())

        label = self.getLabel()
        if isinstance(label, str):
            self.find_staticText.SetLabelText(label)
        img = self.getImage()
        if isinstance(img, str):
            bmp = wxbitmap_func.createIconBitmap(img)
            self.find_bpButton.SetBitmap(bmp)

        # Data object
        self._data_obj = None
        self._data_obj = self.getDataObject()
        self._columns = None

        if self._data_obj:
            # Set find columns
            columns = self.getColumns()
            for column in columns:
                column_description = column.getDescription()
                self.find_choice.Append(column_description)
            if self.find_choice.GetCount():
                self.find_choice.Select(0)
        else:
            log_func.error(u'Not define data object in <%s>' % self.getName())

        # self.createChildren()

    def getDataObject(self):
        """
        Get data object.

        :return: Data object or None if error.
        """
        if self._data_obj is None:
            psp = self.getAttribute('data_obj')
            if psp:
                kernel = self.getKernel()
                self._data_obj = kernel.getObject(psp, register=True)
            else:
                log_func.warning(u'Not define data object in <%s>' % self.getName())
        return self._data_obj

    def setDataObject(self, data_obj):
        """
        Set data object.
        """
        self._data_obj = data_obj

    def getColumns(self):
        """
        Get find columns.
        """
        if self._columns is None:
            self._columns = list()
            if self._data_obj:
                column_names = self.getAttribute('columns')
                if column_names:
                    model_obj = self._data_obj.getModelObj()
                    for column_name in column_names:
                        parent_column_name = column_name.split('.')[0]
                        column = model_obj.getChild(parent_column_name)
                        if column:
                            self._columns.append(column)
                        else:
                            log_func.error(u'Not found column <%s> in model <%s>' % (column_name, model_obj.getName()))
                        if not column.getDescription().strip():
                            log_func.warning(u'Not define description for column <%s> in model <%s>' % (column_name,
                                                                                                        model_obj.getName()))
                else:
                    log_func.warning(u'Not define columns for find in <%s>' % self.getName())
        return self._columns

    def getLabel(self):
        """
        Get find label.
        """
        return _(self.getAttribute('label'))

    def getImage(self):
        """
        Get find image.
        """
        return self.getAttribute('image')

    def onFindButtonClick(self, event):
        """
        Find button event handler.
        """
        find_value = self.find_textCtrl.GetValue().strip()
        if find_value:
            if self.find_idents is None:
                # Get all find identificators
                if self._data_obj is not None:
                    column_names = self.getAttribute('columns')
                    column_idx = self.find_choice.GetSelection()
                    if column_names:
                        column_name = column_names[column_idx]
                        if find_value:
                            self.find_idents = self._data_obj.findIdentsByColumnValue(column_name=column_name,
                                                                                      column_value=find_value)
                            self.find_ident_idx = 0
                else:
                    log_func.error(u'Not define data object in <%s>' % self.getName())
            else:
                # If you do not need to update the list of found identificators,
                # then simply search for the next identificator in the list
                self.find_ident_idx += 1
                if self.find_ident_idx >= len(self.find_idents):
                    self.find_ident_idx = 0

            if self.find_idents:
                try:
                    context = self.getContext()
                    context['self'] = self
                    context['event'] = event
                    context['DATA_OBJ'] = self._data_obj
                    context['FIND_IDENTS'] = self.find_idents
                    context['FIND_IDENT_IDX'] = self.find_ident_idx
                    context['CUR_FIND_IDENT'] = self.find_idents[self.find_ident_idx] if self.find_idents else None

                    function_body = self.getAttribute('on_find')
                    if function_body:
                        exec_func.execTxtFunction(function=function_body,
                                                  context=context)
                except:
                    log_func.fatal(u'Error on_find event handler')
            else:
                log_func.warning(u'Not found for <%s>' % find_value)
        else:
            wxdlg_func.openWarningBox(_(u'WARNING'), _(u'No search bar selected'))
        event.Skip()

    def getCurDataObjFindRowIdx(self, dataset=None):
        """
        Get current data object find row index in dataset.
        """
        cur_find_ident = self.find_idents[self.find_ident_idx] if self.find_idents else None
        if cur_find_ident is not None:
            if dataset is None and self._data_obj:
                dataset = self._data_obj.getDataset()
            if dataset:
                ident_list = [record.get(self._data_obj.getIdentColumnName(), None) for record in dataset]
                try:
                    find_idx = ident_list.index(cur_find_ident)
                    # log_func.debug(u'Found <%s>. Index [%d]' % (cur_find_ident, find_idx), is_force_print=True)
                    return find_idx
                except ValueError:
                    log_func.warning(u'Not found identificator <%s> in <%s> dataset' % (cur_find_ident,
                                                                                        self._data_obj.getName()))
        return -1


COMPONENT = iqWxDataObjFindCtrl
