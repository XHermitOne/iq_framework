#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Global functions module.
"""

from .. import global_data

__version__ = (0, 0, 1, 1)


def isRuntimeMode():
    """
    Is GUI runtime mode?
    """
    return global_data.getGlobal('RUNTIME_MODE')


def setRuntimeMode(runtime_mode=True):
    """
    Set GUI runtime mode.
    """
    global_data.setGlobal('RUNTIME_MODE', runtime_mode)


def isEditorMode():
    """
    Is editor mode?
    """
    return not global_data.getGlobal('RUNTIME_MODE')


def isDebugMode():
    """
    Is debug mode?
    """
    return global_data.getGlobal('DEBUG_MODE')


def setDebugMode(debug_mode=True):
    """
    Set debug mode.
    """
    global_data.setGlobal('DEBUG_MODE', debug_mode)


def isLogMode():
    """
    Is logging mode?
    """
    return global_data.getGlobal('LOG_MODE')


def setLogMode(log_mode=True):
    """
    Set logging mode.
    """
    global_data.setGlobal('LOG_MODE', log_mode)


def getLogFilename():
    """
    Get log filename.
    """
    return global_data.getGlobal('LOG_FILENAME')


def setLogFilename(log_filename):
    """
    Set log filename.

    :param log_filename: Log file name.
    """
    global_data.setGlobal('LOG_FILENAME', log_filename)


def getKernel():
    """
    Get kernel object.

    :return: Kernel object.
    """
    return global_data.getGlobal('KERNEL')


def setProjectName(project_name=None):
    """
    Set project_name name.
    """
    global_data.setGlobal('PROJECT_NAME', project_name)


def getProjectName():
    """
    Get project_name name.

    :return: Project name.
    """
    return global_data.getGlobal('PROJECT_NAME')


def getEngineType():
    """
    Get engine type (wx, qt, cui and etc).
    """
    return global_data.getGlobal('ENGINE_TYPE')


def setEngineType(engine_type):
    """
    Set engine type.

    :param engine_type: Engine type (wx, qt, cui and etc).
    """
    return global_data.setGlobal('ENGINE_TYPE', engine_type)


def isWXEngine():
    """
    Set engine as WX.

    :return: True/False.
    """
    return global_data.getGlobal('ENGINE_TYPE') == global_data.WX_ENGINE_TYPE


def isQTEngine():
    """
    Set engine as QT.

    :return: True/False.
    """
    return global_data.getGlobal('ENGINE_TYPE') == global_data.QT_ENGINE_TYPE


def isGTKEngine():
    """
    Set engine as GTK.

    :return: True/False.
    """
    return global_data.getGlobal('ENGINE_TYPE') == global_data.GTK_ENGINE_TYPE


def isCUIEngine():
    """
    Set engine as CUI.

    :return: True/False.
    """
    return global_data.getGlobal('ENGINE_TYPE') == global_data.CUI_ENGINE_TYPE


def getProject():
    """
    Get current project object.

    :return: Project object.
    """
    return global_data.getGlobal('PROJECT')


def getUser():
    """
    Get current user object.

    :return: User object.
    """
    return global_data.getGlobal('USER')


def isAdministratorUser():
    """
    Is the user an administrator?

    :return: True/False.
    """
    cur_user = getUser()
    return cur_user.isAdministrator() if cur_user else False


def getUsername():
    """
    Get current username.

    :return: Username or None if error.
    """
    user = getUser()
    return user.getName() if user else None


def getDefaultShellEncoding():
    """
    Determine the current encoding for text output.

    :return: Actual text encoding.
    """
    return global_data.getGlobal('DEFAULT_SHELL_ENCODING')


def getDefaultEncoding():
    """
    Get default encoding for text output.

    :return: Default text encoding.
    """
    return global_data.getGlobal('DEFAULT_ENCODING')


def createApplication():
    """
    Create application object.

    :return: Application object.
    """
    app = global_data.getGlobal('APPLICATION')
    if app is None:
        if isWXEngine():
            import wx
            from iq.util import log_func
            log_func.info(u'Create WX application')
            log_func.info(u'wxPython version: %s' % wx.VERSION_STRING)
            app = wx.App()
        elif isQTEngine():
            app = None
        elif isGTKEngine():
            app = None
            try:
                import gi.repository.Gtk
                app = gi.repository.Gtk
            except:
                raise
        elif isCUIEngine():
            app = None

        if app:
            global_data.setGlobal('APPLICATION', app)
    return app


def getApplication():
    """
    Get application object.
    """
    app = global_data.getGlobal('APPLICATION')
    return app


def getMainWin():
    """
    Main window object.
    """
    main_win = global_data.getGlobal('MAIN_WINDOW')
    if main_win is None:
        if isWXEngine():
            app = getApplication()
            main_win = app.GetTopWindow() if app else None
        elif isQTEngine():
            main_win = None
        elif isGTKEngine():
            main_win = None
        elif isCUIEngine():
            main_win = None

        if main_win:
            global_data.setGlobal('MAIN_WINDOW', main_win)
    return main_win


def getDefaultStrDateFmt():
    """
    Get default string date format.
    """
    return global_data.getGlobal('DEFAULT_STR_DATE_FMT')


def getDefaultStrDatetimeFmt():
    """
    Get default string datetime format.
    """
    return global_data.getGlobal('DEFAULT_STR_DATETIME_FMT')


def setSysRootPassword(password):
    """
    Set system root/administrator password.
    """
    return global_data.setGlobal('SYS_ROOT_PASSWORD', password)


def getSysRootPassword():
    """
    Get system root/administrator password.
    """
    return global_data.getGlobal('SYS_ROOT_PASSWORD')
