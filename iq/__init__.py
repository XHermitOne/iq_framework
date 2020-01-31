#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main engine package.
"""

from .config import *
from .util.global_func import *

from iq.kernel.kernel import createKernel
from iq.kernel.kernel import RUNTIME_MODE_STATE
from iq.kernel.kernel import EDITOR_MODE_STATE

__version__ = (0, 0, 1, 1)

