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
## Class iqMainMenubarProto
###########################################################################

class iqMainMenubarProto ( wx.MenuBar ):

	def __init__( self ):
		wx.MenuBar.__init__ ( self, style = 0 )

		self.help_menu = wx.Menu()
		self.about_menuItem = wx.MenuItem( self.help_menu, wx.ID_ANY, _(u"About..."), wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.Append( self.about_menuItem )

		self.Append( self.help_menu, _(u"Help") )


	def __del__( self ):
		pass


