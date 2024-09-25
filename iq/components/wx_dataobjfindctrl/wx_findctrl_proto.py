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
## Class iqFindCtrlProto
###########################################################################

class iqFindCtrlProto ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1147,89 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

        find_choiceChoices = []
        self.find_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, find_choiceChoices, 0 )
        self.find_choice.SetSelection( 0 )
        bSizer1.Add( self.find_choice, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer1.Add( ( 10, 10), 0, 0, 5 )

        self.find_staticText = wx.StaticText( self, wx.ID_ANY, _(u"Find:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.find_staticText.Wrap( -1 )

        bSizer1.Add( self.find_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.find_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.find_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )

        self.find_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

        self.find_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_TOOLBAR ) )
        bSizer1.Add( self.find_bpButton, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        # Connect Events
        self.find_textCtrl.Bind( wx.EVT_TEXT, self.onFindText )
        self.find_bpButton.Bind( wx.EVT_BUTTON, self.onFindButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def onFindText(self, event):
        event.Skip()

    def onFindButtonClick(self, event):
        event.Skip()


