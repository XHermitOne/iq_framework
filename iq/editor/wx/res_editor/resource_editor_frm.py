# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.lib.gizmos
import wx.propgrid as pg

###########################################################################
## Class iqResourceEditorFrameProto
###########################################################################

class iqResourceEditorFrameProto ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Resource editor", pos = wx.Point( 0,0 ), size = wx.Size( 447,765 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.editor_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.new_tool = self.editor_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"New resource", u"New resource", None ) 
		
		self.open_tool = self.editor_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Open resource", u"Open resource", None ) 
		
		self.save_tool = self.editor_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Save resource", u"Save resource", None ) 
		
		self.saveas_tool = self.editor_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE_AS, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Save as ...", u"Save as ...", None ) 
		
		self.editor_toolBar.AddSeparator()
		
		self.test_tool = self.editor_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Test", u"Test", None ) 
		
		self.editor_toolBar.AddSeparator()
		
		self.design_tool = self.editor_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( u"gtk-preferences", wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Design", u"Design", None ) 
		
		self.editor_toolBar.AddSeparator()
		
		self.script_tool = self.editor_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_HELP_SETTINGS, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Open script", u"Open script", None ) 
		
		self.editor_toolBar.AddSeparator()
		
		self.help_tool = self.editor_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_MENU ), wx.NullBitmap, wx.ITEM_NORMAL, u"Help ...", u"Help ...", None ) 
		
		self.editor_toolBar.Realize() 
		
		bSizer1.Add( self.editor_toolBar, 0, wx.EXPAND, 5 )
		
		self.editor_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.editor_splitter.Bind( wx.EVT_IDLE, self.editor_splitterOnIdle )
		
		self.resource_panel = wx.Panel( self.editor_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.resource_treeListCtrl = wx.lib.gizmos.TreeListCtrl( self.resource_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, agwStyle=wx.lib.gizmos.TR_DEFAULT_STYLE|wx.lib.gizmos.TR_FULL_ROW_HIGHLIGHT )
		self.resource_treeListCtrl.AddColumn( u"Name", 200, wx.ALIGN_LEFT)
		self.resource_treeListCtrl.AddColumn( u"Description", 300, wx.ALIGN_LEFT)
		
		bSizer2.Add( self.resource_treeListCtrl, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.resource_panel.SetSizer( bSizer2 )
		self.resource_panel.Layout()
		bSizer2.Fit( self.resource_panel )
		self.property_panel = wx.Panel( self.editor_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.object_propertyGridManager = pg.PropertyGridManager(self.property_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PGMAN_DEFAULT_STYLE|wx.propgrid.PG_SPLITTER_AUTO_CENTER|wx.propgrid.PG_TOOLBAR)
		
		self.attributes_propertyGridPage = self.object_propertyGridManager.AddPage( u"Attributes", wx.ArtProvider.GetBitmap( u"gtk-index", wx.ART_MENU ) );
		
		self.methods_propertyGridPage = self.object_propertyGridManager.AddPage( u"Methods", wx.ArtProvider.GetBitmap( u"gtk-properties", wx.ART_MENU ) );
		
		self.events_propertyGridPage = self.object_propertyGridManager.AddPage( u"Events", wx.ArtProvider.GetBitmap( u"gtk-about", wx.ART_MENU ) );
		bSizer3.Add( self.object_propertyGridManager, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.property_panel.SetSizer( bSizer3 )
		self.property_panel.Layout()
		bSizer3.Fit( self.property_panel )
		self.editor_splitter.SplitHorizontally( self.resource_panel, self.property_panel, 0 )
		bSizer1.Add( self.editor_splitter, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.frame_statusBar = self.CreateStatusBar( 1, 0, wx.ID_ANY )
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onNewToolClicked, id = self.new_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onOpenToolClicked, id = self.open_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSaveToolClicked, id = self.save_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSaveAsToolClicked, id = self.saveas_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onTestToolClicked, id = self.test_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDesignToolClicked, id = self.design_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onScriptToolClicked, id = self.script_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onHelpToolClicked, id = self.help_tool.GetId() )
		self.resource_treeListCtrl.Bind( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.onResTreelistItemContextMenu )
		self.resource_treeListCtrl.Bind( wx.EVT_TREE_SEL_CHANGED, self.onResItemTreelistSelectionChanged )
		self.object_propertyGridManager.Bind( pg.EVT_PG_CHANGED, self.onObjPropertyGridChanged )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onNewToolClicked( self, event ):
		event.Skip()
	
	def onOpenToolClicked( self, event ):
		event.Skip()
	
	def onSaveToolClicked( self, event ):
		event.Skip()
	
	def onSaveAsToolClicked( self, event ):
		event.Skip()
	
	def onTestToolClicked( self, event ):
		event.Skip()
	
	def onDesignToolClicked( self, event ):
		event.Skip()
	
	def onScriptToolClicked( self, event ):
		event.Skip()
	
	def onHelpToolClicked( self, event ):
		event.Skip()
	
	def onResTreelistItemContextMenu( self, event ):
		event.Skip()
	
	def onResItemTreelistSelectionChanged( self, event ):
		event.Skip()
	
	def onObjPropertyGridChanged( self, event ):
		event.Skip()
	
	def editor_splitterOnIdle( self, event ):
		self.editor_splitter.SetSashPosition( 0 )
		self.editor_splitter.Unbind( wx.EVT_IDLE )
	

