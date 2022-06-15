#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Editor functions.
"""

import os.path

from ..util import log_func
from ..util import global_func
from ..util import res_func
from ..util import py_func
from ..util import file_func

from ..kernel import kernel

from ..editor.wx import wxfb_manager
from ..editor.gtk import glade_manager
from ..editor.jasper_report import jasperreport_manager
from ..editor.lime_report import limereport_manager

__version__ = (0, 0, 2, 2)


def openFrameworkEditor():
    """
    Open main editor form.

    :return: True/False.
    """
    if global_func.isWXEngine():
        from .wx import start_editor
        return start_editor.startEditor()
    elif global_func.isGTKEngine():
        from .gtk import start_editor_window
        return start_editor_window.startEditor()
    else:
        log_func.warning(u'Not supported engine as editor')
    return False


def _openResourceEditor(res_filename):
    """
    Open resource editor form.

    :param res_filename: Resource filename.
        Resource file may be *.res or *.py file.
    :return: True/False.
    """
    if global_func.isWXEngine():
        if os.path.isdir(res_filename) and res_filename == file_func.getFrameworkPath():
            log_func.info(u'Main editor <%s>' % res_filename)
            return openFrameworkEditor()

        elif res_func.isResourceFile(res_filename):
            log_func.info(u'Edit resource <%s>' % res_filename)
            from .wx.res_editor import resource_editor
            resource_editor.runResourceEditor(res_filename=res_filename)
            return True

        elif py_func.isPythonFile(res_filename):
            log_func.info(u'Edit python file <%s>' % res_filename)
            from .wx import start_py
            return start_py.startPythonEditor(py_filename=res_filename)

        elif wxfb_manager.isWXFormBuilderProjectFile(res_filename):
            log_func.info(u'Edit wxFormBuilder project <%s>' % res_filename)
            from .wx import start_wxfb
            return start_wxfb.startWXFormBuilderEditor(fbp_filename=res_filename)

        elif glade_manager.isGladeProjectFile(res_filename):
            log_func.info(u'Edit Glade project <%s>' % res_filename)
            from .wx import start_glade
            return start_glade.startGladeEditor(glade_filename=res_filename)

        elif jasperreport_manager.isJasperReportProjectFile(res_filename):
            log_func.info(u'Edit JasperReport project <%s>' % res_filename)
            from .wx import start_jasper_report
            return start_jasper_report.startJasperReportEditor(jrxml_filename=res_filename)

        elif limereport_manager.isLimeReportProjectFile(res_filename):
            log_func.info(u'Edit LimeReport project <%s>' % res_filename)
            from .wx import start_lime_report
            return start_lime_report.startLimeReportEditor(lrxml_filename=res_filename)

        elif os.path.isdir(res_filename) and os.path.exists(os.path.join(res_filename, 'descript.ion')):
            log_func.info(u'Design reports <%s>' % res_filename)
            # Report folder
            from iq_report import report_manager
            rep_manager = report_manager.getReportManager()
            rep_manager.setReportDir(report_dir=res_filename)
            return rep_manager.design()

        elif os.path.isdir(res_filename):
            log_func.info(u'Edit folder <%s>' % res_filename)
            from .wx import start_folder_dialog
            return start_folder_dialog.startFolderEditor(folder_path=res_filename)

        elif not os.path.exists(res_filename):
            # PyCharm
            res_filename = os.path.dirname(res_filename)
            if os.path.exists(res_filename):
                return _openResourceEditor(res_filename)

        else:
            log_func.warning(u'Not support editing file <%s>' % res_filename)

    elif global_func.isGTKEngine():
        if os.path.isdir(res_filename) and res_filename == file_func.getFrameworkPath():
            log_func.info(u'Main editor <%s>' % res_filename)
            return openFrameworkEditor()

        elif res_func.isResourceFile(res_filename):
            log_func.info(u'Edit resource <%s>' % res_filename)
            from .gtk.res_editor import resource_editor
            return resource_editor.runResourceEditor(res_filename=res_filename)

        elif py_func.isPythonFile(res_filename):
            log_func.info(u'Edit python file <%s>' % res_filename)
            from .gtk import start_py_window
            return start_py_window.startPythonEditor(py_filename=res_filename)

        elif wxfb_manager.isWXFormBuilderProjectFile(res_filename):
            log_func.info(u'Edit wxFormBuilder project <%s>' % res_filename)
            from .gtk import start_wxfb_window
            return start_wxfb_window.startWxFormBuilderEditor(fbp_filename=res_filename)

        elif glade_manager.isGladeProjectFile(res_filename):
            log_func.info(u'Edit Glade project <%s>' % res_filename)
            from .gtk import start_glade_window
            return start_glade_window.startGladeEditor(glade_filename=res_filename)

        elif jasperreport_manager.isJasperReportProjectFile(res_filename):
            log_func.info(u'Edit JasperReport project <%s>' % res_filename)
            # from .wx import start_jasper_report
            # return start_jasper_report.startJasperReportEditor(jrxml_filename=res_filename)
            return True

        elif limereport_manager.isLimeReportProjectFile(res_filename):
            log_func.info(u'Edit LimeReport project <%s>' % res_filename)
            from .gtk import start_limereport_window
            return start_limereport_window.startLimeReportEditor(lrxml_filename=res_filename)

        elif os.path.isdir(res_filename) and os.path.exists(os.path.join(res_filename, 'descript.ion')):
            log_func.info(u'Design reports <%s>' % res_filename)
            # # Report folder
            # from iq_report import report_manager
            # rep_manager = report_manager.getReportManager()
            # rep_manager.setReportDir(report_dir=res_filename)
            # return rep_manager.design()
            return True

        elif os.path.isdir(res_filename):
            log_func.info(u'Edit folder <%s>' % res_filename)
            from .gtk import start_folder_window
            return start_folder_window.startFolderEditor(folder_path=res_filename)

        elif not os.path.exists(res_filename):
            # PyCharm
            res_filename = os.path.dirname(res_filename)
            if os.path.exists(res_filename):
                return _openResourceEditor(res_filename)
            return True

        else:
            log_func.warning(u'Not support editing file <%s>' % res_filename)
    else:
        log_func.warning(u'Not supported engine as editor')
    return False


def openResourceEditor(res_filename, create_kernel=True):
    """
    Open resource editor form.

    :param res_filename: Resource filename.
        Resource file may be *.res or *.py file.
    :param create_kernel: Create kernel?
    :return: True/False.
    """
    try:
        if create_kernel:
            # Create KERNEL object
            kernel_obj = kernel.createKernel()
            prj_res_path = res_filename.replace(file_func.getFrameworkPath(), '')
            sub_dirnames = [item for item in prj_res_path.split(os.path.sep) if item]
            if sub_dirnames:
                prj_name = sub_dirnames[0]
                kernel_obj.setProject(prj_name)

        return _openResourceEditor(res_filename)
    except:
        log_func.fatal(u'Error open resource editor form')
    return False
