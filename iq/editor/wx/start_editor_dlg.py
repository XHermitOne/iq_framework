# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
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
## Class iqStartEditorDialogProto
###########################################################################

class iqStartEditorDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"iqFramework"), pos = wx.DefaultPosition, size = wx.Size( 448,308 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.new_prj_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_prj_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.new_prj_button = wx.Button( self, wx.ID_ANY, _(u"New project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_prj_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.run_prj_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.run_prj_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.run_prj_button = wx.Button( self, wx.ID_ANY, _(u"Run project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.run_prj_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer21, 1, wx.EXPAND, 5 )

		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )

		self.dbg_prj_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP_SIDE_PANEL, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer211.Add( self.dbg_prj_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.dbg_prj_button = wx.Button( self, wx.ID_ANY, _(u"Debug project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer211.Add( self.dbg_prj_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer211, 1, wx.EXPAND, 5 )

		bSizer213 = wx.BoxSizer( wx.HORIZONTAL )

		self.tools_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-preferences", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer213.Add( self.tools_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.tools_button = wx.Button( self, wx.ID_ANY, _(u"External tools"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer213.Add( self.tools_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer213, 1, wx.EXPAND, 5 )

		bSizer212 = wx.BoxSizer( wx.HORIZONTAL )

		self.help_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer212.Add( self.help_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.help_button = wx.Button( self, wx.ID_ANY, _(u"Help"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer212.Add( self.help_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer212, 1, wx.EXPAND, 5 )

		bSizer214 = wx.BoxSizer( wx.HORIZONTAL )

		self.exit_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_QUIT, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer214.Add( self.exit_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.exit_button = wx.Button( self, wx.ID_ANY, _(u"Exit"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer214.Add( self.exit_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer214, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.new_prj_button.Bind( wx.EVT_BUTTON, self.onNewPrjButtonClick )
		self.run_prj_button.Bind( wx.EVT_BUTTON, self.onRunPrjButtonClick )
		self.dbg_prj_button.Bind( wx.EVT_BUTTON, self.onDbgPrjButtonClick )
		self.tools_button.Bind( wx.EVT_BUTTON, self.onToolsButtonClick )
		self.help_button.Bind( wx.EVT_BUTTON, self.onHelpButtonClick )
		self.exit_button.Bind( wx.EVT_BUTTON, self.onExitButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onNewPrjButtonClick( self, event ):
		event.Skip()

	def onRunPrjButtonClick( self, event ):
		event.Skip()

	def onDbgPrjButtonClick( self, event ):
		event.Skip()

	def onToolsButtonClick( self, event ):
		event.Skip()

	def onHelpButtonClick( self, event ):
		event.Skip()

	def onExitButtonClick( self, event ):
		event.Skip()


