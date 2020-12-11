#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Prototype object class module.
"""
__version__ = (0, 0, 0, 1)

PROTOTYPE_ATTR_NAMES = ('name', '_children_', 'crc', 'value')


class iqVPrototype(object):
    """
    Virtual Excel object prototype class.
    """
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor.
        """
        self._parent = parent
        # Object attributes
        self._attributes = {}

    def getApp(self):
        """
        Application object.
        """
        if self._parent:
            return self._parent.getApp()
        return self

    def getData(self):
        """
        Get data.
        """
        if self._parent:
            return self._parent.getData()
        return None

    def getAttributes(self):
        """
        Get object attributes.
        """
        return self._attributes

    def setAttributes(self, data_attr={}):
        """
        Set object attributes.
        """
        self._attributes = data_attr
        return self._attributes

    def updateAttributes(self, data_attr={}):
        """
        Update object attributes.
        """
        self._attributes.update(data_attr)
        return self._attributes

    def create(self):
        """
        Create object.
        """
        attrs = self._parent.getAttributes()
        attrs['_children_'].append(self._attributes)
        return self._attributes

    def createIndex(self, idx):
        """
        Create object with index.
        """
        attrs = self._parent.getAttributes()
        attrs['_children_'].insert(idx, self._attributes)
        self._parent.setAttributes(attrs)
        return self._attributes

    def getParentByName(self, name):
        """
        Search for a parent by name.
        """
        if self._parent is None:
            return None
        elif 'name' in self._parent._attributes and self._parent._attributes['name'] == name:
            return self._parent
        else:
            return self._parent.getParentByName(name)

    def clear(self):
        """
        Clear object.
        """
        if '_children_' in self._attributes:
            self._attributes['_children_'] = []

    def copy(self):
        """
        Get object attributes copy.
        """
        pass

    def paste(self, paste, to=None):
        """
        Insert object attributes copy into curent object to the address.
        If to None, then there is a replacement.
        """
        pass

    def findChildAttrsByName(self, name=None):
        """
        Search for attributes of a child by name.

        :param name: Child name.
        :return: Dictionary of attributes of the child or None if not found.
        """
        children = [child for child in self._attributes['_children_'] if child['name'] == name]
        if children:
            return children[0]
        return None     
    
    def getParent(self):
        return self._parent


class iqVIndexedPrototype(iqVPrototype):
    """
    The prototype of the indexed object.
    Needed to implement index tracking and recalculation functions.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        iqVPrototype.__init__(self, parent, *args, **kwargs)

    def _maxElementIdx(self, element_name='', elements=None):
        """
        The maximum index of the specified item in the parent.
        Indexing starts at 0.
        """
        cur_idx = -1
        if elements is None:
            elements = [element for element in self._parent.getAttributes()['_children_']
                        if element['name'] == element_name]

        if elements:
            for i, element_attr in enumerate(elements):
                if 'Index' in element_attr:
                    cur_idx = int(element_attr['Index'])-1
                else:
                    if 'Span' in element_attr:
                        # Multiple items with the same attributes.
                        cur_idx += int(element_attr['Span'])
                    else:
                        cur_idx += 1
        return cur_idx

    def _findElementIdxAttr(self, idx, element_name):
        """
        Find the attributes of the specified element in the parent object by index.
        Indexing starts at 0.
        """
        indexes = []
        cur_idx = 0
        ret_i = -1
        ret_attr = None
        flag = True
        for i, element_attr in enumerate(self._parent.getAttributes()['_children_']):
            if element_attr['name'] == element_name:
                if 'Index' in element_attr:
                    cur_idx = int(element_attr['Index'])
                else:
                    cur_idx += 1

                indexes.append(cur_idx)

                # Combined cell accounting
                if idx == cur_idx and flag:
                    ret_i = i
                    ret_attr = element_attr
                    flag = False
                elif idx < cur_idx and flag:
                    ret_i = i
                    ret_attr = None
                    flag = False

        return indexes, ret_i, ret_attr

    def _reIndexElement(self, element_name, element, index, idx):
        """
        Reindexing the item in the parent.
        """
        if idx > 0:
            # Previous Items
            prev_elements = [element for element in self._parent.getAttributes()['_children_'][:idx - 1]
                             if element['name'] == element_name]
            if prev_elements:
                max_idx = self._maxElementIdx(element_name, prev_elements)
                if index > (max_idx + 1):
                    element.setIndex(index)
                return element
        if index > 1:
            element.setIndex(index)
        return element

    def _reIndexAllElements(self, element_names=(), offset_index=0):
        """
        Reindexing all elements in the parent.
        """
        all_elements = []
        for i, element_attr in enumerate(self._parent.getAttributes()['_children_']):
            if element_attr['name'] in element_names:
                if 'Index' in element_attr:
                    cur_idx = int(element_attr['Index'])
                else:
                    cur_idx += 1
                if 'Index' in element_attr:
                    element_attr['Index'] = cur_idx - offset_index
            all_elements.append(element_attr)
        return all_elements

    def getIndex(self):
        """
        The index of the indexed object in the parent object.
        """
        pass

    def setIndex(self, index):
        """
        The index of the object in the parent object.
        """
        self._attributes['Index'] = str(index)

    def _delElementIdxAttr(self, idx, element_name):
        """
        Delete the specified item from the parent by index.
        Indexing starts at 0.

        :return: True/False.
        """
        # Checking for coincidence of indexes is still done in Excel terms i.e. starts at 1
        idx += 1
        cur_idx = 0
        # children_count = len(self._parent.getAttributes()['_children_'])
        for i, element_attr in enumerate(self._parent.getAttributes()['_children_']):
            if element_attr['name'] == element_name:

                if 'Index' in element_attr:
                    cur_idx = int(element_attr['Index'])
                else:
                    cur_idx += 1

                if idx == cur_idx:
                    del self._parent.getAttributes()['_children_'][i]
                    self._parent.getAttributes()['_children_'] = self._reIndexAfterDel(element_name, i)
                    return True

                elif idx < cur_idx:
                    # Re-index after removal
                    self._reIndexAfterDel(element_name, i)
                    return True
        return False

    def _reIndexAfterDel(self, element_name, index):
        """
        Re-index after removal.
        """
        children = self._parent.getAttributes()['_children_']
        for element_attr in children[index:]:
            if element_attr['name'] == element_name:
                if 'Index' in element_attr:
                    element_attr['Index'] = int(element_attr['Index'])-1
        return children

    def _delElementIdxAttrChild(self, idx, element_name, bIsReIndex=True):
        """
        Delete the child of the specified item by index.
        Indexing starts at 0.

        :return: True/False.
        """
        # Checking for coincidence of indexes is still done in Excel terms i.e. starts at 1
        idx += 1
        cur_idx = 0
        delta = 1
        # children_count = len(self.getAttributes()['_children_'])
        for i, element_attr in enumerate(self.getAttributes()['_children_']):
            if element_attr['name'] == element_name:

                if 'Index' in element_attr:
                    cur_idx = int(element_attr['Index'])
                else:
                    cur_idx += 1

                if idx == cur_idx:
                    element = self.getAttributes()['_children_'][i]
                    if 'MergeAcross' in element:
                        delta += int(element['MergeAcross'])

                    if not bIsReIndex:
                        self.getAttributes()['_children_'] = self._reIndexBeforeClearChild(element_name, i, delta)
                    del self.getAttributes()['_children_'][i]
                    if bIsReIndex:
                        self.getAttributes()['_children_'] = self._reIndexAfterDelChild(element_name, i, delta)
                    return True

                elif idx < cur_idx:
                    # Re-index after removal
                    if bIsReIndex:
                        self._reIndexAfterDelChild(element_name, i, delta)
                    return True
        return False

    def _reIndexAfterDelChild(self, element_name, index, delta=1):
        """
        Re-index child elements after deletion.
        """
        children = self.getAttributes()['_children_']
        for element_attr in children[index:]:
            if element_attr['name'] == element_name:
                if 'Index' in element_attr:
                    element_attr['Index'] = int(element_attr['Index']) - delta
        return children

    def _reIndexBeforeClearChild(self, element_name, index, delta=1):
        """
        Re-index child elements until the element is cleared for merging.
        """
        children = self.getAttributes()['_children_']
        for element_attr in children[index + 1:]:
            if element_attr['name'] == element_name:
                if 'Index' not in element_attr:
                    element_attr['Index'] = self._maxElementIdx(element_name, children[:index + 2]) + delta
                break
        return children

    def _findElementIdxAttrChild(self, idx, element_name):
        """
        Find attributes of a child by index.
        Indexing starts at 0.
        """
        indexes = []
        cur_idx = 0
        # ret_i = -1
        ret_attr = None
        flag = True
        for i, element_attr in enumerate(self.getAttributes()['_children_']):
            if element_attr['name'] == element_name:
                if 'Index' in element_attr:
                    cur_idx = int(element_attr['Index'])
                else:
                    cur_idx += 1

                # Combined cell accounting
                indexes.append(cur_idx)

                if idx == cur_idx and flag:
                    # ret_i = i
                    ret_attr = element_attr
                    flag = False
                elif idx < cur_idx and flag:
                    # ret_i = i
                    ret_attr = None
                    flag = False

        return indexes, ret_attr
