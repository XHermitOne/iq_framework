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
## Class MultiChoiceListBoxExtDialogProto
###########################################################################

class MultiChoiceListBoxExtDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select items"), pos = wx.DefaultPosition, size = wx.Size( 579,598 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer33 = wx.BoxSizer( wx.VERTICAL )

		self.label_staticText = wx.StaticText( self, wx.ID_ANY, _(u"Select:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_staticText.Wrap( -1 )

		bSizer33.Add( self.label_staticText, 0, wx.ALL, 5 )

		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.clear_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"Clear"), wx.ArtProvider.GetBitmap( u"gtk-clear", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Clear"), _(u"Clear"), None )

		self.set_all_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"Set all"), wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Set all"), _(u"Set all"), None )

		self.ctrl_toolBar.Realize()

		bSizer33.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		items_checkListChoices = []
		self.items_checkList = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, items_checkListChoices, 0 )
		bSizer33.Add( self.items_checkList, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )

		self.cancel_button = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.cancel_button, 0, wx.ALL, 5 )

		self.select_without_button = wx.Button( self, wx.ID_ANY, _(u"Select without items"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.select_without_button, 0, wx.ALL, 5 )

		self.ok_button = wx.Button( self, wx.ID_ANY, _(u"Select"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.ok_button, 0, wx.ALL, 5 )


		bSizer33.Add( bSizer35, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer33 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onClearToolClicked, id = self.clear_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSetAllToolClicked, id = self.set_all_tool.GetId() )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.select_without_button.Bind( wx.EVT_BUTTON, self.onSelectWithoutButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onClearToolClicked(self, event):
		event.Skip()

	def onSetAllToolClicked(self, event):
		event.Skip()

	def onCancelButtonClick(self, event):
		event.Skip()

	def onSelectWithoutButtonClick(self, event):
		event.Skip()

	def onOkButtonClick(self, event):
		event.Skip()


