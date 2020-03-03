# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class iqStartPythonEditorDialogProto
###########################################################################

class iqStartPythonEditorDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Python module"), pos = wx.DefaultPosition, size = wx.Size( 438,245 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.wxfb_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_MISSING_IMAGE, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.wxfb_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.wxfb_button = wx.Button( self, wx.ID_ANY, _(u"Adapt wxFormBuilder form module"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.wxfb_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.gen_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_EXECUTABLE_FILE, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.gen_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.gen_button = wx.Button( self, wx.ID_ANY, _(u"Generate GUI module"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.gen_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer22, 1, wx.EXPAND, 5 )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.migrate_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( u"gtk-convert", wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.migrate_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.migrate_button = wx.Button( self, wx.ID_ANY, _(u"Migrate python module"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.migrate_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer21, 1, wx.EXPAND, 5 )
		
		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.exit_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_QUIT, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer211.Add( self.exit_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.exit_button = wx.Button( self, wx.ID_ANY, _(u"Exit"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.exit_button.SetDefault() 
		bSizer211.Add( self.exit_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer211, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.wxfb_button.Bind( wx.EVT_BUTTON, self.onWXFBButtonClick )
		self.gen_button.Bind( wx.EVT_BUTTON, self.onGenButtonClick )
		self.migrate_button.Bind( wx.EVT_BUTTON, self.onMigrateButtonClick )
		self.exit_button.Bind( wx.EVT_BUTTON, self.onExitButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onWXFBButtonClick( self, event ):
		event.Skip()
	
	def onGenButtonClick( self, event ):
		event.Skip()
	
	def onMigrateButtonClick( self, event ):
		event.Skip()
	
	def onExitButtonClick( self, event ):
		event.Skip()
	

