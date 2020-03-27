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
import wx.aui

import gettext
_ = gettext.gettext

###########################################################################
## Class iqReportActionDialogProto
###########################################################################

class iqReportActionDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Report:"), pos = wx.DefaultPosition, size = wx.Size( 393,259 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer1 = wx.FlexGridSizer( 4, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.AddGrowableRow( 2 )
		fgSizer1.AddGrowableRow( 3 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmap2 = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_PRINT, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_bitmap2, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.print_button = wx.Button( self, wx.ID_ANY, _(u"Print"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.print_button.SetDefault() 
		fgSizer1.Add( self.print_button, 1, wx.ALL|wx.EXPAND, 10 )
		
		self.m_bitmap3 = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_bitmap3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.preview_button = wx.Button( self, wx.ID_ANY, _(u"Preview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.preview_button, 1, wx.ALL|wx.EXPAND, 10 )
		
		self.m_bitmap4 = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_bitmap4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.export_button = wx.Button( self, wx.ID_ANY, _(u"Export to Office"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.export_button, 1, wx.ALL|wx.EXPAND, 10 )
		
		self.m_bitmap5 = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_CROSS_MARK, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_bitmap5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.cancel_button, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.print_button.Bind( wx.EVT_BUTTON, self.onPrintButtonClick )
		self.preview_button.Bind( wx.EVT_BUTTON, self.onPreviewButtonClick )
		self.export_button.Bind( wx.EVT_BUTTON, self.onExportButtonClick )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onPrintButtonClick( self, event ):
		event.Skip()
	
	def onPreviewButtonClick( self, event ):
		event.Skip()
	
	def onExportButtonClick( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	

