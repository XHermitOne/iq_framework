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
import wx.lib.masked

import gettext
_ = gettext.gettext

###########################################################################
## Class iqEditMaskedTextDlgProto
###########################################################################

class iqEditMaskedTextDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edit"), pos = wx.DefaultPosition, size = wx.Size( 508,127 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.label_staticText = wx.StaticText( self, wx.ID_ANY, _(u"Редактирование:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_staticText.Wrap( -1 )
		bSizer1.Add( self.label_staticText, 0, wx.ALL, 5 )
		
		self.masked_textCtrl = wx.lib.masked.TextCtrl( self,  -1,  '',
		mask='###', excludeChars='',  formatcodes ='F',
		includeChars='', validRegex=r'\d{3}' ,
		validRange='', choices='', choiceRequired = True,
		defaultValue='', demo=True, name='cod')
		bSizer1.Add( self.masked_textCtrl, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, _(u"ОК"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
		bSizer2.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

