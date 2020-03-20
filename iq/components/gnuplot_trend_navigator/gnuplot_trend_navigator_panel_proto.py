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
from .. import gnuplot_trend

import gettext
_ = gettext.gettext

###########################################################################
## Class iqGnuplotTrendNavigatorPanelProto
###########################################################################

class iqGnuplotTrendNavigatorPanelProto ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 888,726 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.view_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer2.Add( self.view_bpButton, 0, wx.ALL, 5 )
		
		self.print_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_PRINT, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer2.Add( self.print_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.legend_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-justify-fill", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer2.Add( self.legend_bpButton, 0, wx.ALL, 5 )
		
		self.settings_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-properties", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer2.Add( self.settings_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.trend_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.trend_splitter.SetSashGravity( 0 )
		self.trend_splitter.Bind( wx.EVT_IDLE, self.trend_splitterOnIdle )
		
		self.legend_panel = wx.Panel( self.trend_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.legend_listCtrl = wx.ListCtrl( self.legend_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_NO_HEADER|wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer6.Add( self.legend_listCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.legend_panel.SetSizer( bSizer6 )
		self.legend_panel.Layout()
		bSizer6.Fit( self.legend_panel )
		self.trend_panel = wx.Panel( self.trend_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.trend = gnuplot_trend.iqGnuplotTrend(parent=self.trend_panel, id=wx.NewId())
		bSizer5.Add( self.trend, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.up_bpButton = wx.BitmapButton( self.trend_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-go-up", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer7.Add( self.up_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer7.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.zoom_in_bpButton = wx.BitmapButton( self.trend_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-zoom-in", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer7.Add( self.zoom_in_bpButton, 0, wx.ALL, 5 )
		
		self.zoom_out_bpButton = wx.BitmapButton( self.trend_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-zoom-out", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer7.Add( self.zoom_out_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer7.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.down_bpButton = wx.BitmapButton( self.trend_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-go-down", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer7.Add( self.down_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		
		self.trend_panel.SetSizer( bSizer5 )
		self.trend_panel.Layout()
		bSizer5.Fit( self.trend_panel )
		self.trend_splitter.SplitHorizontally( self.legend_panel, self.trend_panel, 64 )
		bSizer3.Add( self.trend_splitter, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.first_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-goto-first", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.first_bpButton, 0, wx.ALL, 5 )
		
		self.prev_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-go-back", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.prev_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.time_zoom_out_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-zoom-out", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.time_zoom_out_bpButton, 0, wx.ALL, 5 )
		
		self.time_zoom_in_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-zoom-in", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.time_zoom_in_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.next_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-go-forward", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.next_bpButton, 0, wx.ALL, 5 )
		
		self.last_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-goto-last", wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.last_bpButton, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.aui.EVT_AUI_PANE_CLOSE, self.onNavigatorAuiPaneClose )
		self.Bind( wx.EVT_SIZE, self.onNavigatorSize )
		self.view_bpButton.Bind( wx.EVT_BUTTON, self.onViewButtonClick )
		self.print_bpButton.Bind( wx.EVT_BUTTON, self.onPrintButtonClick )
		self.legend_bpButton.Bind( wx.EVT_BUTTON, self.onLegendButtonClick )
		self.settings_bpButton.Bind( wx.EVT_BUTTON, self.onSettingsButtonClick )
		self.trend_splitter.Bind( wx.EVT_SIZE, self.onTrendSplitterSize )
		self.trend.Bind( wx.EVT_PAINT, self.onTrendPain )
		self.trend.Bind( wx.EVT_SIZE, self.onTrendSize )
		self.up_bpButton.Bind( wx.EVT_BUTTON, self.onUpButtonClick )
		self.zoom_in_bpButton.Bind( wx.EVT_BUTTON, self.onZoomInButtonClick )
		self.zoom_out_bpButton.Bind( wx.EVT_BUTTON, self.onZoomOutButtonClick )
		self.down_bpButton.Bind( wx.EVT_BUTTON, self.onDownButtonClick )
		self.first_bpButton.Bind( wx.EVT_BUTTON, self.onFirstButtonClick )
		self.prev_bpButton.Bind( wx.EVT_BUTTON, self.onPrevButtonClick )
		self.time_zoom_out_bpButton.Bind( wx.EVT_BUTTON, self.onTimeZoomOutButtonClick )
		self.time_zoom_in_bpButton.Bind( wx.EVT_BUTTON, self.onTimeZoomInButtonClick )
		self.next_bpButton.Bind( wx.EVT_BUTTON, self.onNextButtonClick )
		self.last_bpButton.Bind( wx.EVT_BUTTON, self.onLastButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onNavigatorAuiPaneClose( self, event ):
		event.Skip()
	
	def onNavigatorSize( self, event ):
		event.Skip()
	
	def onViewButtonClick( self, event ):
		event.Skip()
	
	def onPrintButtonClick( self, event ):
		event.Skip()
	
	def onLegendButtonClick( self, event ):
		event.Skip()
	
	def onSettingsButtonClick( self, event ):
		event.Skip()
	
	def onTrendSplitterSize( self, event ):
		event.Skip()
	
	def onTrendPain( self, event ):
		event.Skip()
	
	def onTrendSize( self, event ):
		event.Skip()
	
	def onUpButtonClick( self, event ):
		event.Skip()
	
	def onZoomInButtonClick( self, event ):
		event.Skip()
	
	def onZoomOutButtonClick( self, event ):
		event.Skip()
	
	def onDownButtonClick( self, event ):
		event.Skip()
	
	def onFirstButtonClick( self, event ):
		event.Skip()
	
	def onPrevButtonClick( self, event ):
		event.Skip()
	
	def onTimeZoomOutButtonClick( self, event ):
		event.Skip()
	
	def onTimeZoomInButtonClick( self, event ):
		event.Skip()
	
	def onNextButtonClick( self, event ):
		event.Skip()
	
	def onLastButtonClick( self, event ):
		event.Skip()
	
	def trend_splitterOnIdle( self, event ):
		self.trend_splitter.SetSashPosition( 64 )
		self.trend_splitter.Unbind( wx.EVT_IDLE )
	

