#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DBF readonly file component.
"""

from ...object import object_proto

from . import spc
from . import dbf_readonly

__version__ = (0, 0, 0, 1)


class iqDBFReadOnlyFile(dbf_readonly.iqDBFReadOnlyFile, object_proto.iqObject):
    """
    DBF readonly file component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object_proto.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        dbf_readonly.iqDBFReadOnlyFile.__init__(self, dbf_filename=self.getDBFFileName())

    def getDBFFileName(self):
        """
        Get DBF filename.
        """
        if self._dbf_file_name is None:
            self._dbf_file_name = self.getAttribute('dbf_filename')
        return self._dbf_file_name


COMPONENT = iqDBFReadOnlyFile
