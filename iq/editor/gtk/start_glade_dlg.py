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
## Class iqStartGladeEditorDialogProto
###########################################################################

class iqStartGladeEditorDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Glade"), pos = wx.DefaultPosition, size = wx.Size( 483,293 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.new_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.new_button = wx.Button( self, wx.ID_ANY, _(u"New Glade project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.open_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.open_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.open_button = wx.Button( self, wx.ID_ANY, _(u"Open Glade project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.open_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer21, 1, wx.EXPAND, 5 )

		bSizer2111 = wx.BoxSizer( wx.HORIZONTAL )

		self.preview_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2111.Add( self.preview_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.preview_button = wx.Button( self, wx.ID_ANY, _(u"Preview Glade project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2111.Add( self.preview_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer2111, 1, wx.EXPAND, 5 )

		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )

		self.gen_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer211.Add( self.gen_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.gen_button = wx.Button( self, wx.ID_ANY, _(u"Generate python module by Glade project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer211.Add( self.gen_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer211, 1, wx.EXPAND, 5 )

		bSizer221 = wx.BoxSizer( wx.HORIZONTAL )

		self.exit_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_QUIT, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer221.Add( self.exit_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.exit_button = wx.Button( self, wx.ID_ANY, _(u"Exit"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.exit_button.SetDefault()
		bSizer221.Add( self.exit_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer221, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.new_button.Bind( wx.EVT_BUTTON, self.onNewButtonClick )
		self.open_button.Bind( wx.EVT_BUTTON, self.onOpenButtonClick )
		self.preview_button.Bind( wx.EVT_BUTTON, self.onPreviewButtonClick )
		self.gen_button.Bind( wx.EVT_BUTTON, self.onGenerateButtonClick )
		self.exit_button.Bind( wx.EVT_BUTTON, self.onExitButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onNewButtonClick(self, event):
		event.Skip()

	def onOpenButtonClick(self, event):
		event.Skip()

	def onPreviewButtonClick(self, event):
		event.Skip()

	def onGenerateButtonClick(self, event):
		event.Skip()

	def onExitButtonClick(self, event):
		event.Skip()


