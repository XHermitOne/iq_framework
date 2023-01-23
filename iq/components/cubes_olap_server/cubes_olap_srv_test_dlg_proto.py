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
from . import cubes_olap_srv_request_panel
import wx.stc
import wx.grid

from iq.util import lang_func
_ = lang_func.getTranslation().gettext

###########################################################################
## Class iqCubesOLAPSrvTestDialogProto
###########################################################################

class iqCubesOLAPSrvTestDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"OLAP server"), pos = wx.DefaultPosition, size = wx.Size( 870,812 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.panel_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.panel_splitter.Bind( wx.EVT_IDLE, self.panel_splitterOnIdle )

		self.request_splitter_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )

		self.request_panel = cubes_olap_srv_request_panel.iqCubesOLAPSrvRequestPanel(parent=self.request_splitter_panel)
		bSizer17.Add( self.request_panel, 1, wx.ALL|wx.EXPAND, 5 )


		self.request_splitter_panel.SetSizer( bSizer17 )
		self.request_splitter_panel.Layout()
		bSizer17.Fit( self.request_splitter_panel )
		self.response_panel = wx.Panel( self.panel_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self.response_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.refresh_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( u"gtk-refresh", wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Refresh"), _(u"Refresh"), None )

		self.ctrl_toolBar.Realize()

		bSizer5.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		self.response_splitter = wx.SplitterWindow( self.response_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.response_splitter.Bind( wx.EVT_IDLE, self.response_splitterOnIdle )

		self.json_panel = wx.Panel( self.response_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText4 = wx.StaticText( self.json_panel, wx.ID_ANY, _(u"Result:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		self.m_staticText4.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

		bSizer7.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.json_scintilla = wx.stc.StyledTextCtrl(parent=self.json_panel, id=wx.NewId())
		bSizer7.Add( self.json_scintilla, 1, wx.ALL|wx.EXPAND, 5 )


		self.json_panel.SetSizer( bSizer7 )
		self.json_panel.Layout()
		bSizer7.Fit( self.json_panel )
		self.spreadsheet_panel = wx.Panel( self.response_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText5 = wx.StaticText( self.spreadsheet_panel, wx.ID_ANY, _(u"Result as table:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		self.m_staticText5.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

		bSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.spreadsheet_grid = wx.grid.Grid( self.spreadsheet_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.spreadsheet_grid.CreateGrid( 5, 5 )
		self.spreadsheet_grid.EnableEditing( True )
		self.spreadsheet_grid.EnableGridLines( True )
		self.spreadsheet_grid.EnableDragGridSize( False )
		self.spreadsheet_grid.SetMargins( 0, 0 )

		# Columns
		self.spreadsheet_grid.EnableDragColMove( False )
		self.spreadsheet_grid.EnableDragColSize( True )
		self.spreadsheet_grid.SetColLabelSize( 0 )
		self.spreadsheet_grid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.spreadsheet_grid.EnableDragRowSize( True )
		self.spreadsheet_grid.SetRowLabelSize( 0 )
		self.spreadsheet_grid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.spreadsheet_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer8.Add( self.spreadsheet_grid, 1, wx.ALL|wx.EXPAND, 5 )


		self.spreadsheet_panel.SetSizer( bSizer8 )
		self.spreadsheet_panel.Layout()
		bSizer8.Fit( self.spreadsheet_panel )
		self.response_splitter.SplitVertically( self.json_panel, self.spreadsheet_panel, 250 )
		bSizer5.Add( self.response_splitter, 1, wx.EXPAND, 5 )


		self.response_panel.SetSizer( bSizer5 )
		self.response_panel.Layout()
		bSizer5.Fit( self.response_panel )
		self.panel_splitter.SplitHorizontally( self.request_splitter_panel, self.response_panel, 500 )
		bSizer1.Add( self.panel_splitter, 1, wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.close_button = wx.Button( self, wx.ID_ANY, _(u"Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.close_button, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer3, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onRefreshToolClicked, id = self.refresh_tool.GetId() )
		self.close_button.Bind( wx.EVT_BUTTON, self.onCloseButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onRefreshToolClicked(self, event):
		event.Skip()

	def onCloseButtonClick(self, event):
		event.Skip()

	def panel_splitterOnIdle(self, event):
		self.panel_splitter.SetSashPosition( 500 )
		self.panel_splitter.Unbind( wx.EVT_IDLE )

	def response_splitterOnIdle(self, event):
		self.response_splitter.SetSashPosition( 250 )
		self.response_splitter.Unbind( wx.EVT_IDLE )


