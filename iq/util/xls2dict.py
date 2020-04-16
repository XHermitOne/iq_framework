#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Excel file converter module in xls to dictionary format.
"""

# --- Подключение библиотек ---
import os.path
import sys
import win32api
import win32com.client
import pythoncom

from . import xml2dict

__version__ = (0, 0, 0, 1)

# XML Excel file format
xlXMLSpreadsheet = 46


def XlsFile2Dict(xls_filename):
    """
    Function to convert Excel files in xls format to Python dictionary format.

    :param xls_filename: xls file name.
    :return: The function returns a completed dictionary,
        or None if error.
    """
    try:
        xls_filename = os.path.abspath(xls_filename)
        xml_file_name = os.path.splitext(xls_filename)[0] + '.xml'
        # Connect with Excel
        excel_app = win32com.client.Dispatch('Excel.Application')
        # Make the application invisible
        excel_app.Visible = 0
        # Close all books
        excel_app.Workbooks.Close()
        # Open *.xls file
        excel_app.Workbooks.Open(xls_filename)
        # Save to xml file
        excel_app.ActiveWorkbook.SaveAs(xml_file_name, FileFormat=xlXMLSpreadsheet)
        # Quit Excel
        excel_app.Quit()

        return xml2dict.XmlFile2Dict(xml_file_name)
    except pythoncom.com_error:
        info = sys.exc_info()[1].args[2][2]
        win32api.MessageBox(0, u'Error read file %s : %s.' % (xls_filename, info))
        return None

    except:
        info = sys.exc_info()[1]
        win32api.MessageBox(0, u'Error read file %s : %s.' % (xls_filename, info))
        return None
