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
## Class iqCubesOLAPSrvRequestPanelProto
###########################################################################

class iqCubesOLAPSrvRequestPanelProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 867,483 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		bSizer121 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, _(u"Request:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		self.m_staticText6.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

		bSizer121.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.request_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer121.Add( self.request_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer10.Add( bSizer121, 0, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, _(u"Cube:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cube_choiceChoices = []
		self.cube_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cube_choiceChoices, 0 )
		self.cube_choice.SetSelection( 0 )
		bSizer2.Add( self.cube_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Method:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		method_choiceChoices = []
		self.method_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, method_choiceChoices, 0 )
		self.method_choice.SetSelection( 0 )
		bSizer2.Add( self.method_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Dimension:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		dimension_choiceChoices = []
		self.dimension_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dimension_choiceChoices, 0 )
		self.dimension_choice.SetSelection( 0 )
		bSizer2.Add( self.dimension_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer10.Add( bSizer2, 0, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, _(u"Parameters:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer12.Add( self.m_staticText7, 0, wx.ALL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.cut_checkBox = wx.CheckBox( self, wx.ID_ANY, _(u"Cut"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.cut_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.cut_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.cut_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.cut_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.cut_hlp_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ) )
		bSizer9.Add( self.cut_hlp_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer12.Add( bSizer9, 0, wx.EXPAND, 5 )

		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )

		self.drilldown_checkBox = wx.CheckBox( self, wx.ID_ANY, _(u"Drill down"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.drilldown_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.drilldown_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer101.Add( self.drilldown_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.drilldown_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.drilldown_hlp_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ) )
		bSizer101.Add( self.drilldown_hlp_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer12.Add( bSizer101, 0, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.aggregates_checkBox = wx.CheckBox( self, wx.ID_ANY, _(u"Aggregates"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.aggregates_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.aggregates_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.aggregates_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.aggregates_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.aggregates_hlp_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ) )
		bSizer11.Add( self.aggregates_hlp_bpButton, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer11, 0, wx.EXPAND, 5 )

		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )

		self.measures_checkBox = wx.CheckBox( self, wx.ID_ANY, _(u"Measures"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.measures_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.measures_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.measures_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.measures_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.measures_hlp_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ) )
		bSizer111.Add( self.measures_hlp_bpButton, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer111, 0, wx.EXPAND, 5 )

		bSizer1111 = wx.BoxSizer( wx.HORIZONTAL )

		self.page_checkBox = wx.CheckBox( self, wx.ID_ANY, _(u"Page"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1111.Add( self.page_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.page_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1111.Add( self.page_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.page_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.page_hlp_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ) )
		bSizer1111.Add( self.page_hlp_bpButton, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer1111, 0, wx.EXPAND, 5 )

		bSizer11111 = wx.BoxSizer( wx.HORIZONTAL )

		self.pagesize_checkBox = wx.CheckBox( self, wx.ID_ANY, _(u"Page size"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11111.Add( self.pagesize_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.pagesize_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11111.Add( self.pagesize_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.pagesize_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.pagesize_hlp_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ) )
		bSizer11111.Add( self.pagesize_hlp_bpButton, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer11111, 0, wx.EXPAND, 5 )

		bSizer11112 = wx.BoxSizer( wx.HORIZONTAL )

		self.order_checkBox = wx.CheckBox( self, wx.ID_ANY, _(u"Order"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11112.Add( self.order_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.order_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11112.Add( self.order_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.order_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.order_hlp_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ) )
		bSizer11112.Add( self.order_hlp_bpButton, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer11112, 0, wx.EXPAND, 5 )

		bSizer11113 = wx.BoxSizer( wx.HORIZONTAL )

		self.split_checkBox = wx.CheckBox( self, wx.ID_ANY, _(u"Split"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11113.Add( self.split_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.split_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11113.Add( self.split_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.split_hlp_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.split_hlp_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ) )
		bSizer11113.Add( self.split_hlp_bpButton, 0, wx.ALL, 5 )


		bSizer12.Add( bSizer11113, 0, wx.EXPAND, 5 )


		bSizer10.Add( bSizer12, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer10 )
		self.Layout()

		# Connect Events
		self.cube_choice.Bind( wx.EVT_CHOICE, self.onCubeChoice )
		self.cut_checkBox.Bind( wx.EVT_CHECKBOX, self.onCutCheckBox )
		self.cut_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onCutHelpButtonClick )
		self.drilldown_checkBox.Bind( wx.EVT_CHECKBOX, self.onDrilldownCheckBox )
		self.drilldown_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onDrilldownHelpButtonClick )
		self.aggregates_checkBox.Bind( wx.EVT_CHECKBOX, self.onAggregatesCheckBox )
		self.aggregates_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onAggregatesHelpButtonClick )
		self.measures_checkBox.Bind( wx.EVT_CHECKBOX, self.onMeasuresCheckBox )
		self.measures_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onMeasuresHelpButtonClick )
		self.page_checkBox.Bind( wx.EVT_CHECKBOX, self.onPageCheckBox )
		self.page_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onPageHelpButtonClick )
		self.pagesize_checkBox.Bind( wx.EVT_CHECKBOX, self.onPagesizeCheckBox )
		self.pagesize_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onPagesizeHelpButtonClick )
		self.order_checkBox.Bind( wx.EVT_CHECKBOX, self.onOrderCheckBox )
		self.order_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onOrderHelpButtonClick )
		self.split_checkBox.Bind( wx.EVT_CHECKBOX, self.onSplitCheckBox )
		self.split_hlp_bpButton.Bind( wx.EVT_BUTTON, self.onSplitHelpButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCubeChoice(self, event):
		event.Skip()

	def onCutCheckBox(self, event):
		event.Skip()

	def onCutHelpButtonClick(self, event):
		event.Skip()

	def onDrilldownCheckBox(self, event):
		event.Skip()

	def onDrilldownHelpButtonClick(self, event):
		event.Skip()

	def onAggregatesCheckBox(self, event):
		event.Skip()

	def onAggregatesHelpButtonClick(self, event):
		event.Skip()

	def onMeasuresCheckBox(self, event):
		event.Skip()

	def onMeasuresHelpButtonClick(self, event):
		event.Skip()

	def onPageCheckBox(self, event):
		event.Skip()

	def onPageHelpButtonClick(self, event):
		event.Skip()

	def onPagesizeCheckBox(self, event):
		event.Skip()

	def onPagesizeHelpButtonClick(self, event):
		event.Skip()

	def onOrderCheckBox(self, event):
		event.Skip()

	def onOrderHelpButtonClick(self, event):
		event.Skip()

	def onSplitCheckBox(self, event):
		event.Skip()

	def onSplitHelpButtonClick(self, event):
		event.Skip()


###########################################################################
## Class iqCubesPivotTabRequestPanelProto
###########################################################################

class iqCubesPivotTabRequestPanelProto ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 861,721 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, _(u"Cube:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer14.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cube_choiceChoices = []
		self.cube_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cube_choiceChoices, 0 )
		self.cube_choice.SetSelection( 0 )
		bSizer14.Add( self.cube_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer13.Add( bSizer14, 0, wx.EXPAND, 5 )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Pivot table:") ), wx.VERTICAL )

		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Rows"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer16.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer16.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Dimension:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer16.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		row_dimension_choiceChoices = []
		self.row_dimension_choice = wx.Choice( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), row_dimension_choiceChoices, 0 )
		self.row_dimension_choice.SetSelection( 0 )
		bSizer16.Add( self.row_dimension_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText9 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"to level:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer16.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		row_level_choiceChoices = []
		self.row_level_choice = wx.Choice( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), row_level_choiceChoices, 0 )
		self.row_level_choice.SetSelection( 0 )
		bSizer16.Add( self.row_level_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer1.Add( bSizer16, 0, wx.EXPAND, 5 )

		bSizer161 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText71 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Columns"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )

		bSizer161.Add( self.m_staticText71, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer161.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText81 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Dimension:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )

		bSizer161.Add( self.m_staticText81, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		col_dimension_choiceChoices = []
		self.col_dimension_choice = wx.Choice( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), col_dimension_choiceChoices, 0 )
		self.col_dimension_choice.SetSelection( 0 )
		bSizer161.Add( self.col_dimension_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText91 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"to level:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )

		bSizer161.Add( self.m_staticText91, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		col_level_choiceChoices = []
		self.col_level_choice = wx.Choice( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), col_level_choiceChoices, 0 )
		self.col_level_choice.SetSelection( 0 )
		bSizer161.Add( self.col_level_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer1.Add( bSizer161, 0, wx.EXPAND, 5 )


		bSizer13.Add( sbSizer1, 0, wx.EXPAND, 5 )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Calculations:") ), wx.VERTICAL )

		aggregate_checkListChoices = []
		self.aggregate_checkList = wx.CheckListBox( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, aggregate_checkListChoices, 0 )
		sbSizer2.Add( self.aggregate_checkList, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer13.Add( sbSizer2, 0, wx.EXPAND, 5 )

		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Срезы:") ), wx.VERTICAL )

		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText16 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Cut"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		bSizer20.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer20.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText17 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Dimension:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		bSizer20.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		cut_dimension_choiceChoices = []
		self.cut_dimension_choice = wx.Choice( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), cut_dimension_choiceChoices, 0 )
		self.cut_dimension_choice.SetSelection( 0 )
		bSizer20.Add( self.cut_dimension_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText18 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Values:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		bSizer20.Add( self.m_staticText18, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.cut_value_textCtrl = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 250,-1 ), 0 )
		bSizer20.Add( self.cut_value_textCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.cut_help_bpButton = wx.BitmapButton( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.cut_help_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_TOOLBAR ) )
		bSizer20.Add( self.cut_help_bpButton, 0, wx.ALL, 5 )


		sbSizer3.Add( bSizer20, 0, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.VERTICAL )

		self.cut_toolBar = wx.ToolBar( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.add_cut_tool = self.cut_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.del_cut_tool = self.cut_toolBar.AddTool( wx.ID_ANY, _(u"tool"), wx.ArtProvider.GetBitmap( wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.cut_toolBar.Realize()

		bSizer21.Add( self.cut_toolBar, 0, wx.EXPAND, 5 )

		self.cut_listCtrl = wx.ListCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer21.Add( self.cut_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )


		sbSizer3.Add( bSizer21, 1, wx.EXPAND, 5 )


		bSizer13.Add( sbSizer3, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer13 )
		self.Layout()

		# Connect Events
		self.row_dimension_choice.Bind( wx.EVT_CHOICE, self.onRowDimensionChoice )
		self.col_dimension_choice.Bind( wx.EVT_CHOICE, self.onColDimensionChoice )
		self.cut_help_bpButton.Bind( wx.EVT_BUTTON, self.onHelpCutButtonClick )
		self.Bind( wx.EVT_TOOL, self.onAddCutToolClicked, id = self.add_cut_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelCutToolClicked, id = self.del_cut_tool.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onRowDimensionChoice(self, event):
		event.Skip()

	def onColDimensionChoice(self, event):
		event.Skip()

	def onHelpCutButtonClick(self, event):
		event.Skip()

	def onAddCutToolClicked(self, event):
		event.Skip()

	def onDelCutToolClicked(self, event):
		event.Skip()


