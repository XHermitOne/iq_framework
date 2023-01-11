#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog functions module.
"""

from ..util import global_func
from ..util import log_func
from ..util import lang_func

__version__ = (0, 0, 3, 1)

_ = lang_func.getTranslation().gettext

DIALOG_FUNCTION_MODULE = None


def _importDialogFunctions():
    """
    Check and import dialog function module.

    :return: Dialog function module object or None if error.
    """
    _dlg_func = None
    if globals()['DIALOG_FUNCTION_MODULE'] is None:
        if global_func.isWXEngine():
            log_func.info(u'Dialog functions. Use WX engine')
            from ..engine.wx.dlg import wxdlg_func as _dlg_func
        elif global_func.isQTEngine():
            log_func.warning(u'Dialog functions. Not support QT engine')
        elif global_func.isGTKEngine():
            log_func.info(u'Dialog functions. Use GTK engine')
            from ..engine.gtk.dlg import gtk_dlg_func as _dlg_func
        elif global_func.isCUIEngine():
            log_func.info(u'Dialog functions. Use CUI engine')
            from ..engine.cui.dlg import cui_dlg_func as _dlg_func
        globals()['DIALOG_FUNCTION_MODULE'] = _dlg_func
    return globals()['DIALOG_FUNCTION_MODULE']


def _clearImportDialogFunctions():
    """
    Clear imports dialog functions.
    """
    globals()['DIALOG_FUNCTION_MODULE'] = None
    return True


def getFileDlg(parent=None, title='', wildcard_filter='', default_path=''):
    """
    Open file selection dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param wildcard_filter: File filter.
        For example: All ZIP Files (*.zip)|*.zip
    :param default_path: Default path.
    :return: full name of the selected file or None в случае ошибки.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.getFileDlg(parent=parent, title=title,
                                    wildcard_filter=wildcard_filter, default_path=default_path)
    return None


def getDirDlg(parent=None, title='', default_path=''):
    """
    Directory selection dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param default_path: Default path.
    :return: Directory path or None if error.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.getDirDlg(parent=parent, title=title, default_path=default_path)
    return None


def getColorDlg(parent=None, title='', default_colour=None):
    """
    Color picker dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param default_colour: Default colour.
    :return: Selected colour or default_colour.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.getColorDlg(parent=parent, title=title, default_colour=default_colour)
    return None


def getTextEntryDlg(parent=None, title='', prompt_text='', default_value=''):
    """
    Line input dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog prompt text.
    :param default_value: Default value.
    :return: Input text value or None if pressed cancel.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.getTextEntryDlg(parent=parent, title=title,
                                         prompt_text=prompt_text, default_value=default_value)
    return None


def openAskBox(title='', prompt_text='', **kwargs):
    """
    Open ask dialog.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: True/False.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.openAskBox(title=title, prompt_text=prompt_text, **kwargs)
    return None


def openMsgBox(title=_('MESSAGE'), prompt_text='', **kwargs):
    """
    Open message box.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code wx.YES or wx.NO or None if error.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.openMsgBox(title=title, prompt_text=prompt_text, **kwargs)
    return None


def openErrBox(title=_('ERROR'), prompt_text='', **kwargs):
    """
    Open error message box.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code wx.YES or wx.NO or None if error.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.openErrBox(title=title, prompt_text=prompt_text, **kwargs)
    return None


def openFatalBox(title=_('CRITICAL'), prompt_text='', **kwargs):
    """
    Open error message box with Traceback.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code wx.YES or wx.NO or None if error.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.openFatalBox(title=title, prompt_text=prompt_text, **kwargs)
    return None


def openWarningBox(title=_('WARNING'), prompt_text='', **kwargs):
    """
    Open warning message box.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code wx.YES or wx.NO or None if error.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.openWarningBox(title=title, prompt_text=prompt_text, **kwargs)
    return None


def getSingleChoiceDlg(parent=None, title='', prompt_text='', choices=(),
                       default_idx=-1):
    """
    List selection dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param choices: List of selection lines.
    :param default_idx: Default selected line index.
    :return: Selected text or None if pressed cancel.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.getSingleChoiceDlg(parent=parent, title=title, prompt_text=prompt_text,
                                            choices=choices, default_idx=default_idx)
    return None


def getSingleChoiceIdxDlg(parent=None, title='', prompt_text='', choices=(),
                          default_idx=-1):
    """
    Select index dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param choices: List of selection lines.
    :param default_idx: Default selected line index.
    :return: Selected line index or -1 if pressed cancel.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.getSingleChoiceIdxDlg(parent=parent, title=title, prompt_text=prompt_text,
                                               choices=choices, default_idx=default_idx)
    return None


def getMultiChoiceDlg(parent=None, title='', prompt_text='', choices=(), pos=None):
    """
    Multiple choice dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param choices: List of selection lines as tuple in format ((True/False, 'line text'),...).
    :param pos: Dialog position.
    :return: Selected choices as tuple ((True/False, 'line text'),...).
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.getMultiChoiceDlg(parent=parent, title=title, prompt_text=prompt_text, choices=choices, pos=pos)
    return None


def openProgressDlg(parent=None, title='', prompt_text='',
                    min_value=0, max_value=100, style=None):
    """
    Open progress bar dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param min_value: Minimum value.
    :param max_value: Maximum value.
    :param style: Dialog style.
    :return: Progress bar dialog object or None is error.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.openProgressDlg(parent=parent, title=title, prompt_text=prompt_text,
                                         min_value=min_value, max_value=max_value, style=style)
    return None


def updateProgressDlg(value=-1, new_prompt_text=''):
    """
    Update progress bar dialog.

    :param value: New value.
    :param new_prompt_text: New dialog form prompt text.
    :return: True/False.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.updateProgressDlg(value=value, new_prompt_text=new_prompt_text)
    return None


def stepProgressDlg(step_value=1, new_prompt_text=u''):
    """
    Update progress bar value by change in value.

    :param step_value: Change in value.
    :param new_prompt_text: New dialog form prompt text.
    :return: True/False.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.stepProgressDlg(step_value=step_value, new_prompt_text=new_prompt_text)
    return None


def closeProgressDlg():
    """
    Close progress bar dialog.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.closeProgressDlg()
    return None


def getStrComboBoxDlg(parent=None, title='', prompt_text='', choices=None, default=''):
    """
    Open select/edit string dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param choices: List of selection lines.
    :param default: Default string.
    :return: Selected or input string or None if error.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.getStrComboBoxDlg(parent=parent, title=title, prompt_text=prompt_text,
                                           choices=choices, default=default)
    return None


def openAboutDlg(parent=None, title='', prompt_text='', logo_bitmap=None):
    """
    Open dialog <About ...>.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param logo_bitmap: Logo as wx.Bitmap object.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.openAboutDlg(parent=parent, title=title, prompt_text=prompt_text, logo_bitmap=logo_bitmap)
    return None


def getLoginDlg(parent=None, title='', default_username='', reg_users=None, user_descriptions=None):
    """
    Open login user dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param default_username: Default user name.
    :param reg_users: User name list.
    :param user_descriptions: User description list.
    :return: Tuple: (username, password, password hash) or None if error.
    """
    _dlg_func = _importDialogFunctions()

    if _dlg_func:
        return _dlg_func.getLoginDlg(parent=parent, title=title,
                                     default_username=default_username,
                                     reg_users=reg_users,
                                     user_descriptions=user_descriptions)
    return None
