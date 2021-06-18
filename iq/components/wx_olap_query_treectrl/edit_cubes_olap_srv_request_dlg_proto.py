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
from ..cubes_olap_server import cubes_olap_srv_request_panel
from ..cubes_olap_server import cubes_pivot_table_request_panel

from iq.util import lang_func
_ = lang_func.getTranslation().gettext

###########################################################################
## Class iqEditCubesOLAPSrvRequestDlgProto
###########################################################################

class iqEditCubesOLAPSrvRequestDlgProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edit OLAP server request"), pos = wx.DefaultPosition, size = wx.Size( 874,736 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.request_panel = cubes_olap_srv_request_panel.iqCubesOLAPSrvRequestPanel(parent=self)
		bSizer13.Add( self.request_panel, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.refresh_button = wx.Button( self, wx.ID_ANY, _(u"Address"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.refresh_button, 0, wx.ALL, 5 )


		bSizer14.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.cancel_button = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.cancel_button, 0, wx.ALL, 5 )

		self.ok_button = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.ok_button, 0, wx.ALL, 5 )


		bSizer13.Add( bSizer14, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )


		self.SetSizer( bSizer13 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.refresh_button.Bind( wx.EVT_BUTTON, self.onRefreshButtonClick )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onRefreshButtonClick(self, event):
		event.Skip()

	def onCancelButtonClick(self, event):
		event.Skip()

	def onOkButtonClick(self, event):
		event.Skip()


###########################################################################
## Class iqEditCubesPivotTabRequestDlgProto
###########################################################################

class iqEditCubesPivotTabRequestDlgProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edir pivot table request"), pos = wx.DefaultPosition, size = wx.Size( 874,736 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.request_panel = cubes_pivot_table_request_panel.iqCubesPivotTabRequestPanel(parent=self)
		bSizer13.Add( self.request_panel, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.cancel_button = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.cancel_button, 0, wx.ALL, 5 )

		self.ok_button = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.ok_button, 0, wx.ALL, 5 )


		bSizer13.Add( bSizer14, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer13 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick(self, event):
		event.Skip()

	def onOkButtonClick(self, event):
		event.Skip()


