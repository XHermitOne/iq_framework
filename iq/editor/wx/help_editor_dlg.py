# -*- coding: utf-8 -*-

###########################################################################
## Adapted Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.lib.gizmos
import wx.aui

from iq.util import lang_func
_ = lang_func.getTranslation().gettext

###########################################################################
## Class iqHelpEditorDialogProto
###########################################################################

class iqHelpEditorDialogProto ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Help"), pos = wx.DefaultPosition, size = wx.Size( 509,264 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.version_staticText = wx.StaticText( self, wx.ID_ANY, _(u"..."), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.version_staticText.Wrap( -1 )

        self.version_staticText.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer1.Add( self.version_staticText, 0, wx.ALL|wx.EXPAND, 5 )

        self.button_scrolledWindow = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.button_scrolledWindow.SetScrollRate( 5, 5 )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )


        self.button_scrolledWindow.SetSizer( bSizer2 )
        self.button_scrolledWindow.Layout()
        bSizer2.Fit( self.button_scrolledWindow )
        bSizer1.Add( self.button_scrolledWindow, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


