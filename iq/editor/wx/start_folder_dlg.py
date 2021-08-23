# -*- coding: utf-8 -*-

###########################################################################
## Adapted Python code generated with wxFormBuilder (version Oct 26 2018)
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
## Class iqStartFolderDialogProto
###########################################################################

class iqStartFolderDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Project folder/package"), pos = wx.DefaultPosition, size = wx.Size( 395,185 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.new_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.new_button = wx.Button( self, wx.ID_ANY, _(u"New ..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.run_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.run_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.run_button = wx.Button( self, wx.ID_ANY, _(u"Run project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.run_button.Enable( False )

		bSizer5.Add( self.run_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.exit_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_QUIT, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.exit_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.exit_button = wx.Button( self, wx.ID_ANY, _(u"Exit"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.exit_button.SetDefault()
		bSizer22.Add( self.exit_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer22, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.new_button.Bind( wx.EVT_BUTTON, self.onNewButtonClick )
		self.run_button.Bind( wx.EVT_BUTTON, self.onRunButtonClick )
		self.exit_button.Bind( wx.EVT_BUTTON, self.onExitButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onNewButtonClick(self, event):
		event.Skip()

	def onRunButtonClick(self, event):
		event.Skip()

	def onExitButtonClick(self, event):
		event.Skip()


