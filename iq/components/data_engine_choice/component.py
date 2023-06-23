#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine choice component.
"""

from ... import object

from . import spc
from . import db_engine_choice

# from ...util import lang_func

__version__ = (0, 0, 0, 1)

# _ = lang_func.getTranslation().gettext


class iqDataEngineChoice(db_engine_choice.iqDBEngineChoiceManager, object.iqObject):
    """
    Data engine choice component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        db_engine_choice.iqDBEngineChoiceManager.__init__(self, *args, **kwargs)

    def getFilename(self):
        """
        Get data filename.
        """
        filename = self.getAttribute('filename')
        if filename is None:
            filename = self.genCustomDataFilename()
        return filename


COMPONENT = iqDataEngineChoice
