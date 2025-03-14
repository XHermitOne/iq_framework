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
## Class iqStartWXFormBuilderEditorDialogProto
###########################################################################

class iqStartWXFormBuilderEditorDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"wxFormBuilder"), pos = wx.DefaultPosition, size = wx.Size( 483,315 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.new_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.new_button = wx.Button( self, wx.ID_ANY, _(u"New wxFormBuilder project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.open_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.open_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.open_button = wx.Button( self, wx.ID_ANY, _(u"Open wxFormBuilder project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.open_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer21, 1, wx.EXPAND, 5 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.migrate_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_COPY, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.migrate_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.migrate_button = wx.Button( self, wx.ID_ANY, _(u"Migrate wxFormBuilder project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.migrate_button.Enable( False )

		bSizer22.Add( self.migrate_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer22, 1, wx.EXPAND, 5 )

		bSizer222 = wx.BoxSizer( wx.HORIZONTAL )

		self.translate_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_COPY, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer222.Add( self.translate_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.translate_button = wx.Button( self, wx.ID_ANY, _(u"Translate wxFormBuilder project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer222.Add( self.translate_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer222, 1, wx.EXPAND, 5 )

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
		self.migrate_button.Bind( wx.EVT_BUTTON, self.onMigrateButtonClick )
		self.translate_button.Bind( wx.EVT_BUTTON, self.onTranslateButtonClick )
		self.exit_button.Bind( wx.EVT_BUTTON, self.onExitButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onNewButtonClick(self, event):
		event.Skip()

	def onOpenButtonClick(self, event):
		event.Skip()

	def onMigrateButtonClick(self, event):
		event.Skip()

	def onTranslateButtonClick(self, event):
		event.Skip()

	def onExitButtonClick(self, event):
		event.Skip()


