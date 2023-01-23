# -*- coding: utf-8 -*-

###########################################################################
## Adapted Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
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
## Class iqWxRefObjChoicePanelProto
###########################################################################

class iqWxRefObjChoicePanelProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 798,43 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.choice_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer1.Add( self.choice_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )

		self.choice_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.choice_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_MISSING_IMAGE, wx.ART_TOOLBAR ) )
		bSizer1.Add( self.choice_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.choice_textCtrl.Bind( wx.EVT_LEFT_DOWN, self.onMouseLeftDown )
		self.choice_bpButton.Bind( wx.EVT_BUTTON, self.onChoiceButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onMouseLeftDown(self, event):
		event.Skip()

	def onChoiceButtonClick(self, event):
		event.Skip()


