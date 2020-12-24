#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ref object data source as tree data.
"""

import operator

import iq

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqRefObjItemDataSourceBase(object):
    """
    Base class.
    """
    def getData(self):
        """
        Item data.
        """
        assert None, 'Abstract method getData in class %s!' % self.__class__.__name__

    def setData(self, item_data):
        """
        Set item data.
        """
        assert None, 'Abstract method setData in class %s!' % self.__class__.__name__

    def getChildren(self):
        """
        Get children items.
        """
        assert None, 'Abstract method getChildren in class %s!' % self.__class__.__name__

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

    def getParent(self):
        """
        Get parent item.
        """
        assert None, 'Abstract method getParent in class %s!' % self.__class__.__name__

    def hasChildren(self):
        """
        Does the item have child items?
        """
        assert None, 'Abstract method hasChildren in class %s!' % self.__class__.__name__


class iqRefObjItemDataSource(iqRefObjItemDataSourceBase):
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
            rec = self._data
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
            return ref_obj.hasChildrenCodes(self._code)
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
            tab_data = ref_obj.getLevelRecsByCod(cod)
            if auto_sort:
                try:
                    tab_data = sorted(tab_data, key=lambda rec: rec[ref_obj.getCodColumnName()])
                except ValueError:
                    log_func.fatal(u'Error sort by cod [%s]' % cod)

            for rec in tab_data:
                child_code = rec[ref_obj.getCodColumnName()]
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
            return ref_obj.getLevelIdxByCod(cod)
        return -1

    def findItemByCode(self, cod):
        """
        Find item by cod.

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

    def findItemByLabel(self, label):
        """
        Find item by label.

        :return: Tree item or None if not found.
        """
        for child in self.getChildren():
            if child.getLabel() == label:
                return child
            if child.hasChildren():
                find_child = child.findItemByLabel(label)
                if find_child is not None:
                    return find_child
        return None


class iqRefObjTreeDataSource(iqRefObjItemDataSourceBase):
    """
    Reference object data source as tree.
    """
    def __init__(self, refobj_psp, root_code=None, sort_col=None):
        """
        Constructor.

        :param refobj_psp: Ref object passport.
        :param root_code: Root item code.
        :param sort_col: Sort column name.
        """
        self._sort_column = sort_col

        self._ref_object = self._createRefObj(refobj_psp)
        self._children = self._loadChildren(root_code)

    def getParent(self):
        """
        Parent item.
        Tree root has no parent.
        """
        return None

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
            return kernel.createByPsp(psp=refobj_psp)
        return None
    
    def _loadChildren(self, cod=None):
        """
        Load children items data.

        :return: Children item list.
        """
        children = list()
        if self._ref_object:
            tab_data = self._ref_object.getLevelRecsByCod(parent_cod=cod)

            # Sort dataset by column
            if self._sort_column:
                try:
                    tab_data = sorted(tab_data,
                                      key=operator.itemgetter(self._sort_column))
                except:
                    log_func.fatal(u'Error sort dataset by column <%s>' % self._sort_column)

            for rec in tab_data or list():
                child_code = rec[self._ref_object.getCodColumnName()]

                item = iqRefObjItemDataSource(parent_item=self, cod=child_code)
                item.setData(rec)
                children.append(item)
        
        return children
        
    def getChildren(self):
        """
        Get children items.
        """
        return self._children
    
    def find(self, find_text, find_column='name'):
        """
        Find item label by text.

        :param find_text: Find text.
        :param find_column: Find ref object column.
        :return: Found item label or None if item not found.
        """
        if self._ref_object:
            # cod = find_text
            # find_dict = self._ref_object.Find(cod,
            #                                   [self._ref_object.getCodColumnName(),
            #                                    self._ref_object.getNameColumnName()])
            find_dict = self._ref_object.findRecByColContent(column_name=find_column,
                                                             search_text=find_text)
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
                rec_dict = self._ref_object.getRecByCod(find_text)
            else:
                rec_dict = self._ref_object.getRecByColValue(field_name, find_text)
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

    def findItemByLabel(self, label):
        """
        Find recursive item by label.

        :param label: Find item label.
        :return: Tree item or None if not found.
        """
        for child in self.getChildren():
            if child.getLabel() == label:
                return child
            if child.hasChildren():
                find_child = child.findItemByLabel(label)
                if find_child is not None:
                    return find_child
        return None
