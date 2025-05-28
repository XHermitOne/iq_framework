#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XLSX file manipulate functions.
"""


from . import log_func

try:
    import xlsxwriter
except ImportError:
    log_func.error(u'Import error xlsxwriter. For install: pip3 install --break-system-packages --user XlsxWriter', is_force_print=True)

__version__ = (0, 0, 2, 1)

XLSX_EXT = '.xlsx'

DEFAULT_WORKSHEET_NAME = u'Sheet1'


def saveLinesToXlsxFile(xlsx_filename, worksheet_name=None, lines=None):
    """
    Save lines to XLSX file.

    :param xlsx_filename: XLSX file name.
    :param worksheet_name: Worksheet name.
    :param lines: List of line.
    :return: True/False.
    """
    if not lines:
        log_func.warning(u'Not defined data list for write to XLSX file <%s>' % xlsx_filename)
        return False

    try:
        # Workbook() takes one, non-optional, argument
        # which is the filename that we want to create.
        workbook = xlsxwriter.Workbook(xlsx_filename)

        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        if worksheet_name is None:
            worksheet_name = DEFAULT_WORKSHEET_NAME
        worksheet = workbook.add_worksheet(name=worksheet_name[:31])

        for i, line in enumerate(lines):
            # Use the worksheet object to write
            # data via the write() method.
            worksheet.write(i, 0, line)

        # Finally, close the Excel file
        # via the close() method.
        workbook.close()
        return True
    except:
        log_func.fatal(u'Error save to XLSX file <%s>' % xlsx_filename)
    return False
