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
from iq.components import wx_olap_query_treectrl
import wx.grid

from iq.util import lang_func
_ = lang_func.getTranslation().gettext

###########################################################################
## Class iqOLAPQueryBrowsePanelProto
###########################################################################

class iqOLAPQueryBrowsePanelProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.browse_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.browse_splitter.Bind( wx.EVT_IDLE, self.browse_splitterOnIdle )

		self.tree_panel = wx.Panel( self.browse_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.query_treectrl = wx_olap_query_treectrl.COMPONENT(parent=self.tree_panel, id=wx.NewId(), resource={'save_filename': '~/.iq/tree_olap_request.save', 'on_change': 'self.GetParent().GetParent().GetParent().refreshPivotTable()'})
		bSizer2.Add( self.query_treectrl, 1, wx.ALL|wx.EXPAND, 5 )


		self.tree_panel.SetSizer( bSizer2 )
		self.tree_panel.Layout()
		bSizer2.Fit( self.tree_panel )
		self.grid_panel = wx.Panel( self.browse_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self.grid_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.collapse_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Collapse"), _(u"Collapse"), None )

		self.expand_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Expande"), _(u"Expande"), None )

		self.ctrl_toolBar.AddSeparator()

		self.sort_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( u"gtk-sort-ascending", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_RADIO, _(u"Sort"), _(u"Sort"), None )

		self.reverse_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( u"gtk-sort-descending", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_RADIO, _(u"Reverse"), _(u"Reverse"), None )

		self.ctrl_toolBar.AddSeparator()

		self.norm_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( wx.ART_REPORT_VIEW, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_CHECK, _(u"Normal"), _(u"Normal"), None )

		self.total_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( u"gtk-justify-fill", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_CHECK, _(u"Total"), _(u"Total"), None )

		self.grp_total_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( u"gtk-justify-center", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_CHECK, _(u"Group total"), _(u"Group total"), None )

		self.ctrl_toolBar.Realize()

		bSizer3.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		self.spreadsheet_grid = wx.grid.Grid( self.grid_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.spreadsheet_grid.CreateGrid( 5, 5 )
		self.spreadsheet_grid.EnableEditing( False )
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
		bSizer3.Add( self.spreadsheet_grid, 1, wx.ALL|wx.EXPAND, 5 )


		self.grid_panel.SetSizer( bSizer3 )
		self.grid_panel.Layout()
		bSizer3.Fit( self.grid_panel )
		self.browse_splitter.SplitHorizontally( self.tree_panel, self.grid_panel, 0 )
		bSizer1.Add( self.browse_splitter, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onCollapseToolClicked, id = self.collapse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onExpandToolClicked, id = self.expand_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSortToolClicked, id = self.sort_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onReverseToolClicked, id = self.reverse_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onNormToolClicked, id = self.norm_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onTotalToolClicked, id = self.total_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onGrpTotalToolClicked, id = self.grp_total_tool.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCollapseToolClicked(self, event):
		event.Skip()

	def onExpandToolClicked(self, event):
		event.Skip()

	def onSortToolClicked(self, event):
		event.Skip()

	def onReverseToolClicked(self, event):
		event.Skip()

	def onNormToolClicked(self, event):
		event.Skip()

	def onTotalToolClicked(self, event):
		event.Skip()

	def onGrpTotalToolClicked(self, event):
		event.Skip()

	def browse_splitterOnIdle(self, event):
		self.browse_splitter.SetSashPosition( 0 )
		self.browse_splitter.Unbind( wx.EVT_IDLE )


