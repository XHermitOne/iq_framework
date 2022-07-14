#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog functions module.
"""

import hashlib
import os
import os.path
import traceback

import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ....util import log_func
from ....util import global_func
from ....util import lang_func

from . import text_entry_dialog
from . import single_choice_dialog
from . import multi_choice_dialog

from . import login_dialog

__version__ = (0, 0, 2, 1)

_ = lang_func.getTranslation().gettext


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
    dlg = None
    try:
        all_files_wildcard = 'All Files (*.*)|*.*'
        wildcard = wildcard_filter + '|' + all_files_wildcard if wildcard_filter else all_files_wildcard

        dlg = gi.repository.Gtk.FileChooserDialog(title=title, parent=parent,
                                                  action=gi.repository.Gtk.FileChooserAction.OPEN)
        dlg.add_buttons(gi.repository.Gtk.STOCK_CANCEL,
                        gi.repository.Gtk.ResponseType.CANCEL,
                        gi.repository.Gtk.STOCK_OPEN,
                        gi.repository.Gtk.ResponseType.OK)

        wildcard_list = wildcard.split('|')
        for i in range(len(wildcard_list) / 2):
            filter_name = wildcard_list[i * 2]
            filter_pattern = wildcard_list[i * 2 + 1]
            file_filter = gi.repository.Gtk.FileFilter()
            file_filter.set_name(filter_name)
            if '*' in filter_pattern:
                file_filter.add_pattern(filter_pattern)
            else:
                file_filter.add_mime_type(filter_pattern)
            dlg.add_filter(file_filter)

        if default_path:
            dlg.set_filename(os.path.normpath(default_path))
        else:
            dlg.set_filename(os.getcwd())

        response = dlg.run()
        if response == gi.repository.Gtk.ResponseType.OK:
            result = dlg.get_filename()
        else:
            result = ''

        dlg.destroy()
        return result
    finally:
        if dlg:
            dlg.destroy()
    return None


def getDirDlg(parent=None, title='', default_path=''):
    """
    Directory selection dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param default_path: Default path.
    :return: Directory path or None if error.
    """
    result = ''
    dlg = None
    try:
        dlg = gi.repository.Gtk.FileChooserDialog(title=title, parent=parent,
                                                  action=gi.repository.Gtk.FileChooserAction.SELECT_FOLDER)
        dlg.add_buttons(gi.repository.Gtk.STOCK_CANCEL,
                        gi.repository.Gtk.ResponseType.CANCEL,
                        'Select',
                        gi.repository.Gtk.ResponseType.OK)

        if not default_path:
            default_path = os.getcwd()
        dlg.set_filename(default_path)

        response = dlg.run()
        if response == gi.repository.Gtk.ResponseType.OK:
            result = dlg.get_filename()
    except:
        log_func.fatal(u'Error open directory selection dialog')
        result = None

    if dlg:
        dlg.destroy()

    return result


def getColorDlg(parent=None, title='', default_colour=None):
    """
    Color picker dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param default_colour: Default colour.
    :return: Selected colour or default_colour.
    """
    dlg = None
    colour = default_colour
    try:
        dlg = gi.repository.Gtk.ColorChooserDialog(title=title, parent=parent)

        response = dlg.run()
        if response == gi.repository.Gtk.ResponseType.OK:
            colour = dlg.get_color()
        dlg.destroy()
    finally:
        if dlg:
            dlg.destroy()
    return colour


def getTextEntryDlg(parent=None, title='', prompt_text='', default_value=''):
    """
    Line input dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog prompt text.
    :param default_value: Default value.
    :return: Input text value or None if pressed cancel.
    """
    return text_entry_dialog.openTextEntryDialog(parent=parent, title=title,
                                                 prompt_text=prompt_text, default_value=default_value)


def getAskDlg(title='', prompt_text='', style=None):
    """
    Open ask dialog.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param style: Dialog form style.
    :return: YES or NO or None if error.
    """
    result = None
    dlg = None
    try:
        dlg = gi.repository.Gtk.MessageDialog(transient_for=None,
                                              flags=0,
                                              message_type=gi.repository.Gtk.MessageType.QUESTION,
                                              buttons=gi.repository.Gtk.ButtonsType.YES_NO,
                                              text=title)
        dlg.format_secondary_text(prompt_text)
        response = dlg.run()
        result = response
    except:
        log_func.fatal(u'Error ask dialog')

    if dlg is not None:
        dlg.destroy()
    return result


def openAskBox(*args, **kwargs):
    """
    Open ask dialog.

    :return: True/False.
    """
    return getAskDlg(*args, **kwargs) == gi.repository.Gtk.ResponseType.YES


def openMsgBox(title='', prompt_text='', **kwargs):
    """
    Open message box.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code YES or NO or None if error.
    """
    result = None
    dlg = None
    try:
        dlg = gi.repository.Gtk.MessageDialog(transient_for=None,
                                              flags=0,
                                              message_type=gi.repository.Gtk.MessageType.INFO,
                                              buttons=gi.repository.Gtk.ButtonsType.OK,
                                              text=title,
                                              **kwargs)
        dlg.format_secondary_text(prompt_text)
        response = dlg.run()
        result = response == gi.repository.Gtk.ResponseType.OK
    except:
        log_func.fatal(u'Error open message box')

    if dlg is not None:
        dlg.destroy()
    return result


def openErrBox(title='', prompt_text='', **kwargs):
    """
    Open error message box.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code YES or NO or None if error.
    """
    result = None
    dlg = None
    try:
        dlg = gi.repository.Gtk.MessageDialog(transient_for=None,
                                              flags=0,
                                              message_type=gi.repository.Gtk.MessageType.ERROR,
                                              buttons=gi.repository.Gtk.ButtonsType.OK,
                                              text=title,
                                              **kwargs)
        dlg.format_secondary_text(prompt_text)
        response = dlg.run()
        result = response == gi.repository.Gtk.ResponseType.OK
    except:
        log_func.fatal(u'Open error message box')

    if dlg is not None:
        dlg.destroy()
    return result


def openFatalBox(title='', prompt_text='', **kwargs):
    """
    Open error message box with Traceback.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code YES or NO or None if error.
    """
    trace_txt = traceback.format_exc()
    txt = prompt_text + trace_txt
    return openErrBox(title, txt, **kwargs)


def openWarningBox(title='', prompt_text='', **kwargs):
    """
    Open warning message box.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code YES or NO or None if error.
    """
    result = None
    dlg = None
    try:
        dlg = gi.repository.Gtk.MessageDialog(transient_for=None,
                                              flags=0,
                                              message_type=gi.repository.Gtk.MessageType.WARNING,
                                              buttons=gi.repository.Gtk.ButtonsType.OK,
                                              text=title,
                                              **kwargs)
        dlg.format_secondary_text(prompt_text)
        response = dlg.run()
        result = response == gi.repository.Gtk.ResponseType.OK
    except:
        log_func.fatal(u'Error open warning message box')

    if dlg is not None:
        dlg.destroy()
    return result


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
    selected_idx = single_choice_dialog.openSingleChoiceDialog(parent=parent,
                                                               title=title,
                                                               prompt_text=prompt_text,
                                                               choices=choices,
                                                               default_idx=default_idx)
    return choices[selected_idx] if 0 <= selected_idx < len(choices) else None


def getSingleChoiceIdxDlg(parent=None, title='', prompt_text='', choices=[],
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
    selected_idx = single_choice_dialog.openSingleChoiceDialog(parent=parent,
                                                               title=title,
                                                               prompt_text=prompt_text,
                                                               choices=choices,
                                                               default_idx=default_idx)
    return selected_idx


def getMultiChoiceDlg(parent=None, title='', prompt_text='', choices=()):
    """
    Multiple choice dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param choices: List of selection lines as tuple in format ((True/False, 'line text'),...).
    :return: Selected choices as tuple ((True/False, 'line text'),...).
    """
    return multi_choice_dialog.openMultiChoiceDialog(parent=parent,
                                                     title=title,
                                                     prompt_text=prompt_text,
                                                     choices=choices)


# class iqProgressDlg(wx.ProgressDialog):
#     """
#     The progress bar dialog box class.
#     """
#     def __init__(self, parent=None, title='', prompt_text='',
#                  min_value=0, max_value=100, style=wx.PD_AUTO_HIDE):
#         """
#         Constructor.
#
#         :param parent: Parent form.
#         :param title: Dialog form title.
#         :param prompt_text: Dialog form prompt text.
#         :param min_value: Minimum value.
#         :param max_value: Maximum value.
#         :param style: Dialog style.
#         """
#         self._ProgressFrame = parent
#         self._MyFrame = False
#         if self._ProgressFrame is None:
#             self._ProgressFrame = wx.Frame(None, -1, '')
#             self._MyFrame = True
#
#         self._ProgressMIN = min_value
#         self._ProgressMAX = max_value
#         if self._ProgressMIN > self._ProgressMAX:
#             tmp_value = self._ProgressMAX
#             self._ProgressMAX = self._ProgressMIN
#             self._ProgressMIN = tmp_value
#         self._current_value = 0
#         try:
#             if style is None:
#                 style = wx.PD_AUTO_HIDE
#
#             wx.ProgressDialog.__init__(self,
#                                        title=title,
#                                        message=prompt_text,
#                                        maximum=self._ProgressMAX - self._ProgressMIN,
#                                        parent=self._ProgressFrame,
#                                        style=style | wx.PD_APP_MODAL | wx.PD_SMOOTH)
#
#             self.SetSize(wx.Size(500, 130))
#             self.CenterOnScreen()
#         except:
#             log_func.fatal(u'Error progress dialog create')
#
#     def getMax(self):
#         return self._ProgressMAX
#
#     def getMin(self):
#         return self._ProgressMIN
#
#     def updateDlg(self, value=-1, new_prompt_text=''):
#         """
#         Update progress bar value.
#
#         :param value: New value.
#         :param new_prompt_text: New dialog form prompt text.
#         """
#         if value < self._ProgressMIN:
#             value = self._ProgressMIN
#         if value > self._ProgressMAX:
#             value = self._ProgressMAX
#         self.Update(value - self._ProgressMIN, new_prompt_text)
#
#     def makeStepDlg(self, step_value=1, new_prompt_text=u''):
#         """
#         Update progress bar value by change in value.
#
#         :param step_value: Change in value.
#         :param new_prompt_text: New dialog form prompt text.
#         """
#         self._current_value += step_value
#         if self._current_value < self._ProgressMIN:
#             self._current_value = self._ProgressMIN
#         if self._current_value > self._ProgressMAX:
#             self._current_value = self._ProgressMAX
#         self.Update(self._current_value - self._ProgressMIN, new_prompt_text)
#
#     def closeDlg(self):
#         """
#         Close progress bar dialog.
#         """
#         self.Close()
#         if self._MyFrame:
#             self._ProgressFrame.Close()
#             self._ProgressFrame.Destroy()
#             self._ProgressFrame = None
#
#
# PROGRESS_DLG = None


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
    global PROGRESS_DLG
    PROGRESS_DLG = None
    try:
        if parent is None:
            app = wx.GetApp()
            parent = app.GetTopWindow()

        PROGRESS_DLG = iqProgressDlg(parent, title, prompt_text, min_value, max_value, style)
    except:
        log_func.fatal(u'Error open progress bar dialog')
    return PROGRESS_DLG


def updateProgressDlg(value=-1, new_prompt_text=''):
    """
    Update progress bar dialog.

    :param value: New value.
    :param new_prompt_text: New dialog form prompt text.
    :return: True/False.
    """
    global PROGRESS_DLG

    try:
        if PROGRESS_DLG is not None:
            PROGRESS_DLG.updateDlg(value, new_prompt_text)
            return True
    except:
        log_func.fatal(u'Update progress bar dialog error')
    return False


def stepProgressDlg(step_value=1, new_prompt_text=u''):
    """
    Update progress bar value by change in value.

    :param step_value: Change in value.
    :param new_prompt_text: New dialog form prompt text.
    :return: True/False.
    """
    global PROGRESS_DLG

    try:
        if PROGRESS_DLG is not None:
            PROGRESS_DLG.makeStepDlg(step_value, new_prompt_text)
            return True
    except:
        log_func.fatal(u'Update progress bar value by change in value error')
    return False


def closeProgressDlg():
    """
    Close progress bar dialog.
    """
    global PROGRESS_DLG

    try:
        if PROGRESS_DLG is not None:
            PROGRESS_DLG.updateDlg(PROGRESS_DLG.getMax())
            PROGRESS_DLG.closeDlg()
            PROGRESS_DLG.Destroy()
            PROGRESS_DLG = None
            return True
    except:
        log_func.fatal(u'Close progress bar dialog error')
    return False


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
    dlg = None
    win_clear = False
    try:
        if choices is None:
            choices = []

        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        result = default
        dlg = iqStrComboBoxDialog(parent, title, prompt_text, choices, default)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getEntered()

        if dlg:
            dlg.Destroy()

        if win_clear:
            parent.Destroy()

        return result
    except:
        if dlg:
            dlg.Destroy()

        if win_clear:
            parent.Destroy()
        log_func.fatal(u'Open select/edit string dialog error')
    return None


# class iqStrComboBoxDialog(wx.Dialog):
#     """
#     Select/edit string dialog.
#     """
#     def __init__(self, parent, title='', prompt_text='',
#                  choices=None, default_value=''):
#         """
#         Constructor.
#
#         :param parent: Parent form.
#         :param title: Dialog form title.
#         :param prompt_text: Dialog form prompt text.
#         :param choices: List of selection lines.
#         :param default_value: Default value.
#         """
#         try:
#             if choices is None:
#                 choices = []
#
#             wx.Dialog.__init__(self, parent, -1, title=title,
#                                pos=wx.DefaultPosition, size=wx.Size(500, 150))
#
#             self._text = wx.StaticText(self, -1, prompt_text, wx.Point(10, 10), wx.Size(-1, -1))
#
#             id_ = wx.NewId()
#             self._ok_button = wx.Button(self, id_, _(u'OK'), wx.Point(420, 80), wx.Size(60, -1))
#             self.Bind(wx.EVT_BUTTON, self.onOKButtonClick, id=id_)
#
#             id_ = wx.NewId()
#             self._cancel_button = wx.Button(self, id_, _(u'Cancel'), wx.Point(340, 80), wx.Size(60, -1))
#             self.Bind(wx.EVT_BUTTON, self.onCancelButtonClick, id=id_)
#
#             id_ = wx.NewId()
#             self._combo_box = wx.ComboBox(self, 500, default_value, wx.Point(20, 30), wx.Size(460, -1),
#                                           choices, wx.CB_DROPDOWN)
#             self._string = default_value
#         except:
#             log_func.fatal(u'Select/edit string dialog create error')
#
#     def onOKButtonClick(self, event):
#         """
#         Button click handler <OK>.
#         """
#         self._string = self._combo_box.GetValue()
#         self.EndModal(wx.ID_OK)
#         event.Skip()
#
#     def onCancelButtonClick(self, event):
#         """
#         Button click handler <Cancel>.
#         """
#         self.EndModal(wx.ID_CANCEL)
#         event.Skip()
#
#     def getEntered(self):
#         """
#         Get edited string.
#         """
#         return self._string


def openAboutDlg(parent=None, title='', prompt_text='', logo_bitmap=None):
    """
    Open dialog <About ...>.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param logo_bitmap: Logo as Bitmap object.
    """
    about_dialog = gi.repository.Gtk.AboutDialog(transient_for=parent, modal=True)
    about_dialog.present()


LOGIN_USER_IDX = 0
LOGIN_PASSWORD_IDX = 1
LOGIN_PASSWORD_MD5_IDX = 2


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
    return login_dialog.openLoginDialog(title=title,
                                        default_username=default_username,
                                        reg_users=reg_users,
                                        user_descriptions=user_descriptions)
