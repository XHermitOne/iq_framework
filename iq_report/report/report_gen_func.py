#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module of functions of the general interface to the generation system.
"""

from iq.util import log_func
from iq.util import res_func

from . import xml_report_generator
from . import ods_report_generator
# from . import xls_report_generator
# from . import reportman_generator
from . import rtf_report_generator

__version__ = (0, 0, 2, 1)

REPORT_GEN_SYSTEM = None

REPORT_GENERATOR_SYSTEM_TYPES = {'.xml': xml_report_generator.iqXMLReportGeneratorSystem,  # XMLSS generator
                                 '.ods': ods_report_generator.iqODSReportGeneratorSystem,  # ODS generator
                                 # '.xls': icxlsreportgenerator.icXLSReportGeneratorSystem,  # XLS generator
                                 # '.rep': reportman_generator.iqReportManagerGeneratorSystem,     # Report Manager
                                 '.rtf': rtf_report_generator.iqRTFReportGeneratorSystem,  # RTF generator
                                 }

# List of template source extensions
SRC_REPORT_EXT = REPORT_GENERATOR_SYSTEM_TYPES.keys()


def getReportGeneratorSystem(rep_filename, parent=None, refresh=True):
    """
    Get the object of the reporting system.

    :param rep_filename: Report template filename.
    :param parent: Parent window.
    :param refresh: Update report template data in the generator.
    :return: Report generator system object or None if error.
    """
    try:
        rep = res_func.loadResourcePickle(rep_filename)
        
        global REPORT_GEN_SYSTEM

        if REPORT_GEN_SYSTEM is None:
            REPORT_GEN_SYSTEM = createReportGeneratorSystem(rep['generator'], rep, parent)
            REPORT_GEN_SYSTEM.setReportTemplateFileName(rep_filename)
        elif not REPORT_GEN_SYSTEM.sameGeneratorType(rep['generator']):
            REPORT_GEN_SYSTEM = createReportGeneratorSystem(rep['generator'], rep, parent)
            REPORT_GEN_SYSTEM.setReportTemplateFileName(rep_filename)
        else:
            if refresh:
                REPORT_GEN_SYSTEM.setReportData(rep)
                REPORT_GEN_SYSTEM.setReportTemplateFileName(rep_filename)

        if REPORT_GEN_SYSTEM and REPORT_GEN_SYSTEM.getParent() is None:
            REPORT_GEN_SYSTEM.setParent(parent)
            
        return REPORT_GEN_SYSTEM
    except:
        log_func.fatal(u'Error defining a reporting system object. Report <%s>.' % rep_filename)
    return None


def createReportGeneratorSystem(repgen_sys_type, report=None, parent=None):
    """
    Create report generator system.

    :param repgen_sys_type: Indication of the type of reporting system.
         The type is specified by the template source file extension.
         In our case, one of SRC_REPORT_EXT.
    :param report: Report data dictionary.
    :param parent: Parent window.
    :return: Report generator system object or None if error.
    """
    rep_gen_sys_type = repgen_sys_type[-4:].lower() if isinstance(repgen_sys_type, str) else None
    rep_gen_sys = None
    if rep_gen_sys_type:
        rep_gen_sys_class = REPORT_GENERATOR_SYSTEM_TYPES.setdefault(rep_gen_sys_type, None)
        if rep_gen_sys_class is not None:
            rep_gen_sys = rep_gen_sys_class(report, parent)
        else:
            log_func.warning(u'Unknown generator type <%s>' % rep_gen_sys_type)
    else:
        log_func.warning(u'Invalid generator type <%s>' % repgen_sys_type)
    return rep_gen_sys


def getCurReportGeneratorSystem(report_browser_dialog=None):
    """
    Return current generation system.
    """
    global REPORT_GEN_SYSTEM
    if REPORT_GEN_SYSTEM is None:
        REPORT_GEN_SYSTEM = ods_report_generator.iqODSReportGeneratorSystem(parent=report_browser_dialog)
    return REPORT_GEN_SYSTEM
