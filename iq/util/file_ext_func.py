#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File extended functions.
"""

from . import file_func
from . import log_func

__version__ = (0, 0, 1, 1)

PDF_FILENAME_EXT = ('.pdf', )
IMG_FILENAME_EXT = ('.png', '.jpg', '.jpeg', '.gif')
OFFICE_FILENAME_EXT = ('.doc', '.docx', '.xls', '.xlsx', '.odt', '.ods')


def viewFileByExt(filename):
    """
    View file in program by extension.

    :param filename: Full file name path.
    :return: True/False.
    """
    filename_ext = file_func.getFilenameExt(filename)
    if filename_ext:
        filename_ext = filename_ext.lower()
        if filename_ext in PDF_FILENAME_EXT:
            from . import pdf_func
            return pdf_func.viewPDF(pdf_filename=filename)

        elif filename_ext in IMG_FILENAME_EXT:
            from . import img_func
            return img_func.viewImage(img_filename=filename)

        elif filename_ext in OFFICE_FILENAME_EXT:
            from . import office_func
            return office_func.openInLibreOffice(filename)
        else:
            log_func.warning(u'Not supported view file type <%s>' % filename_ext)
    else:
        log_func.warning(u'Not defined ext of filename <%s>' % filename)
    return False
