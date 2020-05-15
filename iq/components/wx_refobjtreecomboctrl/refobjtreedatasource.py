#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ref object data source as tree data.
"""

import iq

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqRefObjItemDataSource(object):
    """
    Ref object item.
    """
    def __init__(self, parent_item, cod):
        """
        Constructor.

        :param parent_item: Parent item.
        """
        self._parent_item = parent_item
        self._code = cod

        # Item data
        self._data = None
        self._children = None

    def __getitem__(self, i):
        return self.getChildren()[i]

    def __len__(self):
        return len(self.getChildren())

    def getRoot(self):
        """
        Get root item.
        """
        if self.isRoot():
            return self
        else:
            parent = self.getParent()
            if parent:
                return parent.getRoot()
        return None

    def isRoot(self):
        """
        Validation is the current root element.
        """
        return self.getParent() is None

    def getRecDict(self):
        """
        Data item as a dictionary.
        """
        ref_obj = self.getRoot().getRefObj()
        if ref_obj:
            storage = ref_obj.getStorage()
            if storage:
                rec_dict = storage.getRecByCod(self.getCode())
                return rec_dict
        return None
        
    def getCode(self):
        """
        Ref object code, corresponding to this item.
        """
        return self._code
        
    def getParent(self):
        """
        Get parent item.
        """
        return self._parent_item
        
    def setData(self, data):
        """
        Set item data.
        """
        self._data = data
        
    def getDescription(self):
        """
        Get item description.
        """
        root = self.getRoot()
        ref_obj = root.getRefObj()
        if ref_obj:
            storage = ref_obj.getStorage()
            level_idx = ref_obj.getLevelByCod(self.getCode()).getIndex()
            rec = storage.getSpravFieldDict(self._data, level_idx=level_idx)
            return rec['name']
        return u'Unknown'
    
    def getLabel(self, label_func=None):
        """
        Get item label.
        """
        if label_func:
            return label_func
        return self.getDescription()

    def hasChildren(self):
        """
        Does the item have child items?
        """
        root = self.getRoot()
        ref_obj = root.getRefObj()
        if ref_obj:
            return ref_obj.isSubCodes(self._code)
        return False

    def _loadChildren(self, cod=None, auto_sort=True):
        """
        Load children data.

        :param auto_sort: Sort entries automatically by code?
        :return: Returns a list of objects of child items.
        """
        children = []
        root = self.getRoot()
        ref_obj = root.getRefObj()
        if ref_obj:
            level_idx = ref_obj.getLevelByCod(cod).getIndex() + 1 if cod else 0
            storage = ref_obj.getStorage()
            tab_data = storage.getLevelTable(cod)
            if auto_sort:
                try:
                    i_cod = storage.getSpravFieldNames(level_idx=level_idx).index('cod')
                    tab_data = sorted(tab_data, key=lambda rec: rec[i_cod])
                except ValueError:
                    log_func.fatal(u'Error sort by cod. Level [%d]' % level_idx)

            for rec in tab_data:
                rec_dict = storage.getSpravFieldDict(rec, level_idx=level_idx)
                child_code = rec_dict['cod']
                if ref_obj.isActive(child_code):
                    item = iqRefObjItemDataSource(self, child_code)
                    item.setData(rec)
                
                    children.append(item)
        
        return children

    def getChildren(self):
        """
        Get children items.
        """
        if self._children is None:
            self._children = self._loadChildren(self._code)
        return self._children
  
    def getLevelIdx(self):
        """
        Get ref obj level index, to which the item belongs.
        """
        ref_obj = self.getRoot().getRefObj()
        if ref_obj:
            cod = self.getCode()
            level = ref_obj.getLevelByCod(cod)
            if level:
                return level.getIndex()
        return -1

    def findItemByCode(self, cod):
        """
        Find item by cod.

        :return: Tree item or None if not found.
        """
        find_child = None
        for child in self.getChildren():
            if child.getCode() == cod:
                return child
            if child.hasChildren():
                find_child = child.findItemByCode(cod)
                if find_child is not None:
                    return find_child
        return None


class iqRefObjTreeDataSource(object):
    """
    Reference object data source as tree.
    """
    def __init__(self, refobj_psp, root_code=None):
        """
        Constructor.

        :param refobj_psp: Ref object passport.
        :param root_code: Root item code.
        """
        self._ref_object = self._createRefObj(refobj_psp)
        self._children = self._loadChildren(root_code)

    def getRefObj(self):
        """
        Ref object.
        """
        return self._ref_object

    def getRefObjDescription(self):
        """
        Ref object description.
        """
        return self._ref_object.getDescription() if self._ref_object else None

    def _createRefObj(self, refobj_psp):
        """
        Create ref object.
        """
        kernel = iq.getKernel()
        if kernel:
            return kernel.Create(refobj_psp)
        return None
    
    def _loadChildren(self, cod=None):
        """
        Load children items data.

        :return: Children item list.
        """
        children = []
        if self._ref_object:
            storage = self._ref_object.getStorage()
            tab_data = storage.getLevelTable(cod)
            for rec in tab_data or []:
                level_idx = self._ref_object.getLevelByCod(cod).getIndex() + 1 if cod else 0
                rec_dict = storage.getSpravFieldDict(rec, level_idx=level_idx)
                child_code = rec_dict['cod']

                item = iqRefObjItemDataSource(self, child_code)
                item.setData(rec)
                children.append(item)
        
        return children
        
    def getChildren(self):
        """
        Get children items.
        """
        return self._children
    
    def find(self, find_text):
        """
        Find item label by text.

        :return: Found item label or None if item not found.
        """
        if self._ref_object:
            cod = find_text
            find_dict = self._ref_object.Find(cod, ['cod', 'name'])
            if not find_dict:
                label = None
            else:
                label = find_dict['name']
            return label
        return None
    
    def findRecord(self, find_text, field_name=None):
        """
        Find record by field value.

        :param find_text: Find value as text.
        :param field_name: Field name if None, then find by cod.
        :return: Record dictionary or None if not found.
        """
        if self._ref_object:
            if field_name is None:
                rec_dict = self._ref_object.getRec(find_text)
            else:
                rec_dict = self._ref_object.getStorage().getRecByFieldValue(field_name, find_text)
            return rec_dict
        return None

    def findItemByCode(self, cod):
        """
        Find recursive item by cod.

        :param cod: Cod.
        :return: Tree item or None if not found.
        """
        for child in self.getChildren():
            if child.getCode() == cod:
                return child
            if child.hasChildren():
                find_child = child.findItemByCode(cod)
                if find_child is not None:
                    return find_child
        return None
