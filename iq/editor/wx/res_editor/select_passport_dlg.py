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
import wx.dataview

from iq.util import lang_func
_ = lang_func.getTranslation().gettext

###########################################################################
## Class iqSelectPassportDialogProto
###########################################################################

class iqSelectPassportDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select passport"), pos = wx.DefaultPosition, size = wx.Size( 939,345 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Passport:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer5.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.psp_staticText = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.psp_staticText.Wrap( -1 )

		self.psp_staticText.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

		bSizer5.Add( self.psp_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer5, 0, wx.EXPAND, 5 )

		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

		self.prj_panel = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.prj_treeListCtrl = wx.lib.gizmos.TreeListCtrl( self.prj_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.TL_DEFAULT_STYLE|wx.dataview.TL_SINGLE )
		self.prj_treeListCtrl.AddColumn( _(u"Name"), 300, wx.ALIGN_LEFT)
		self.prj_treeListCtrl.AddColumn( _(u"Description"), 300, wx.ALIGN_LEFT)

		bSizer2.Add( self.prj_treeListCtrl, 1, wx.EXPAND |wx.ALL, 5 )


		self.prj_panel.SetSizer( bSizer2 )
		self.prj_panel.Layout()
		bSizer2.Fit( self.prj_panel )
		self.res_panel = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.res_treeListCtrl = wx.lib.gizmos.TreeListCtrl( self.res_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.TL_DEFAULT_STYLE|wx.dataview.TL_SINGLE )
		self.res_treeListCtrl.AddColumn( _(u"Name"), 300, wx.ALIGN_LEFT)
		self.res_treeListCtrl.AddColumn( _(u"Description"), 300, wx.ALIGN_LEFT)

		bSizer3.Add( self.res_treeListCtrl, 1, wx.EXPAND |wx.ALL, 5 )


		self.res_panel.SetSizer( bSizer3 )
		self.res_panel.Layout()
		bSizer3.Fit( self.res_panel )
		self.m_splitter1.SplitVertically( self.prj_panel, self.res_panel, 0 )
		bSizer1.Add( self.m_splitter1, 1, wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.del_button = wx.Button( self, wx.ID_ANY, _(u"Delete"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.del_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.cancel_button = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.cancel_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.ok_button = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.ok_button.SetDefault()
		bSizer4.Add( self.ok_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.prj_treeListCtrl.Bind( wx.EVT_TREE_SEL_CHANGED, self.onPrjTreelistSelectionChanged )
		self.res_treeListCtrl.Bind( wx.EVT_TREE_SEL_CHANGED, self.onResTreelistSelectionChanged )
		self.del_button.Bind( wx.EVT_BUTTON, self.onDeleteButtonClick )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onPrjTreelistSelectionChanged( self, event ):
		event.Skip()

	def onResTreelistSelectionChanged( self, event ):
		event.Skip()

	def onDeleteButtonClick( self, event ):
		event.Skip()

	def onCancelButtonClick( self, event ):
		event.Skip()

	def onOkButtonClick( self, event ):
		event.Skip()

	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 0 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )


