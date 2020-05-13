#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cataloger component package.

Cataloger - an object that takes a file or line, parses it and
saves the result in a physical directory.

There is physic catalog and logic catalog.

Physic catalog - physical structure of data storage.
For example: folders and files.

Logic catalog - catalog with excellent (from the physical catalog)
catalog nesting order (catalog level).
Catalog level - type of directory folders at one level,
defining one of the features of a cataloged object.

For example:
Physic path:
    /partner/year/document type/file-object
        ^        ^        ^            ^
        It is catalog levels           |
                                Catalogable object

Logic path:
    /document type/year/partner/file-object
          ^        ^        ^           ^
          It is catalog levels          |
                                Catalogable object

Objects are stored on the physical path, but you can access them
both in physical and logical ways.
"""

from .spc import SPC
from .spc import COMPONENT_TYPE
from .component import COMPONENT

__version__ = (0, 0, 0, 1)
