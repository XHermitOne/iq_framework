#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mnemoscheme component.
"""

from . import spc
from . import mnemoscheme

from .. import mnemo_anchor

from .. import wx_panel

__version__ = (0, 0, 0, 1)


class iqMnemoScheme(wx_panel.COMPONENT, mnemoscheme.iqMnemoSchemeManager):
    """
    Mnemoscheme component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        wx_panel.COMPONENT.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)
        mnemoscheme.iqMnemoSchemeManager.__init__(self, *args, **kwargs)

    def getAnchors(self):
        """
        List of mnemonic anchors.
        """
        children = self.getChildren()
        return [child for child in children if isinstance(child, mnemo_anchor.COMPONENT)]

    def getControls(self):
        """
        List of active mnemonic controls.
        """
        children = self.getChildren()
        return [child for child in children if not isinstance(child, mnemo_anchor.COMPONENT)]

    def layoutAll(self, auto_refresh=True):
        """
        The method of arranging and dimensioning controls mnemonic diagrams according to the anchors.

        :param auto_refresh: Automatically refresh the mnemoscheme object.
        :return: True/False.
        """
        anchors = self.getAnchors()
        result = all([anchor.layoutControl() for anchor in anchors])

        if auto_refresh:
            self.Refresh()

        return result


COMPONENT = iqMnemoScheme
