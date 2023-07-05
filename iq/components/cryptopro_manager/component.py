#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CryptoPro manager component.
"""

from ... import object

from . import spc
from . import cryptopro

__version__ = (0, 0, 0, 1)


class iqCryptoProManager(cryptopro.iqCryptoProManagerProto, object.iqObject):
    """
    CryptoProManager component.
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

        cryptopro.iqCryptoProManagerProto.__init__(self)

    def getFindPaths(self):
        """
        Get find CryptoPro console utilities paths.
        """
        find_paths = self.getAttribute('find_paths')

        if find_paths is None:
            find_paths = cryptopro.iqCryptoProManagerProto.getFindPaths(self)

        return find_paths


COMPONENT = iqCryptoProManager
