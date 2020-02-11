#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog functions module.
"""

import hashlib
import os
import os.path
import traceback
import wx
import wx.lib.imagebrowser

from ....util import log_func

__version__ = (0, 0, 0, 1)


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
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        wildcard = wildcard_filter + '|All Files (*.*)|*.*'
        dlg = wx.FileDialog(parent, title, '', '', wildcard, wx.FD_OPEN)
        if default_path:
            dlg.SetDirectory(os.path.normpath(default_path))
        else:
            dlg.SetDirectory(os.getcwd())
        
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetPaths()[0]
        else:
            result = ''
        dlg.Destroy()
        return result
    finally:
        if dlg:
            dlg.Destroy()

        if win_clear:
           parent.Destroy()
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
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.DirDialog(parent, title,
                           style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if not default_path:
            default_path = os.getcwd()
        dlg.SetPath(default_path)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetPath()
    except:
        log_func.fatal(u'Open directory selection dialog error')
        result = None

    if dlg:
        dlg.Destroy()
        dlg = None

    if win_clear:
        parent.Destroy()

    return result


def getColorDlg(parent=None, title='', default_colour=wx.BLACK):
    """
    Color picker dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param default_colour: Default colour.
    :return: Selected colour or default_colour.
    """
    dlg = None
    win_clear = False
    colour = default_colour
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.ColourDialog(parent, wx.ColourData().SetColour(default_colour))
        dlg.SetTitle(title)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            colour = dlg.GetColourData().GetColour()
        dlg.Destroy()
    finally:
        if dlg:
            dlg.Destroy()

        if win_clear:
           parent.Destroy()
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
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.TextEntryDialog(parent, prompt_text, title)
        if default_value is None:
            default_value = ''
        dlg.SetValue(str(default_value))
        if dlg.ShowModal() == wx.ID_OK:
            txt = dlg.GetValue()
            return txt
    finally:
        if dlg:
            dlg.Destroy()

        if win_clear:
            parent.Destroy()
    return None


def getAskDlg(title='', prompt_text='', style=wx.YES_NO | wx.ICON_QUESTION):
    """
    Open ask dialog.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param style: Dialog form style.
    :return: wx.YES or wx.NO or None if error.
    """
    try:
        return wx.MessageBox(prompt_text, title, style=style)
    except:
        log_func.fatal(u'Ask dialog error')
    return None


def openAskBox(*args, **kwargs):
    """
    Open ask dialog.

    :return: True/False.
    """
    return getAskDlg(*args, **kwargs) == wx.YES


def openMsgBox(title='', prompt_text='', **kwargs):
    """
    Open message box.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code wx.YES or wx.NO or None if error.
    """
    try:
        return wx.MessageBox(prompt_text, title, style=wx.OK, **kwargs)
    except:
        log_func.fatal(u'Open message box error')
    return None


def openErrBox(title='', prompt_text='', **kwargs):
    """
    Open error message box.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code wx.YES or wx.NO or None if error.
    """
    try:
        return wx.MessageBox(prompt_text, title, style=wx.OK | wx.ICON_ERROR, **kwargs)
    except:
        log_func.fatal(u'Open error message box')
    return None


def openFatalBox(title='', prompt_text='', **kwargs):
    """
    Open error message box with Traceback.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code wx.YES or wx.NO or None if error.
    """
    trace_txt = traceback.format_exc()
    txt = prompt_text + trace_txt
    return openErrBox(title, txt, **kwargs)


def openWarningBox(title='', prompt_text='', **kwargs):
    """
    Open warning message box.

    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :return: Pressed button code wx.YES or wx.NO or None if error.
    """
    try:
        return wx.MessageBox(prompt_text, title, style=wx.OK | wx.ICON_WARNING, **kwargs)
    except:
        log_func.fatal(u'Open warning message box error')
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
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.SingleChoiceDialog(parent, prompt_text, title, choices, wx.CHOICEDLG_STYLE)
        if default_idx >= 0:
            dlg.SetSelection(default_idx)
        if dlg.ShowModal() == wx.ID_OK:
            txt = dlg.GetStringSelection()
            return txt
    finally:
        if dlg:
            dlg.Destroy()
        if win_clear:
            parent.Destroy()
    return None


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
    idx = -1
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = wx.SingleChoiceDialog(parent, prompt_text, title,
                                    choices, wx.CHOICEDLG_STYLE)
        if default_idx >= 0:
            dlg.SetSelection(default_idx)

        if dlg.ShowModal() == wx.ID_OK:
            idx = dlg.GetSelection()
    finally:
        if dlg:
            dlg.Destroy()
        if win_clear:
            parent.Destroy()
    return idx


def getMultiChoiceDlg(parent=None, title='', prompt_text='', choices=()):
    """
    Multiple choice dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param choices: List of selection lines as tuple in format ((True/False, 'line text'),...).
    :return: Selected chices as tuple ((True/False, 'line text'),...).
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        choice_list = [row[1] for row in choices]
        dlg = wx.MultiChoiceDialog(parent, prompt_text, title, choice_list)
        selections = [i for i, row in enumerate(choices) if row[0]]
        dlg.SetSelections(selections)
        
        if dlg.ShowModal() == wx.ID_OK:
            selections = dlg.GetSelections()
            result = [(bool(i in selections), txt) for i, txt in enumerate(choice_list)]
            return result
    finally:
        if dlg:
            dlg.Destroy()
        if win_clear:
            parent.Destroy()
    return None


class icProgressDlg(wx.ProgressDialog):
    """
    The progress bar dialog box class.
    """
    def __init__(self, parent=None, title='', prompt_text='',
                 min_value=0, max_value=100, style=wx.PD_CAN_ABORT):
        """
        Constructor.

        :param parent: Parent form.
        :param title: Dialog form title.
        :param prompt_text: Dialog form prompt text.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        :param style: Dialog style.
        """
        self._ProgressFrame = parent
        self._MyFrame = False
        if self._ProgressFrame is None:
            self._ProgressFrame = wx.Frame(None, -1, '')
            self._MyFrame = True

        self._ProgressMIN = min_value
        self._ProgressMAX = max_value
        if self._ProgressMIN > self._ProgressMAX:
            tmp_value = self._ProgressMAX
            self._ProgressMAX = self._ProgressMIN
            self._ProgressMIN = tmp_value
        self._current_value = 0
        try:
            wx.ProgressDialog.__init__(self, title, prompt_text,
                                       self._ProgressMAX - self._ProgressMIN,
                                       self._ProgressFrame, style | wx.PD_APP_MODAL)

            self.SetSize(wx.Size(500, 130))
            self.CenterOnScreen()
        except:
            log_func.fatal(u'Progress dialog _create error')

    def getMax(self):
        return self._ProgressMAX

    def getMin(self):
        return self._ProgressMIN

    def updateDlg(self, value=-1, new_prompt_text=''):
        """
        Update progress bar value.

        :param value: New value.
        :param new_prompt_text: New dialog form prompt text.
        """
        if value < self._ProgressMIN:
            value = self._ProgressMIN
        if value > self._ProgressMAX:
            value = self._ProgressMAX
        self.Update(value - self._ProgressMIN, new_prompt_text)

    def makeStepDlg(self, step_value=1, new_prompt_text=u''):
        """
        Update progress bar value by change in value.

        :param step_value: Change in value.
        :param new_prompt_text: New dialog form prompt text.
        """
        self._current_value += step_value
        if self._current_value < self._ProgressMIN:
            self._current_value = self._ProgressMIN
        if self._current_value > self._ProgressMAX:
            self._current_value = self._ProgressMAX
        self.Update(self._current_value - self._ProgressMIN, new_prompt_text)

    def closeDlg(self):
        """
        Close progress bar dialog.
        """
        self.Close()
        if self._MyFrame:
            self._ProgressFrame.Close()
            self._ProgressFrame.Destroy()
            self._ProgressFrame = None


PROGRESS_DLG = None


def openProgressDlg(parent=None, title='', prompt_text='',
                    min_value=0, max_value=100, style=wx.PD_AUTO_HIDE):
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
        PROGRESS_DLG = icProgressDlg(parent, title, prompt_text, min_value, max_value, style)
    except:
        log_func.fatal(u'Open progress bar dialog error')
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


class iqStrComboBoxDialog(wx.Dialog):
    """
    Select/edit string dialog.
    """
    def __init__(self, parent, title='', prompt_text='',
                 choices=None, default_value=''):
        """
        Constructor.

        :param parent: Parent form.
        :param title: Dialog form title.
        :param prompt_text: Dialog form prompt text.
        :param choices: List of selection lines.
        :param default_value: Default value.
        """
        try:
            if choices is None:
                choices = []

            wx.Dialog.__init__(self, parent, -1, title=title,
                               pos=wx.DefaultPosition, size=wx.Size(500, 150))

            self._text = wx.StaticText(self, -1, prompt_text, wx.Point(10, 10), wx.Size(-1, -1))

            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK', wx.Point(420, 80), wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.onOKButtonClick, id=id_)

            id_ = wx.NewId()
            self._cancel_button = wx.Button(self, id_, u'Cancel', wx.Point(340, 80), wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.onCancelButtonClick, id=id_)

            id_ = wx.NewId()
            self._combo_box = wx.ComboBox(self, 500, default_value, wx.Point(20, 30), wx.Size(460, -1),
                                          choices, wx.CB_DROPDOWN)
            self._string = default_value
        except:
            log_func.fatal(u'Select/edit string dialog _create error')

    def onOKButtonClick(self, event):
        """
        Button click handler <OK>.
        """
        self._string = self._combo_box.GetValue()
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Button click handler <Cancel>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def getEntered(self):
        """
        Get edited string.
        """
        return self._string


def openAboutDlg(parent=None, title='', prompt_text='', logo_bitmap=None):
    """
    Open dialog <About ...>.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param prompt_text: Dialog form prompt text.
    :param logo_bitmap: Logo as wx.Bitmap object.
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
           parent = wx.Frame(None, -1, '')
           win_clear = True

        dlg = iqAboutDialog(parent, title, prompt_text, logo_bitmap)
        dlg.ShowModal()

        if dlg:
            dlg.Destroy()

        if win_clear:
            parent.Destroy()
    except:
        if dlg:
            dlg.Destroy()

        if win_clear:
           parent.Destroy()


class iqAboutDialog(wx.Dialog):
    """
    Dialog <About...>.
    """
    def __init__(self, parent, title='', prompt_text='', logo_bitmap=None):
        """
        Constructor.

        :param parent: Parent form.
        :param title: Dialog form title.
        :param prompt_text: Dialog form prompt text.
        :param logo_bitmap: Logo as wx.Bitmap object.
        """
        try:
            wx.Dialog.__init__(self, parent, -1, title=title,
                               pos=wx.DefaultPosition, size=wx.Size(500, 500))

            sizer = wx.BoxSizer(wx.VERTICAL)
            self._logo = None
            if logo_bitmap is not None:
                self._logo = wx.StaticBitmap(self, -1, logo_bitmap, pos=wx.Point(10, 10))
                sizer.Add(self._logo, 10, wx.ALL, 5)

            self._text = wx.StaticText(self, -1, prompt_text)
            sizer.Add(self._text, 0, wx.ALL, 5)

            line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
            sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK')
            self.Bind(wx.EVT_BUTTON, self.onOKButtonClick, id=id_)
            sizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

            self.SetSizer(sizer)
            self.SetAutoLayout(True)
            sizer.Fit(self)
        except:
            log_func.fatal(u'Diallog <About...> _create error')

    def onOKButtonClick(self, event):
        """
        Button click handler <OK>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()


LOGIN_USER_IDX = 0
LOGIN_PASSWORD_IDX = 1
LOGIN_PASSWORD_MD5_IDX = 2


def getLoginDlg(parent=None, title='', default_username='', reg_users=None):
    """
    Open login user dialog.

    :param parent: Parent form.
    :param title: Dialog form title.
    :param default_username: Default user name.
    :param reg_users: User name list.
    :return: Tuple: (username, password, password hash) or None if error.
    """
    dlg = None
    win_clear = False
    try:
        if parent is None:
            id_ = wx.NewId()
            parent = wx.Frame(None, id_, '')
            win_clear = True

        dlg = iqLoginDialog(parent, title, default_username, reg_users)
        if dlg.ShowModal() == wx.ID_OK:
            result = (dlg.getUsername(), dlg.getPassword(), dlg.getPasswordHash())
            dlg.Destroy()

            if win_clear:
                parent.Destroy()
            return result
    except:
        log_func.fatal(u'Open login dialog error')

    if dlg:
       dlg.Destroy()

    if win_clear:
        parent.Destroy()
    return None


class iqLoginDialog(wx.Dialog):
    """
    Login user dialog.
    """
    def __init__(self, parent_, title='', default_username='', reg_users=None):
        """
        Constructor.

        :param parent: Parent form.
        :param title: Dialog form title.
        :param default_username: Default user name.
        :param reg_users: User name list.
        """
        try:
            if not title:
                title = ''
                
            wx.Dialog.__init__(self, parent_, -1, title=title,
                               pos=wx.DefaultPosition, size=wx.Size(350, 150))

            from ic.PropertyEditor.images import editorimg
            icon_img = editorimg.shield.GetBitmap()
            if icon_img:
                icon = wx.Icon(icon_img)
                self.SetIcon(icon)

            id_ = wx.NewId()
            self._text = wx.StaticText(self, id_, u'User name:',
                                       wx.Point(10, 10), wx.Size(-1, -1))
            id_ = wx.NewId()
            self._text = wx.StaticText(self, id_, u'Password:',
                                       wx.Point(10, 40), wx.Size(-1, -1))

            id_ = wx.NewId()
            self._ok_button = wx.Button(self, id_, u'OK',
                                        wx.Point(280, 80), wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.onOKButtonClick, id=id_)
            self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

            id_ = wx.NewId()
            self._cancel_button = wx.Button(self, id_, u'Cancel',
                                            wx.Point(200, 80), wx.Size(60, -1))
            self.Bind(wx.EVT_BUTTON, self.onCancelButtonClick, id=id_)

            id_ = wx.NewId()
            if reg_users is None:
                reg_users = []
            if default_username is None:
                default_username = ''
            self._user_edit = wx.ComboBox(self, id_,
                                          value=default_username,
                                          pos=(120, 10), size=(220, -1),
                                          choices=reg_users)
            id_ = wx.NewId()
            self._password_edit = wx.TextCtrl(self, id_, '',
                                              wx.Point(120, 40), wx.Size(220, -1),
                                              style=wx.TE_PASSWORD)

            self._user = default_username
            self._password = ''

            self._user_edit.SetFocus()
        except:
            log_func.fatal(u'Login dialog _create error')

    def onKeyDown(self, event):
        """
        Keyboard handler.
        """
        key = event.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        elif key == wx.WXK_RETURN:
            self._user = self._getSelectedUsername()
            self._password = self._password_edit.GetValue()
            self.EndModal(wx.ID_OK)
        # event.Skip()

    def onOKButtonClick(self, event):
        """
        Button click handler <OK>.
        """
        self._user = self._getSelectedUsername()
        self._password = self._password_edit.GetValue()
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Button click handler <Cancel>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def _getSelectedUsername(self):
        """
        Get selected username in combobox.
        """
        value = self._user_edit.GetValue()
        if value:
            return value.split(' ')[0].strip() 
        return ''
    
    def getUsername(self):
        """
        Get username.
        """
        return self._user

    def getPassword(self):
        """
        Get password.
        """
        return self._password

    def getPasswordHash(self):
        """
        Get password hash as md5.
        """
        return hashlib.md5(self._password.encode()).hexdigest()