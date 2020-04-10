#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
iqReport - Report management program.

Command line options:
    
    python iq_report.py <Launch parameters>
    
Launch parameters:

    [Help and debugging]
        --help|-h|-?        Print help
        --version|-v        Print version
        --debug|-d          Debug mode
        --log|-l            Log mode

   [Launch modes]
        --viewer|-V         The mode of selecting a report and sending it to print
        --editor|-E         Mode with support for calling the report editor
        --print=|-p=        Run mode for generating a report with printing
        --preview=|-P=      Report generation start-up mode with preview
        --export=|-E=       Start-up mode for generating a report with subsequent conversion to office
        --select=|-S=       The mode of launching the formation of the report with the subsequent choice of action
        --gen=              Report generation launch mode with additional parameters
        --db=               Indication of communication with the database (in the form of url)
        --sql=              Specifying an SQL query to get a report table
        --postprint         Print report after generation
        --postpreview       Report preview after generation
        --postexport        Convert Office report after generation
        --stylelib=         Specify a style library for single reporting
        --var=              Adding a variable to populate in the report
        --path=             Specifying a Report Folder
        --no_gui            Enabling console mode
"""


import sys
import os
import os.path
import getopt
import wx

from iq.util import log_func
from iq.util import file_func
from iq.util import global_func
from iq import global_data

try:
    from .report import do_report
except ModuleNotFoundError:
    from report import do_report

__version__ = (0, 0, 0, 1)

DEFAULT_REPORTS_PATH = os.path.join(file_func.getFrameworkPath(), 'reports')

LOG_FILENAME = os.path.join(file_func.getProfilePath(), 'iq_report')


def main(argv):
    """
    Main function.

    :param argv: A list of command line options.
    """
    # Parse command line options
    try:
        options, args = getopt.getopt(argv, 'h?vdVEDpPES',
                                      ['help', 'version', 'debug', 'log',
                                       'viewer', 'editor',
                                       'postprint', 'postpreview', 'postexport',
                                       'print=', 'preview=', 'export=', 'select=',
                                       'gen=', 'db=', 'sql=',
                                       'stylelib=', 'var=', 'path=',
                                       'no_gui'])
    except getopt.error as err:
        log_func.error(err.msg, is_force_print=True)
        log_func.info(__doc__, is_force_print=True)
        sys.exit(2)

    report_filename = None
    db = None
    sql = None
    do_cmd = None
    stylelib = None
    variables = dict()
    path = None
    mode = 'default'
    mode_arg = None

    for option, arg in options:
        if option in ('-h', '--help', '-?'):
            log_func.info(__doc__, is_force_print=True)
            sys.exit(0)   
        elif option in ('-v', '--version'):
            version_txt = 'iqReport version: %s' % '.'.join([str(ver) for ver in __version__])
            log_func.info(version_txt, is_force_print=True)
            sys.exit(0)
        elif option in ('-d', '--debug'):
            global_func.setDebugMode()
        elif option in ('-l', '--log'):
            global_func.setLogMode()
        elif option in ('-V', '--viewer'):
            mode = 'view'
        elif option in ('-E', '--editor'):
            mode = 'edit'
        elif option in ('-p', '--print'):
            mode = 'print'
            mode_arg = arg
        elif option in ('-P', '--preview'):
            mode = 'preview'
            mode_arg = arg
        elif option in ('-E', '--export'):
            mode = 'export'
            mode_arg = arg
        elif option in ('-S', '--select'):
            mode = 'select'
            mode_arg = arg
        elif option in ('--gen',):
            report_filename = arg
        elif option in ('--db',):
            db = arg
        elif option in ('--sql',):
            sql = arg
        elif option in ('--postprint',):
            do_cmd = do_report.DO_COMMAND_PRINT
        elif option in ('--postpreview',):
            do_cmd = do_report.DO_COMMAND_PREVIEW
        elif option in ('--postexport',):
            do_cmd = do_report.DO_COMMAND_EXPORT
        elif option in ('--stylelib',):
            stylelib = arg
        elif option in ('--var',):
            var_name = arg.split('=')[0].strip()
            var_value = arg.split('=')[-1].strip()
            variables[var_name] = var_value
            log_func.debug(u'External variable <%s>. Value [%s]' % (str(var_name), str(var_value)))
        elif option in ('--path',):
            path = arg
        elif option in ('--no_gui', ):
            global_func.setEngineType(global_data.CUI_ENGINE_TYPE)

    log_func.init(LOG_FILENAME)

    # You must add the path to the report folder so that import of report modules
    if path is None:
        path = DEFAULT_REPORTS_PATH
    if os.path.exists(path) and os.path.isdir(path) and path not in sys.path:
        sys.path.append(path)

    app = wx.App()
    # locale = wx.Locale()
    # locale.Init(wx.LANGUAGE_RUSSIAN)

    if mode == 'default':
        if report_filename:
            # Run report generation from the command line
            do_report.doReport(report_filename=report_filename, report_dir=path,
                               db_url=db, sql=sql, command=do_cmd,
                               stylelib_filename=stylelib, variables=variables)
    elif mode == 'view':
        do_report.openReportViewer(report_dir=path)
    elif mode == 'edit':
        do_report.openReportEditor(report_dir=path)
    elif mode == 'print':
        do_report.printReport(report_filename=mode_arg, report_dir=path,
                              db_url=db, sql=sql, command=do_cmd,
                              stylelib_filename=stylelib, variables=variables)
    elif mode == 'preview':
        do_report.previewReport(report_filename=mode_arg, report_dir=path,
                                db_url=db, sql=sql, command=do_cmd,
                                stylelib_filename=stylelib, variables=variables)
    elif mode == 'export':
        do_report.exportReport(report_filename=mode_arg, report_dir=path,
                               db_url=db, sql=sql, command=do_cmd,
                               stylelib_filename=stylelib, variables=variables)
    elif mode == 'select':
        do_report.selectReport(report_filename=mode_arg, report_dir=path,
                               db_url=db, sql=sql, command=do_cmd,
                               stylelib_filename=stylelib, variables=variables)

    app.MainLoop()


if __name__ == '__main__':
    main(sys.argv[1:])
