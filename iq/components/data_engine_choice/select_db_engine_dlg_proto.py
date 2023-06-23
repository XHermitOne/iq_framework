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
## Class iqSelectDBEngineDialogProto
###########################################################################

class iqSelectDBEngineDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select database engine"), pos = wx.DefaultPosition, size = wx.Size( 777,280 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.new_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"New database engine"), wx.ArtProvider.GetBitmap( wx.ART_PLUS, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"New database engine"), _(u"New database engine"), None )

		self.del_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"Delete database engine"), wx.ArtProvider.GetBitmap( wx.ART_MINUS, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Delete database engine"), _(u"Delete database engine"), None )

		self.ctrl_toolBar.AddSeparator()

		self.edit_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"Edit database engine"), wx.ArtProvider.GetBitmap( u"gtk-edit", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Edit database engine"), _(u"Edit database engine"), None )

		self.test_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"Test database connection"), wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Test database connection"), _(u"Test database connection"), None )

		self.ctrl_toolBar.Realize()

		bSizer1.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		db_listBoxChoices = []
		self.db_listBox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, db_listBoxChoices, wx.LB_SINGLE )
		bSizer1.Add( self.db_listBox, 1, wx.ALL|wx.EXPAND, 5 )

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
		self.Bind( wx.EVT_TOOL, self.onNewToolClicked, id = self.new_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelToolClicked, id = self.del_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onEditToolClicked, id = self.edit_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onTestToolClicked, id = self.test_tool.GetId() )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onNewToolClicked(self, event):
		event.Skip()

	def onDelToolClicked(self, event):
		event.Skip()

	def onEditToolClicked(self, event):
		event.Skip()

	def onTestToolClicked(self, event):
		event.Skip()

	def onCancelButtonClick(self, event):
		event.Skip()

	def onOkButtonClick(self, event):
		event.Skip()


