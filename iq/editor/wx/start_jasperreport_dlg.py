# -*- coding: utf-8 -*-

###########################################################################
## Adapted Python code generated with wxFormBuilder (version Oct 26 2018)
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
## Class iqStartJasperReportEditorDialogProto
###########################################################################

class iqStartJasperReportEditorDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"JasperReport"), pos = wx.DefaultPosition, size = wx.Size( 483,369 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.new_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.new_button = wx.Button( self, wx.ID_ANY, _(u"New JasperReport project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.new_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.open_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.open_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.open_button = wx.Button( self, wx.ID_ANY, _(u"Open JasperReport project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.open_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer21, 1, wx.EXPAND, 5 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.preview_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.preview_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.preview_button = wx.Button( self, wx.ID_ANY, _(u"Preview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.preview_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer22, 1, wx.EXPAND, 5 )

		bSizer222 = wx.BoxSizer( wx.HORIZONTAL )

		self.print_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_PRINT, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer222.Add( self.print_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.print_button = wx.Button( self, wx.ID_ANY, _(u"Print"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer222.Add( self.print_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer222, 1, wx.EXPAND, 5 )

		bSizer2221 = wx.BoxSizer( wx.HORIZONTAL )

		self.convert_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_MISSING_IMAGE, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2221.Add( self.convert_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, _(u"Convert to"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText1.Wrap( -1 )

		bSizer2221.Add( self.m_staticText1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		convert_choiceChoices = [ _(u"PDF"), _(u"RTF"), _(u"XLS"), _(u"XLSX"), _(u"DOCX"), _(u"ODT"), _(u"ODS"), _(u"PPTX"), _(u"CSV"), _(u"HTML"), _(u"XML") ]
		self.convert_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, convert_choiceChoices, 0 )
		self.convert_choice.SetSelection( 0 )
		bSizer2221.Add( self.convert_choice, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.convert_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.convert_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_TOOLBAR ) )
		bSizer2221.Add( self.convert_bpButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer2221, 1, wx.EXPAND, 5 )

		bSizer221 = wx.BoxSizer( wx.HORIZONTAL )

		self.exit_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_QUIT, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer221.Add( self.exit_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.exit_button = wx.Button( self, wx.ID_ANY, _(u"Exit"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.exit_button.SetDefault()
		bSizer221.Add( self.exit_button, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer221, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.new_button.Bind( wx.EVT_BUTTON, self.onNewButtonClick )
		self.open_button.Bind( wx.EVT_BUTTON, self.onOpenButtonClick )
		self.preview_button.Bind( wx.EVT_BUTTON, self.onPreviewButtonClick )
		self.print_button.Bind( wx.EVT_BUTTON, self.onPrintButtonClick )
		self.convert_bpButton.Bind( wx.EVT_BUTTON, self.onConvertButtonClick )
		self.exit_button.Bind( wx.EVT_BUTTON, self.onExitButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onNewButtonClick(self, event):
		event.Skip()

	def onOpenButtonClick(self, event):
		event.Skip()

	def onPreviewButtonClick(self, event):
		event.Skip()

	def onPrintButtonClick(self, event):
		event.Skip()

	def onConvertButtonClick(self, event):
		event.Skip()

	def onExitButtonClick(self, event):
		event.Skip()


