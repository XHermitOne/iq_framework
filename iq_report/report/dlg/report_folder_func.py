#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report folder functions.
"""

import os
import os.path

from iq.util import log_func
from iq.util import file_func
from iq.util import res_func

__version__ = (0, 0, 0, 1)

# Indexes
REP_FILE_IDX = 0            # full file name / report directory
REP_NAME_IDX = 1            # report name / directory
REP_DESCRIPTION_IDX = 2     # report description / directory
REP_ITEMS_IDX = 3           # nested objects
REP_IMG_IDX = 4             # Report image in the report tree

# Unprocessed folder names
NOT_WORK_DIRNAMES = ('__pycache__',)

REPORT_FILENAME_EXT = '.rep'
XLS_FILENAME_EXT = '.xls'


def getReportList(report_dir, is_sort=True):
    """
    Get report template list.

    :param report_dir: Report directory.
    :type is_sort: bool.
    :param is_sort: Sort list by name?
    :return: Format list:
        [
            [
            full file name / report directory,
            report name / directory,
            report description / directory,
            None / Nested Objects,
            image index
            ],
        .
        .
        .
        ]
        The description of the directory is taken from the descript.ion file,
        which should be in the same directory.
        If such a file is not found, then the directory description is empty.
        Nested objects is a list whose elements have the same structure.
    """
    try:
        report_dir = os.path.abspath(os.path.normpath(report_dir))
        log_func.debug(u'Report folder scan <%s>' % report_dir)

        dir_list = list()
        rep_list = list()

        sub_dirs = file_func.getSubDirs(report_dir)

        img_idx = 0
        for sub_dir in sub_dirs:
            # Exclude not processed folders
            if os.path.basename(sub_dir) in NOT_WORK_DIRNAMES:
                continue

            description_file = None
            try:
                description_file = open(os.path.join(sub_dir, 'descript.ion'), 'rt')
                dir_description = description_file.read()
                description_file.close()
            except:
                if description_file:
                    description_file.close()
                dir_description = sub_dir

            data = [sub_dir, os.path.basename(sub_dir), dir_description,
                    getReportList(sub_dir, is_sort), img_idx]
            dir_list.append(data)

        if is_sort:
            dir_list.sort(key=lambda i: i[2])

        filename_mask = os.path.join(report_dir, '*%s' % REPORT_FILENAME_EXT)
        file_rep_list = [filename for filename in file_func.getFilesByMask(filename_mask)]

        for rep_file_name in file_rep_list:
            rep_struct = res_func.loadResourcePickle(rep_file_name)
            img_idx = 2
            try:
                if rep_struct['generator'][-3:].lower() == 'xml':
                    img_idx = 1
            except:
                log_func.warning(u'Report type definition error')

            try:
                data = [rep_file_name, rep_struct['name'],
                        rep_struct['description'], None, img_idx]
                rep_list.append(data)
            except:
                log_func.fatal(u'Error reading report template <%s>' % rep_file_name)

        if is_sort:
            rep_list.sort(key=lambda i: i[2])

        return dir_list + rep_list
    except:
        log_func.fatal(u'Error filling out information about report files <%s>.' % report_dir)
    return list()


def getRootDirname():
    """
    Get project root dirname.
    """
    cur_dirname = os.path.dirname(__file__)
    if not cur_dirname:
        cur_dirname = os.getcwd()
    return os.path.dirname(os.path.dirname(cur_dirname))
