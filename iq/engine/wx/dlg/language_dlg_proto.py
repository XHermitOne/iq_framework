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
import wx.lib.langlistctrl

from iq.util import lang_func
_ = lang_func.getTranslation().gettext

###########################################################################
## Class iqSelectLanguageDialogProto
###########################################################################

class iqSelectLanguageDialogProto ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select language"), pos = wx.DefaultPosition, size = wx.Size( 273,525 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        # self.wx_languages = [getattr(wx, attr_name) for attr_name in dir(wx) if attr_name.startswith('LANGUAGE_')] if not hasattr(self, 'wx_languages') else self.wx_languages
        self.language_list_box = wx.lib.langlistctrl.LanguageListCtrl(parent=self, id=wx.NewId(), select=self.wx_languages)
        bSizer1.Add( self.language_list_box, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.cancel_button = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.cancel_button, 0, wx.ALL, 5 )

        self.ok_button = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.ok_button, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
        self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def onCancelButtonClick(self, event):
        event.Skip()

    def onOkButtonClick(self, event):
        event.Skip()


###########################################################################
## Class iqSelectTranslationLanguageDialogProto
###########################################################################

class iqSelectTranslationLanguageDialogProto ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select translation"), pos = wx.DefaultPosition, size = wx.Size( 837,280 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"From language") ), wx.VERTICAL )

        # self.wx_languages = [getattr(wx, attr_name) for attr_name in dir(wx) if attr_name.startswith('LANGUAGE_')] if not hasattr(self, 'wx_languages') else self.wx_languages
        self.from_language_list_box = wx.lib.langlistctrl.LanguageListCtrl(parent=self, id=wx.NewId(), select=self.wx_languages)
        sbSizer1.Add( self.from_language_list_box, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer4.Add( sbSizer1, 1, wx.EXPAND, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u">>"), wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText2.Wrap( -1 )

        self.m_staticText2.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

        bSizer4.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"To language") ), wx.VERTICAL )

        self.to_language_list_box = wx.lib.langlistctrl.LanguageListCtrl(parent=self, id=wx.NewId(), select=self.wx_languages)
        sbSizer2.Add( self.to_language_list_box, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer4.Add( sbSizer2, 1, wx.EXPAND, 5 )


        bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.cancel_button = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.cancel_button, 0, wx.ALL, 5 )

        self.ok_button = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.ok_button, 0, wx.ALL, 5 )


        bSizer3.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )


        self.SetSizer( bSizer3 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
        self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def onCancelButtonClick(self, event):
        event.Skip()

    def onOkButtonClick(self, event):
        event.Skip()


