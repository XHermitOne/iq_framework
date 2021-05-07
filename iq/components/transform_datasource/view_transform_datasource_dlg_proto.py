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
import wx.propgrid as pg

from iq.util import lang_func
_ = lang_func.getTranslation().gettext

###########################################################################
## Class iqViewTransformDataSourceDialogProto
###########################################################################

class iqViewTransformDataSourceDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Viewing transfor datasource results"), pos = wx.DefaultPosition, size = wx.Size( 856,619 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )

		self.query_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.var_panel = wx.Panel( self.query_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self.var_panel, wx.ID_ANY, _(u"Variables:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer5.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.var_propertyGrid = pg.PropertyGrid(self.var_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		bSizer5.Add( self.var_propertyGrid, 1, wx.ALL|wx.EXPAND, 5 )


		self.var_panel.SetSizer( bSizer5 )
		self.var_panel.Layout()
		bSizer5.Fit( self.var_panel )
		bSizer3.Add( self.var_panel, 1, wx.EXPAND |wx.ALL, 5 )


		self.query_panel.SetSizer( bSizer3 )
		self.query_panel.Layout()
		bSizer3.Fit( self.query_panel )
		self.table_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self.table_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.collapse_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"Свернуть панель"), wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Collapse panel"), _(u"Collapse panel"), None )

		self.expand_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"Развернуть панель"), wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Expand panel"), _(u"Expand panel"), None )

		self.ctrl_toolBar.AddSeparator()

		self.refresh_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"Обновить результаты запроса"), wx.ArtProvider.GetBitmap( u"gtk-refresh", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Refresh"), _(u"Refresh"), None )

		self.ctrl_toolBar.AddSeparator()

		self.m_staticText3 = wx.StaticText( self.ctrl_toolBar, wx.ID_ANY, _(u"Limiting the number of records:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		self.ctrl_toolBar.AddControl( self.m_staticText3 )
		self.limit_spinCtrl = wx.SpinCtrl( self.ctrl_toolBar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0 )
		self.ctrl_toolBar.AddControl( self.limit_spinCtrl )
		self.ctrl_toolBar.Realize()

		bSizer4.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		self.records_listCtrl = wx.ListCtrl( self.table_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer4.Add( self.records_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self.table_panel, wx.ID_ANY, _(u"Total records:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer7.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.count_textCtrl = wx.TextCtrl( self.table_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.count_textCtrl.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

		bSizer7.Add( self.count_textCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer4.Add( bSizer7, 0, wx.EXPAND, 5 )


		self.table_panel.SetSizer( bSizer4 )
		self.table_panel.Layout()
		bSizer4.Fit( self.table_panel )
		self.panel_splitter.SplitHorizontally( self.query_panel, self.table_panel, 0 )
		bSizer1.Add( self.panel_splitter, 1, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.ok_button = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.ok_button.SetDefault()
		bSizer2.Add( self.ok_button, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onCollapseToolClicked, id = self.collapse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onExpandToolClicked, id = self.expand_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onRefreshToolClicked, id = self.refresh_tool.GetId() )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCollapseToolClicked(self, event):
		event.Skip()

	def onExpandToolClicked(self, event):
		event.Skip()

	def onRefreshToolClicked(self, event):
		event.Skip()

	def onOkButtonClick(self, event):
		event.Skip()

	def panel_splitterOnIdle(self, event):
		self.panel_splitter.SetSashPosition( 0 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )


