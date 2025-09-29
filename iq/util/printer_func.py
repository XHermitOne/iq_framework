#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Printer functions.

Printing is done by the utility lpr.
For example:
lpr -o fit-to-page -P "PrinterName" /.nixprint/print.pdf

Additional printing options for each printer can be found using the utility lpoptions.
For example:
lpoptions -p <Printer name> -l
lpoptions -p WorkCentre-5325 -l

To work with CUPS-PDF virtual printer, a package is required cups-pdf:
sudo apt install cups-pdf
or
sudo apt install printer-driver-cups-pdf
"""

import os
import os.path
import subprocess
import locale
import time

from . import log_func

from . import file_func
from . import str_func

__version__ = (0, 2, 1, 2)

NO_DEFAULT_PRINTER_MSG = 'no system default destination'
PDF_EXT = '.pdf'
GRAPH_FILE_EXT = ('.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.png', '.gif')
# Options for waiting for the printer to finish printing
TIMEOUT_BUSY_PRINTER = 5
TIMEOUT_COUNT_BUSY_PRINTER = 20


def _getExecCmdStdoutLines(cmd):
    """
    Execute the OS command and return a list of output stream lines.

    :param cmd: Command as string or list.
        For example:
        'lpstat -d' or ('lpstat', '-d')
    :return: Lines as list. Empty list if error.
    """
    if isinstance(cmd, str):
        cmd = cmd.split(u' ')
    if not isinstance(cmd, tuple) and not isinstance(cmd, list):
        log_func.warning(u'Not supported command type <%s>' % str(cmd))
        return list()

    lines = list()
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        b_lines = process.stdout.readlines()
        console_encoding = locale.getpreferredencoding()
        lines = [line.decode(console_encoding).strip() for line in b_lines]
    except:
        log_func.fatal(u'Error execute OS command <%s>' % cmd)
    return lines


def noDefaultPrinter(lpstat_result=None):
    """
    Checking for the default printer in the system.

    :param lpstat_result: lpstat -d result. If None, the function will call the command itself.
    :return: True-there is no default printer, False - there is a default printer.
    """
    if lpstat_result is None:
        cmd = ('lpstat', '-d')
        lines = _getExecCmdStdoutLines(cmd)
        lpstat_result = lines[0]

    if lpstat_result:
        return lpstat_result.lower().strip() == NO_DEFAULT_PRINTER_MSG
    return False


def getDefaultPrinter():
    """
    The default printer name.

    :return: The default printer name or None, if not installed.
    """
    cmd = ('lpstat', '-d')
    lines = _getExecCmdStdoutLines(cmd)

    if (not lines) or noDefaultPrinter(lines[0]):
        return None
    else:
        if ':' not in lines[0]:
            log_func.warning(u'No default printer. Message <%s>' % lines[0])
            return None
        result = lines[0].split(': ')[1].strip()
        return result


def getPrinterDevices():
    """
    Get a list of printer devices.
    The function works through the utility lpstat.

    :return: [(Printer name, connection address),...].
    """
    cmd = ('lpstat', '-v')
    lines = _getExecCmdStdoutLines(cmd)
    if not lines:
        return None
    else:
        result = [printer.split(' ') for printer in lines]
        result = [(device[2][:-1], device[3]) for device in result]
        return result


def getNetworkPrinters():
    """
    List of network printer names.

    :return: A list of printer name strings that have a network address.
    """
    printer_devices = getPrinterDevices()
    return [device[0] for device in printer_devices if device[1].startswith('ipp://') or device[1].startswith('socket://')]


def getPrinters():
    """
    Get a list of installed printers.
    The function works through the utility lpstat.

    :return: Printer names.
    """
    cmd = ('lpstat', '-a')
    lines = _getExecCmdStdoutLines(cmd)
    if not lines:
        return None
    else:
        result = [printer.split(' ')[0] for printer in lines]
        return result


def getPrintersInfo():
    """
    Get information about printers.

    :return: [(By default?, Printer name, Network printer?),...].
    """
    printers = getPrinters()
    network_printers = getNetworkPrinters()

    if printers is None:
        return None
    else:
        default_printer = getDefaultPrinter()
        return [(printer == default_printer, printer, printer in network_printers) for printer in printers]


def printPDF(pdf_filename, printer_name=None, copies=1):
    """
    Send a PDF file for printing.

    :type pdf_filename: C{string}
    :param pdf_filename: PDF file name for printing.
    :type printer_name: C{string}
    :param printer_name: Printer name. If not specified, then to print the default printer.
    :param copies: The number of copies.
    :return: True - the file has been sent for printing, False - no.
    """
    if not os.path.exists(pdf_filename):
        log_func.warning('PDF file %s not exists' % pdf_filename)
        return False

    if printer_name is None:
        printer_name = getDefaultPrinter()

    if printer_name:
        cmd = 'lpr -o fit-to-page -P "%s" %s' % (printer_name, pdf_filename)
    else:
        cmd = 'lpr -o fit-to-page %s' % pdf_filename

    for i in range(copies):
        os.system(cmd)
    return True


def toPDF(filename):
    """
    Convert the file to PDF if possible.

    :param filename: The full name of the printed file.
    :return: The name of the PDF file or None if conversion is not possible.
    """
    filename_ext = os.path.splitext(filename)[1].lower()
    if filename_ext == PDF_EXT:
        # PDF
        return filename
    elif filename_ext in GRAPH_FILE_EXT:
        # Graphic files
        pdf_filename = os.path.splitext(filename)[0] + PDF_EXT
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)
        cmd = 'convert %s %s' % (filename, pdf_filename)
        os.system(cmd)
        return pdf_filename
    log_func.warning(u'Not supported convert to PDF <%s>' % filename)
    return None


def printFile(filename, printer_name=None, copies=1):
    """
    Print the file.
        Files are recognized by extension.
        PDF files are printed by the print PDF function.
        First we convert graphic files to PDF
        and then we print it as a regular PDF.

    :param filename: The full name of the printed file.
    :param printer_name: The name of the printer to print. If not specified, then
        to print the default printer.
    :param copies: The number of copies.
    :return: True - the file has been sent for printing, False - no.
    """
    pdf_filename = toPDF(filename)
    return printPDF(pdf_filename, printer_name, copies)


DEFAULT_CUPS_PDF_DIRNAME = 'PDF'
DEFAULT_CUPS_PDF_DEVICE = 'cups-pdf:'


def printToCupsPDF(filename, printer_name=None, copies=1):
    """
    Printing a file to a CUPS-PDF virtual printer.
        For printing documents with Cyrillic file names
        you need to set in /etc/cups/cups-pdf.conf
        TitlePref 1 and DecodeHexStrings 1

    :param filename: The full name of the printed file.
    :param printer_name: The name of the printer to print.
        By default, the CUPS-PDF printer is called PDF.
    :param copies: The number of copies.
    :return: The new name of the printed PDF file or None in case of an error.
    """
    if printer_name is None:
        printer_name = getCupsPDFPrinterName()
        if printer_name is None:
            log_func.warning(u'CUPS-PDF printer is not installed in the system')
            return None

    log_func.info(u'For printing documents with Cyrillic file names')
    log_func.info(u'\tyou need to set in /etc/cups/cups-pdf.conf')
    log_func.info(u'\tTitlePref 1 and DecodeHexStrings 1')

    result = printFile(filename=filename, printer_name=printer_name, copies=copies)

    if result:
        pdf_out_path = os.path.join(file_func.getHomePath(), DEFAULT_CUPS_PDF_DIRNAME)
        if not os.path.exists(pdf_out_path):
            log_func.warning(u'CUPS PDF printer path not found <%s>' % pdf_out_path)
            return None

        new_pdf_filename = os.path.join(pdf_out_path,
                                        os.path.splitext(os.path.basename(filename))[0] + PDF_EXT)

        # Необходимо подождать окончания печати
        if waitBusyPrinter(printer_name) and os.path.exists(new_pdf_filename):
            return new_pdf_filename

        log_func.warning(u'The resulting PDF print file <%s> not created' % new_pdf_filename)
    return None


def waitBusyPrinter(printer_name):
    """
    Waiting for the printer to finish printing.

    :param printer_name: Printer name.
    :return: True - the printer is free after printing.
        False - the waiting time has ended (the timeout has triggered).
    """
    for i_timeout in range(TIMEOUT_COUNT_BUSY_PRINTER):
        log_func.debug(u'Waiting for the PDF printer to print: %d' % i_timeout)
        if isBusyPrinter(printer_name):
            time.sleep(TIMEOUT_BUSY_PRINTER)
        else:
            break
    return not isBusyPrinter(printer_name)


def isCupsPDF():
    """
    Check if the CUPS-PDF printer is installed in the system?

    :return: True - installed, False - not installed.
    """
    printer_devices = getPrinterDevices()
    return any([printer_dev.startswith(DEFAULT_CUPS_PDF_DEVICE) for printer_name, printer_dev in printer_devices])


def getCupsPDFPrinterName():
    """
    Get the name of the CUPS-PDF printer if it is installed.

    :return: CUPS-PDF printer name or None if the printer is not installed.
    """
    printer_devices = getPrinterDevices()
    find_cups_pdf_printer_name = [printer_name for printer_name, printer_dev in printer_devices if printer_dev.startswith(DEFAULT_CUPS_PDF_DEVICE)]
    return find_cups_pdf_printer_name[0] if find_cups_pdf_printer_name else None


def isBusyPrinter(printer_name):
    """
    Checking a busy printer.
    The function works by lpstat utility.

    :param printer_name: Printer name.
    :return: True - the printer is busy / False - the printer is free.
    """
    cmd = ('lpstat', '-p', printer_name)
    lines = _getExecCmdStdoutLines(cmd)

    if not lines:
        return None
    else:
        result = any([str_func.isWordsInText(text=printer, words=(u'свободен', 'free')) for printer in lines])
        return not result


# Print quality Ghostscript
GS_QUALITY_DEFAULT = 'default'
GS_QUALITY_PREPRESS = 'prepress'    # Color 300dpi
GS_QUALITY_PRINTER = 'printer'      # 300dpi
GS_QUALITY_EBOOK = 'ebook'          # 150dpi
GS_QUALITY_SCREEN = 'screen'        # 72dpi


def printToGhostscriptPDF(filename, new_pdf_filename=None, quality=GS_QUALITY_DEFAULT):
    """
    Printing a file using Ghostscript to PDF.

    :param filename: The full name of the printed file.
    :param new_pdf_filename: The name of the resulting PDF file.
        If not specified, the resulting file is overwritten.
    :param quality: Print quality
        GS_QUALITY_PREPRESS = 'prepress'    (Color 300dpi)
        GS_QUALITY_PRINTER = 'printer'      (300dpi)
        GS_QUALITY_EBOOK = 'ebook'          (150dpi)
        GS_QUALITY_SCREEN = 'screen'        (72dpi)
    :return: The new name of the printed PDF file or None in case of an error.
    """
    try:
        pdf_filename = toPDF(filename)
        dst_pdf_filename = os.path.join(os.path.dirname(pdf_filename),
                                        '_'+os.path.basename(pdf_filename)) if new_pdf_filename is None else new_pdf_filename

        cmd = ('gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
               '-dPDFSETTINGS=/{}'.format(quality),
               '-dNOPAUSE', '-dQUIET', '-dBATCH',
               '-sOutputFile={}'.format(dst_pdf_filename),
               pdf_filename)
        subprocess.call(cmd)

        if not os.path.exists(dst_pdf_filename):
            log_func.warning(u'Intermediate print file not formed <%s> by Ghostscriopt to PDF' % dst_pdf_filename)
            return None

        if os.path.exists(dst_pdf_filename) and new_pdf_filename is None:
            file_func.copyFile(dst_pdf_filename, pdf_filename, rewrite=True)
            file_func.removeFile(dst_pdf_filename)
            new_pdf_filename = pdf_filename

        if os.path.exists(new_pdf_filename):
            return new_pdf_filename
        log_func.warning(u'The resulting print file has not been generated <%s> by Ghostscriopt to PDF' % new_pdf_filename)
    except:
        log_func.fatal(u'Error print file <%s> by Ghostscriopt to PDF' % filename)
    return None
