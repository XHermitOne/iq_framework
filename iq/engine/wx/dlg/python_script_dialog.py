#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog module <iqPythonScriptDialogProto>. 
Generated by the iqFramework modulo the wxFormBuider prototype dialog.
"""

import keyword
import wx
import wx.stc
from . import py_script_edit_dlg_proto

import iq
from iq.util import log_func
from iq.util import global_func

from iq.engine.wx import form_manager

__version__ = (0, 0, 0, 1)


class iqPythonScriptDialog(py_script_edit_dlg_proto.iqPythonScriptDialogProto, form_manager.iqFormManager):
    """
    Dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        py_script_edit_dlg_proto.iqPythonScriptDialogProto.__init__(self, *args, **kwargs)

        self.script = None

        # Create python source editor
        self.source_scintilla = wx.stc.StyledTextCtrl(parent=self)
        # Set python source editor style
        self.setPythonSourceScintillaStyle(self.source_scintilla)

        sizer = self.GetSizer()
        sizer.Insert(0, self.source_scintilla, 1, wx.EXPAND | wx.ALL, 5)

    def setPythonSourceScintillaStyle(self, scintilla):
        """
        Set python source editor style.

        :param scintilla: The control object of the stylized text editor.
        """
        # Lexical analysis setup
        scintilla.SetLexer(wx.stc.STC_LEX_PYTHON)
        scintilla.SetKeyWords(0, ' '.join(keyword.kwlist))

        scintilla.SetProperty('fold', '1')
        scintilla.SetProperty('tab.timmy.whinge.level', '1')
        scintilla.SetMargins(0, 0)

        # Do not see blank spaces as dots
        scintilla.SetViewWhiteSpace(False)

        # Set tab width
        scintilla.SetIndent(4)                 # Forbidden indentation size for wx
        scintilla.SetIndentationGuides(True)   # Show guides
        scintilla.SetBackSpaceUnIndents(True)  # Indents instead of removing 1 space
        scintilla.SetTabIndents(True)          # Tab key indents
        scintilla.SetTabWidth(4)               # Forbidden tab size for wx
        scintilla.SetUseTabs(False)            # Use spaces instead of tabs, or

        # Setting a field to capture folder markers
        scintilla.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        scintilla.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        scintilla.SetMarginSensitive(1, True)
        scintilla.SetMarginSensitive(2, True)
        scintilla.SetMarginWidth(1, 25)
        scintilla.SetMarginWidth(2, 12)

        # and now set the fold markers
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND,     wx.stc.STC_MARK_BOXPLUSCONNECTED,  'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, 'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,  'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL,    wx.stc.STC_MARK_LCORNER,  'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB,     wx.stc.STC_MARK_VLINE,    'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER,        wx.stc.STC_MARK_BOXPLUS,  'white', 'black')
        scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN,    wx.stc.STC_MARK_BOXMINUS, 'white', 'black')

        scintilla.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Courier New,size:9')
        scintilla.StyleClearAll()

        # Crop line numbers
        scintilla.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, 'back:#99A9C2,face:Arial Narrow,size:8')

        # Highlighted bracket
        scintilla.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, 'fore:#00009D,back:#FFFF00')
        # Unrivaled brace
        scintilla.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, 'fore:#00009D,back:#FF0000')
        # Indentation guide
        scintilla.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, 'fore:#CDCDCD')
        # Styles Python
        scintilla.StyleSetSpec(wx.stc.STC_P_DEFAULT, 'fore:#000000')
        # Comments
        scintilla.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, 'fore:#008000')
        scintilla.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, 'fore:#008000')
        # Numbers
        scintilla.StyleSetSpec(wx.stc.STC_P_NUMBER, 'fore:#008080')
        # Strings and characters
        scintilla.StyleSetSpec(wx.stc.STC_P_STRING, 'fore:#800080')
        scintilla.StyleSetSpec(wx.stc.STC_P_CHARACTER, 'fore:#800080')
        # Keywords
        scintilla.StyleSetSpec(wx.stc.STC_P_WORD, 'fore:#000080,bold')
        # Triple quotes
        scintilla.StyleSetSpec(wx.stc.STC_P_TRIPLE, 'fore:#000080')
        scintilla.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, 'fore:#000080')
        # Class names
        scintilla.StyleSetSpec(wx.stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        # Function names
        scintilla.StyleSetSpec(wx.stc.STC_P_DEFNAME, 'fore:#000000,bold')
        # Operators
        scintilla.StyleSetSpec(wx.stc.STC_P_OPERATOR, 'fore:#800000,bold')
        # Identifiers
        scintilla.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, 'fore:#000000')

        # Carriage color
        scintilla.SetCaretForeground('BLUE')
        # Background selection
        scintilla.SetSelBackground(1, '#66CCFF')

        scintilla.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        scintilla.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

    def init(self):
        """
        Init dialog.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images method.
        """
        pass

    def initControls(self):
        """
        Init controls method.
        """
        pass

    def onCancelButtonClick(self, event):
        """
        Cancel button click handle.
        """
        self.script = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        OK button click handle.
        """
        self.script = self.source_scintilla.GetText()
        self.EndModal(wx.ID_OK)
        event.Skip()


def openPythonScriptDialog(parent=None):
    """
    Open dialog.

    :param parent: Parent window.
    :return: True/False.
    """
    dialog = None
    try:
        if parent is None:
            parent = global_func.getMainWin()

        dialog = iqPythonScriptDialog(parent)
        dialog.init()
        result = dialog.ShowModal()
        dialog.Destroy()
        return result == wx.ID_OK
    except:
        if dialog:
            dialog.Destroy()
        log_func.fatal(u'Error open dialog <iqPythonScriptDialog>')
    return False


def getPythonScriptDialog(parent=None, script=None):
    """
    Open dialog.

    :param parent: Parent window.
    :param script: Python script text.
    :return: Script text or None if Cancel button clicked.
    """
    dialog = None
    try:
        if parent is None:
            parent = global_func.getMainWin()

        dialog = iqPythonScriptDialog(parent)
        dialog.init()
        if script is not None:
            dialog.source_scintilla.SetText(script)

        result = dialog.ShowModal()
        new_script = dialog.script
        dialog.Destroy()
        return new_script if result == wx.ID_OK else None
    except:
        if dialog:
            dialog.Destroy()
        log_func.fatal(u'Error open dialog <iqPythonScriptDialog>')
    return None