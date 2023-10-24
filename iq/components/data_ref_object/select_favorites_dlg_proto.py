# -*- coding: utf-8 -*-

###########################################################################
## Adapted Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.lib.gizmos
import wx.aui
from iq.components.wx_refobjmultiplecheckcomboctrl import refobjmultiplecheckcomboctrl

from iq.util import lang_func
_ = lang_func.getTranslation().gettext

###########################################################################
## Class iqSelectFavoritesDialogProto
###########################################################################

class iqSelectFavoritesDialogProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"FAVORITES"), pos = wx.DefaultPosition, size = wx.Size( 1144,237 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.from_staticText = wx.StaticText( self, wx.ID_ANY, _(u"..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.from_staticText.Wrap( -1 )

		self.from_staticText.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

		bSizer3.Add( self.from_staticText, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_TOOLBAR ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_bitmap1, 0, wx.ALL, 5 )

		self.to_staticText = wx.StaticText( self, wx.ID_ANY, _(u"..."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.to_staticText.Wrap( -1 )

		self.to_staticText.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Sans" ) )

		bSizer3.Add( self.to_staticText, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )

		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )

		self.from_ref_obj_comboctrl = refobjmultiplecheckcomboctrl.iqRefObjMultipleCheckComboCtrlProto(parent=self)
		bSizer41.Add( self.from_ref_obj_comboctrl, 1, wx.ALL, 5 )

		self.clear_bpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )

		self.clear_bpButton.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_MISSING_IMAGE, wx.ART_MENU ) )
		bSizer41.Add( self.clear_bpButton, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer41, 1, wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.cancel_button = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.cancel_button, 0, wx.ALL, 5 )

		self.add_button = wx.Button( self, wx.ID_ANY, _(u"Add"), wx.DefaultPosition, wx.DefaultSize, 0 )

		self.add_button.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_PLUS, wx.ART_MENU ) )
		self.add_button.SetBitmapPosition( wx.LEFT )
		bSizer4.Add( self.add_button, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer4, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.clear_bpButton.Bind( wx.EVT_BUTTON, self.onClearButtonClick )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.add_button.Bind( wx.EVT_BUTTON, self.onAddButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onClose(self, event):
		event.Skip()

	def onClearButtonClick(self, event):
		event.Skip()

	def onCancelButtonClick(self, event):
		event.Skip()

	def onAddButtonClick(self, event):
		event.Skip()


