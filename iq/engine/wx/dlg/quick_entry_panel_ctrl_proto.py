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

###########################################################################
## Class iqQuickEntryPanelCtrlProto
###########################################################################

class iqQuickEntryPanelCtrlProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		panel_Sizer = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.prev_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Предыдущий элемент", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Предыдущий элемент", u"Предыдущий элемент", None )

		self.next_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Следующий элемент", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Следующий элемент", u"Следующий элемент", None )

		self.ctrl_toolBar.AddSeparator()

		self.cancel_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Отмена ввода", wx.ArtProvider.GetBitmap( wx.ART_CROSS_MARK, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Отмена ввода", u"Отмена ввода", None )

		self.ok_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Подтверждение ввода", wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Подтверждение ввода", u"Подтверждение ввода", None )

		self.default_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Значения по умолчанию", wx.ArtProvider.GetBitmap( wx.ART_UNDO, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Значения по умолчанию", u"Значения по умолчанию", None )

		self.ctrl_toolBar.AddSeparator()

		self.add_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Добавить", wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Добавить", u"Добавить", None )

		self.del_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Удалить", wx.ArtProvider.GetBitmap( wx.ART_DEL_BOOKMARK, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Удалить", u"Удалить", None )

		self.ctrl_toolBar.AddSeparator()

		self.help_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"Помощь", wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Помощь", u"Помощь", None )

		self.ctrl_toolBar.Realize()

		panel_Sizer.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )


		self.SetSizer( panel_Sizer )
		self.Layout()

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onPrevToolClicked, id = self.prev_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onNextToolClicked, id = self.next_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onCancelToolClicked, id = self.cancel_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onOkToolClicked, id = self.ok_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDefaultToolClicked, id = self.default_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onAddToolClicked, id = self.add_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelToolClicked, id = self.del_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onHelpToolClicked, id = self.help_tool.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onPrevToolClicked(self, event):
		event.Skip()

	def onNextToolClicked(self, event):
		event.Skip()

	def onCancelToolClicked(self, event):
		event.Skip()

	def onOkToolClicked(self, event):
		event.Skip()

	def onDefaultToolClicked(self, event):
		event.Skip()

	def onAddToolClicked(self, event):
		event.Skip()

	def onDelToolClicked(self, event):
		event.Skip()

	def onHelpToolClicked(self, event):
		event.Skip()


###########################################################################
## Class testPanelProto
###########################################################################

class testPanelProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Значение1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer3.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		bSizer3.Add( self.m_textCtrl2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( bSizer3, 0, wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Значение2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer4.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_spinCtrl1 = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.TAB_TRAVERSAL, 0, 10, 1 )
		bSizer4.Add( self.m_spinCtrl1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"Значение2", wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		bSizer5.Add( self.m_checkBox1, 0, wx.ALL, 5 )


		bSizer2.Add( bSizer5, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass


