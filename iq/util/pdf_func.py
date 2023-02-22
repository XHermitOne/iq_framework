#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF file functions.
"""

import os.path

from . import log_func
from . import sys_func
from . import exec_func
from . import file_func
from . import printer_func

__version__ = (0, 0, 1, 1)


PDF_FILENAME_EXT = '.pdf'

DEFAULT_PDF_VIEWER = 'evince'
DEFAULT_PDF_PRINT_SYSTEM = 'lpr'


def viewPDF(pdf_filename):
    """
    View PDF file in viewer.

    :param pdf_filename: PDF filename.
    :return: True/False.
    """
    if not os.path.exists(pdf_filename):
        log_func.warning(u'PDF file <%s> not found' % pdf_filename)
        return False

    try:
        if sys_func.isLinuxPlatform():
            cmd = '%s %s &' % (DEFAULT_PDF_VIEWER, pdf_filename)
            return exec_func.execSystemCommand(cmd)
        elif sys_func.isWindowsPlatform():
            log_func.warning(u'Not support view PDF file <%s> on Windows platform' % pdf_filename)
    except:
        log_func.fatal(u'Error view PDF file <%s>' % pdf_filename)
    return False


def printPDF(pdf_filename, printer_name=None):
    """
    Print PDF file.

    :param pdf_filename: PDF filename.
    :param printer_name: Printer name.
    :return: True/False.
    """
    if not os.path.exists(pdf_filename):
        log_func.warning(u'PDF file <%s> not found' % pdf_filename)
        return False

    try:
        if sys_func.isLinuxPlatform():
            if printer_name:
                cmd = '%s -o fit-to-page -P "%s" %s' % (DEFAULT_PDF_PRINT_SYSTEM, printer_name, pdf_filename)
            else:
                cmd = '%s -o fit-to-page %s' % (DEFAULT_PDF_PRINT_SYSTEM, pdf_filename)
            return exec_func.execSystemCommand(cmd)
        elif sys_func.isWindowsPlatform():
            log_func.warning(u'Not support print PDF file <%s> on Windows platform' % pdf_filename)
    except:
        log_func.fatal(u'Error print PDF file <%s>. Printer <%s>' % (pdf_filename, printer_name))
    return False


def joinPDF(src_pdf_filenames, dst_pdf_filename):
    """
    Join PDF files into one.

    :param src_pdf_filenames: List of source files.
        All files must be present!
        Otherwise, they will not be added to the resulting one.
    :param dst_pdf_filename: The full name of the resulting PDF file.
    :return: True/False.
    """
    try:
        pdf_filenames_str = ' '.join(['\'%s\'' % pdf_filename for pdf_filename in src_pdf_filenames if os.path.exists(pdf_filename)])

        cmd = 'pdftk %s cat output \'%s\'' % (pdf_filenames_str, dst_pdf_filename)

        log_func.debug(u'PDF join command <%s>' % cmd)
        os.system(cmd)

        if os.path.exists(dst_pdf_filename):
            return True
        else:
            log_func.warning(u'Error join PDF file <%s>' % dst_pdf_filename)
    except:
        log_func.fatal(u'Error join PDF file')
    return False


DEFAULT_COMPRESSED_FILENAME = 'compress.pdf'


def compressCupsPDF(pdf_filename, new_pdf_filename=None):
    """
    An attempt to reduce the size of a PDF file.
        PDF file compression is performed via CUPS-PDF virtual printer
        For compression in the PDF printer settings in /etc/cups/cups-pdf.conf
        the parameter -dPDFSETTINGS db is set as /ebook which corresponds to 150dpi
        Other parameter values:
        /screen - 72dpi
        /ebook - 150dpi
        /printer - 300dpi
        /prepress - color300dpi

    :param pdf_filename: Compressible PDF file.
    :param new_pdf_filename: A new PDF file.
        If not specified, the existing PDF file is overwritten.
    :return: True/False.
    """
    try:
        log_func.info(u'Compress PDF file <%s> by CUPS-PDF' % pdf_filename)
        log_func.info(u'\tTo compress in the PDF printer settings in /etc/cups/cups-pdf.conf')
        log_func.info(u'\tparameter -dPDFSETTINGS set as /ebook which corresponds to 150dpi')

        if printer_func.isCupsPDF():
            dst_pdf_filename = printer_func.printToCupsPDF(pdf_filename)
            if dst_pdf_filename:
                if new_pdf_filename is None:
                    file_func.copyFile(dst_pdf_filename, pdf_filename)
                else:
                    file_func.copyFile(dst_pdf_filename, new_pdf_filename)
                file_func.removeFile(dst_pdf_filename)
                return True
        else:
            log_func.warning(u'The CUPS-PDF printer installed in the system for PDF file compression was not found <%s>' % pdf_filename)
    except:
        log_func.fatal(u'PDF file compression error <%s>' % pdf_filename)
    return False


def compressGhostscriptPDF(pdf_filename, new_pdf_filename=None,
                           quality=printer_func.GS_QUALITY_DEFAULT):
    """
    An attempt to reduce the size of a PDF file.
        The PDF file is compressed via Ghostscript.

    :param pdf_filename: Compressible PDF file.
    :param new_pdf_filename: New PDF file.
        If not specified, the existing PDF file is overwritten.
    :param quality: Print quality.
        GS_QUALITY_PREPRESS = 'prepress'    (Color 300dpi)
        GS_QUALITY_PRINTER = 'printer'      (300dpi)
        GS_QUALITY_EBOOK = 'ebook'          (150dpi)
        GS_QUALITY_SCREEN = 'screen'        (72dpi)
    :return: True/False.
    """
    try:
        log_func.info(u'PDF file compression <%s> by Ghostscript' % pdf_filename)

        dst_pdf_filename = printer_func.printToGhostscriptPDF(pdf_filename, new_pdf_filename,
                                                              quality=quality)
        if dst_pdf_filename:
            return True
    except:
        log_func.fatal(u'Error PDF file compression <%s> by Ghostscript' % pdf_filename)
    return False
