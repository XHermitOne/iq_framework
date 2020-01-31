#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Abstract project_name item class.
"""

from  iq.util import id_func

__version__ = (0, 0, 0, 1)


class iqProjectItem(object):
    """
    Abstract project_name item class.
    """
    def __init__(self, name=None, parent=None, description=u'',
                 img=None, img_extended=None, readonly=False):
        """
        Constructor.
        :param name: Item name.
        :param parent: Parent item object.
        :param description: Item description.
        :param img: Item image.
        :param img_extended: Extended item image.
        :param readonly: Read only state.
        """
        self.name = name
        self.parent = parent
        self.description = description
        self.img = img
        self.img_extended = img_extended
        self.readonly = readonly

    def default(self):
        """
        Default item initialization.
        """
        pass

    def getChildrenCount(self):
        """
        Number of children.
        """
        return 0

    def getChildren(self):
        """
        Children list.
        """
        return list()

    def design(self):
        """
        Start item designer.
        """
        pass

    def edit(self):
        """
        Start editing in the resource editor.
        """
        pass

    def rename(self, old_name, new_name):
        """
        Rename item.
        :param src_name: Old item name.
        :param new_item: New item name.
        """
        pass

    def create(self, new_name=None):
        """
        Create item.
        :param new_name: New item name.
        """
        return True

    def save(self):
        """
        Save item.
        """
        pass

    def load(self, filename):
        """
        Load item from file.
        :param filename: File name.
        """
        pass

    def extend(self):
        """
        Additional item tools.
        """
        pass

    def getRoot(self):
        """
        Root item.
        """
        return None

    def getParent(self):
        """
        Parent item.
        """
        return self.parent

    def cut(self):
        """
        Cut item.
        :return: Returns a pointer to a remote item.
        """
        # Delete first in the tree
        self.parent.delChild(self)
        return self

    def copy(self):
        """
        Copy item.
        :return: Returns a pointer to item..
        """
        new_item = self.__class__(self.parent)
        new_item.name = self.name + id_func.genNewId()
        new_item.description = self.description
        return new_item

    def paste(self, item):
        """
        Paste item.
        :param item: Project item.
        """
        if item:
            self.parent.addChild(item)
            return True
        return False

    def clone(self):
        """
        Clone item.
        """
        new_item_clone = self.copy()
        is_ok = self.paste(new_item_clone)
        if is_ok:
            return new_item_clone
        return None

    def delete(self):
        """
        Delete item.
        """
        return self.__class__.cut(self)

    def getPath(self):
        """
        Item path.
        """
        return None


