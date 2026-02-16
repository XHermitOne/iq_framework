#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CSV file functions.
"""

import csv
import os
import os.path

from . import log_func

__version__ = (0, 0, 0, 1)


def loadCSVFile(csv_filename, delim=u',', encoding='utf-8'):
    """
    Load CSV file as record list.

    :param csv_filename: CSV filename.
    :param delim: Separator character.
    :param encoding: Text file code page.
    :return: Record list.
        Each record is a list of field values.
        Or None if error.
    """
    if not os.path.exists(csv_filename):
        log_func.warning(u'File <%s> not found' % csv_filename)
        return None

    result = list()
    try:
        with open(csv_filename, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            result = [tuple(row) for row in csv_reader]
        return result
    except:
        log_func.fatal(u'Error load CSV file <%s>' % csv_filename)
    return None

