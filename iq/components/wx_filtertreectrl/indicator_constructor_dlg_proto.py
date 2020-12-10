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
import wx.stc

###########################################################################
## Class iqIndicatorConstructorDlgProto
###########################################################################

class iqIndicatorConstructorDlgProto ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Filter indicator", pos = wx.DefaultPosition, size = wx.Size( 776,724 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.ctrl_toolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.moveup_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Выше", u"Выше", None )

		self.movedown_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Ниже", u"Ниже", None )

		self.ctrl_toolBar.AddSeparator()

		self.add_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Добавить", u"Добавить", None )

		self.del_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Удалить", u"Удалить", None )

		self.save_tool = self.ctrl_toolBar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Сохранить", u"Сохранить", None )

		self.ctrl_toolBar.Realize()

		bSizer1.Add( self.ctrl_toolBar, 0, wx.EXPAND, 5 )

		self.indicator_listCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer1.Add( self.indicator_listCtrl, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Наименование:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.name_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.name_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.image_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Образ:", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.image_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.image_bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_MISSING_IMAGE, wx.ART_MENU ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.image_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.image_filePicker = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Файл образа", u"Файлы образов (*.png)|*.png", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer3.Add( self.image_filePicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.textcolor_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Цвет текста:", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.textcolor_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textcolor_colourPicker = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer4.Add( self.textcolor_colourPicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.bgcolor_checkBox = wx.CheckBox( self, wx.ID_ANY, u"Цвет фона:", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.bgcolor_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.bgcolor_colourPicker = wx.ColourPickerCtrl( self, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer4.Add( self.bgcolor_colourPicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )

		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"Выражение:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )

		bSizer1.Add( self.m_staticText31, 0, wx.ALL, 5 )

		self.expression_edit = wx.stc.StyledTextCtrl(parent=self, id=wx.NewId())
		bSizer1.Add( self.expression_edit, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"* Выражение должно возвращать True/False. True - индикатор в текущем состоянии и дальнейшая проверка не нужна. False - индикатор не в текущем стостоянии,\nпроисходит дальнейшая проверка других состояний.\nCначала должны проверятся самые критичные состояния (они должные стоять в списке описаний состояний на первом месте), а затем менее критичные.\nПри выполнении выражения в его окружении присутствует объект RECORDS. RECORDS - список словарей записей.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.cancel_button, 0, wx.ALL, 5 )

		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.ok_button, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer8, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onMoveUpToolClicked, id = self.moveup_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onMoveDownToolClicked, id = self.movedown_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onAddToolClicked, id = self.add_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onDelToolClicked, id = self.del_tool.GetId() )
		self.Bind( wx.EVT_TOOL, self.onSaveToolClicked, id = self.save_tool.GetId() )
		self.indicator_listCtrl.Bind( wx.EVT_LIST_ITEM_SELECTED, self.onIndicatorListItemSelected )
		self.image_checkBox.Bind( wx.EVT_CHECKBOX, self.onImageCheckBox )
		self.image_filePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.onImageFileChanged )
		self.textcolor_checkBox.Bind( wx.EVT_CHECKBOX, self.onTextColorCheckBox )
		self.bgcolor_checkBox.Bind( wx.EVT_CHECKBOX, self.onBGColorCheckBox )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onMoveUpToolClicked( self, event ):
		event.Skip()

	def onMoveDownToolClicked( self, event ):
		event.Skip()

	def onAddToolClicked( self, event ):
		event.Skip()

	def onDelToolClicked( self, event ):
		event.Skip()

	def onSaveToolClicked( self, event ):
		event.Skip()

	def onIndicatorListItemSelected( self, event ):
		event.Skip()

	def onImageCheckBox( self, event ):
		event.Skip()

	def onImageFileChanged( self, event ):
		event.Skip()

	def onTextColorCheckBox( self, event ):
		event.Skip()

	def onBGColorCheckBox( self, event ):
		event.Skip()

	def onCancelButtonClick( self, event ):
		event.Skip()

	def onOkButtonClick( self, event ):
		event.Skip()


