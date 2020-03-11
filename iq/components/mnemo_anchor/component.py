#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mnemoscheme anchor component.
"""

from ... import object
from ... import passport

from . import spc
from . import mnemoanchor

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqMnemoAnchor(object.iqObject, mnemoanchor.iqMnemoAnchorManager):
    """
    Mnemoscheme anchor component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)
        mnemoanchor.iqMnemoAnchorManager.__init__(self,
                                                  mnemoscheme=self.getParent(),
                                                  pos=self.getSVGPosition(),
                                                  size=self.getSVGSize(),
                                                  direction=self.getDirection(),
                                                  min_size=self.getMinSize(),
                                                  max_size=self.getMaxSize())

    def getDirection(self):
        """
        Indication of the direction of the anchor displacement relative to the anchor point.
        """
        return self.getAttribute('direction')

    def getSVGPosition(self):
        """
        Anchor reference position in SVG units.
        """
        return self.getAttribute('svg_pos')

    def getSVGSize(self):
        """
        Anchor cell size in SVG units.
        """
        return self.getAttribute('svg_size')

    def getMinSize(self):
        """
        Get minimum pixel size limit.
        """
        return self.getAttribute('min_size')

    def getMaxSize(self):
        """
        Get maximum pixel size limit.
        """
        return self.getAttribute('max_size')

    def getAttachmentPsp(self):
        """
        Get a passport of the control object attached to the anchor.
        """
        str_psp = self.getAttribute('attachment')
        return passport.iqPassport().setAsStr(str_psp)

    def getAttachment(self):
        """
        Get the control object attached to the anchor.

        :return: Control object, which can be placed on a mnemoscheme
            or None if error.
        """
        psp = self.getAttachmentPsp()

        if psp:
            name = psp.name
            parent = self.getParent()
            if parent.hasChild(name):
                return parent.getChild(name)
            else:
                log_func.error(u'Object <%s> is not a child of the mnemoscheme anchor <%s>' % (name, self.getName()))
        return None


COMPONENT = iqMnemoAnchor
