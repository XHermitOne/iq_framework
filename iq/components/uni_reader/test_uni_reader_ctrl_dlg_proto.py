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

###########################################################################
## Class iqTestUniReaderControllerDlgProto
###########################################################################

class iqTestUniReaderControllerDlgProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"UniReader controller test", pos = wx.DefaultPosition, size = wx.Size( 1139,463 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"New tag" ), wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Tag name:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.tag_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.tag_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Tag address:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer3.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.address_textCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.address_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )


		bSizer1.Add( sbSizer1, 0, wx.EXPAND, 5 )

		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.add_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Add tag", wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Add tag", u"Add tag", None )

		self.del_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Delete tag", wx.ArtProvider.GetBitmap( wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Delete tag", u"Delete tag", None )

		self.ctrl_toolBar.AddSeparator()

		self.update_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-refresh", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.ctrl_toolBar.Realize()

		bSizer1.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		self.tags_listCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer1.Add( self.tags_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.ok_button = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.ok_button, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer5, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onAddToolClicked, id = self.add_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelToolClicked, id = self.del_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onUpdateToolClicked, id = self.update_tool.GetId() )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onAddToolClicked( self, event ):
		event.Skip()

	def onDelToolClicked( self, event ):
		event.Skip()

	def onUpdateToolClicked( self, event ):
		event.Skip()

	def onOkButtonClick( self, event ):
		event.Skip()


