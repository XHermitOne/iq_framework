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
# import wx.calendar

###########################################################################
## Class calendarDialogProto
###########################################################################

class calendarDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Календарь", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.calendarCtrl = wx.adv.CalendarCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.CAL_SHOW_HOLIDAYS )
		bSizer1.Add( self.calendarCtrl, 0, wx.ALL, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer2.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class yearDialogProto
###########################################################################

class yearDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор года", pos = wx.DefaultPosition, size = wx.Size( 351,130 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Год:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer5.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		year_choiceChoices = []
		self.year_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, year_choiceChoices, 0 )
		self.year_choice.SetSelection( 0 )
		bSizer5.Add( self.year_choice, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.cancelButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer4.Add( self.okButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer3.Add( bSizer4, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class monthDialogProto
###########################################################################

class monthDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор месяца", pos = wx.DefaultPosition, size = wx.Size( 390,130 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Месяц:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer7.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		month_choiceChoices = [ u"Январь", u"Февраль", u"Март", u"Апрель", u"Май", u"Июнь", u"Июль", u"Август", u"Сентябрь", u"Октябрь", u"Ноябрь", u"Декабрь" ]
		self.month_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, month_choiceChoices, 0 )
		self.month_choice.SetSelection( 0 )
		bSizer7.Add( self.month_choice, 1, wx.ALL|wx.EXPAND, 5 )
		
		year_choiceChoices = []
		self.year_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, year_choiceChoices, 0 )
		self.year_choice.SetSelection( 0 )
		bSizer7.Add( self.year_choice, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer6.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer8.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer8, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class monthRangeDialogProto
###########################################################################

class monthRangeDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор периода", pos = wx.DefaultPosition, size = wx.Size( 393,179 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 2, 3, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.AddGrowableCol( 2 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"с:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		month_first_choiceChoices = [ u"Январь", u"Февраль", u"Март", u"Апрель", u"Май", u"Июнь", u"Июль", u"Август", u"Сентябрь", u"Октябрь", u"Ноябрь", u"Декабрь", wx.EmptyString ]
		self.month_first_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, month_first_choiceChoices, 0 )
		self.month_first_choice.SetSelection( 0 )
		fgSizer1.Add( self.month_first_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		year_first_choiceChoices = []
		self.year_first_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, year_first_choiceChoices, 0 )
		self.year_first_choice.SetSelection( 0 )
		fgSizer1.Add( self.year_first_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"по:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		fgSizer1.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		month_last_choiceChoices = [ u"Январь", u"Февраль", u"Март", u"Апрель", u"Май", u"Июнь", u"Июль", u"Август", u"Сентябрь", u"Октябрь", u"Ноябрь", u"Декабрь", wx.EmptyString ]
		self.month_last_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, month_last_choiceChoices, 0 )
		self.month_last_choice.SetSelection( 0 )
		fgSizer1.Add( self.month_last_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		year_last_choiceChoices = []
		self.year_last_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, year_last_choiceChoices, 0 )
		self.year_last_choice.SetSelection( 0 )
		fgSizer1.Add( self.year_last_choice, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer6.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer8.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer8, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class dateRangeDialogProto
###########################################################################

class dateRangeDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор периода", pos = wx.DefaultPosition, size = wx.Size( 391,193 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.concrete_date_checkBox = wx.CheckBox( self, wx.ID_ANY, u"На определенную дату", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer20.Add( self.concrete_date_checkBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer6.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.AddGrowableRow( 0 )
		fgSizer2.AddGrowableRow( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"с:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.firstDatePicker = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		fgSizer2.Add( self.firstDatePicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"по:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		fgSizer2.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.lastDatePicker = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT )
		fgSizer2.Add( self.lastDatePicker, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer6.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer8.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer8, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.concrete_date_checkBox.Bind( wx.EVT_CHECKBOX, self.onConcreteDateCheckBox )
		self.firstDatePicker.Bind( wx.adv.EVT_DATE_CHANGED, self.onFirstDateChanged )
		self.lastDatePicker.Bind( wx.adv.EVT_DATE_CHANGED, self.onLastDateChanged )
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onConcreteDateCheckBox( self, event ):
		event.Skip()
	
	def onFirstDateChanged( self, event ):
		event.Skip()
	
	def onLastDateChanged( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class NSIListDialogProto
###########################################################################

class NSIListDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор значения справочника", pos = wx.DefaultPosition, size = wx.Size( 586,570 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		nsi_listBoxChoices = []
		self.nsi_listBox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, nsi_listBoxChoices, 0 )
		bSizer13.Add( self.nsi_listBox, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetDefault() 
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
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class integerDialogProto
###########################################################################

class integerDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Целое значение", pos = wx.DefaultPosition, size = wx.Size( 509,134 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.label_staticText = wx.StaticText( self, wx.ID_ANY, u"Значение:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_staticText.Wrap( -1 )
		bSizer19.Add( self.label_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.value_spinCtrl = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 500, 0 )
		bSizer19.Add( self.value_spinCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer15.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer2.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer15 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class radioChoiceDialogProto
###########################################################################

class radioChoiceDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор элемента", pos = wx.DefaultPosition, size = wx.Size( 566,133 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		choice_radioBoxChoices = [ u"Item1", u"Item2", u"item 3", u"item 4", u"item5" ]
		self.choice_radioBox = wx.RadioBox( self, wx.ID_ANY, u"Title", wx.DefaultPosition, wx.DefaultSize, choice_radioBoxChoices, 1, wx.RA_SPECIFY_ROWS )
		self.choice_radioBox.SetSelection( 0 )
		self.choice_radioBox.SetMinSize( wx.Size( -1,80 ) )
		
		bSizer19.Add( self.choice_radioBox, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer2.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer19 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class intRangeDialogProto
###########################################################################

class intRangeDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Диапазон номеров", pos = wx.DefaultPosition, size = wx.Size( 536,152 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.begin_staticText = wx.StaticText( self, wx.ID_ANY, u"Первый номер:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.begin_staticText.Wrap( -1 )
		bSizer22.Add( self.begin_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.begin_spinCtrl = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 1000, 1 )
		bSizer22.Add( self.begin_spinCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer21.Add( bSizer22, 1, wx.EXPAND, 5 )
		
		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.end_staticText = wx.StaticText( self, wx.ID_ANY, u"Последний номер:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.end_staticText.Wrap( -1 )
		bSizer23.Add( self.end_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.end_spinCtrl = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 2, 1000, 2 )
		bSizer23.Add( self.end_spinCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer21.Add( bSizer23, 1, wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer2.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer21.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer21 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.begin_spinCtrl.Bind( wx.EVT_SPINCTRL, self.onBeginSpinCtrl )
		self.end_spinCtrl.Bind( wx.EVT_SPINCTRL, self.onEndSpinCtrl )
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onBeginSpinCtrl( self, event ):
		event.Skip()
	
	def onEndSpinCtrl( self, event ):
		event.Skip()
	
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class checkBoxDialogProto
###########################################################################

class checkBoxDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор элементов", pos = wx.DefaultPosition, size = wx.Size( 753,130 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.Size( -1,130 ), wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.label_staticText = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_staticText.Wrap( -1 )
		bSizer19.Add( self.label_staticText, 0, wx.ALL, 5 )
		
		bSizer27 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.item_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox2 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox3 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox4 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox5 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox6 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox7 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer27, 1, wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer2.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer19 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class radioChoiceMaxiDialogProto
###########################################################################

class radioChoiceMaxiDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор элемента", pos = wx.DefaultPosition, size = wx.Size( 566,503 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		choice_radioBoxChoices = [ u"Item1", u"item 5", u"Item 2", u"item 4", u"item 5", u"item 6", u"item 7", u"item 8", u"item 9", u"item 10", u"item 11", u"item 12", u"item 13", u"item 14", u"item 15" ]
		self.choice_radioBox = wx.RadioBox( self, wx.ID_ANY, u"Title", wx.DefaultPosition, wx.DefaultSize, choice_radioBoxChoices, 1, wx.RA_SPECIFY_COLS )
		self.choice_radioBox.SetSelection( 0 )
		bSizer19.Add( self.choice_radioBox, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer2.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer19 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class checkBoxMaxiDialogProto
###########################################################################

class checkBoxMaxiDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор элементов", pos = wx.DefaultPosition, size = wx.Size( 525,601 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.Size( -1,130 ), wx.DefaultSize )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.label_staticText = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_staticText.Wrap( -1 )
		bSizer19.Add( self.label_staticText, 0, wx.ALL, 5 )
		
		bSizer27 = wx.BoxSizer( wx.VERTICAL )
		
		self.item_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox2 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox3 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox4 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox5 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox6 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox7 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.item_checkBox8 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox8, 0, wx.ALL, 5 )
		
		self.item_checkBox9 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox9, 0, wx.ALL, 5 )
		
		self.item_checkBox10 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox10, 0, wx.ALL, 5 )
		
		self.item_checkBox11 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox11, 0, wx.ALL, 5 )
		
		self.item_checkBox12 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox12, 0, wx.ALL, 5 )
		
		self.item_checkBox13 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox13, 0, wx.ALL, 5 )
		
		self.item_checkBox14 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox14, 0, wx.ALL, 5 )
		
		self.item_checkBox15 = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer27.Add( self.item_checkBox15, 0, wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer27, 1, wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer2.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer2, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer19 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

###########################################################################
## Class checkListBoxDialogProto
###########################################################################

class checkListBoxDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор элементов", pos = wx.DefaultPosition, size = wx.Size( 579,598 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer33 = wx.BoxSizer( wx.VERTICAL )
		
		self.label_staticText = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_staticText.Wrap( -1 )
		bSizer33.Add( self.label_staticText, 0, wx.ALL, 5 )
		
		items_checkListChoices = []
		self.items_checkList = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, items_checkListChoices, 0 )
		bSizer33.Add( self.items_checkList, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.ok_button, 0, wx.ALL, 5 )
		
		
		bSizer33.Add( bSizer35, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer33 )
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
	

###########################################################################
## Class quarterDialogProto
###########################################################################

class quarterDialogProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Выбор квартала", pos = wx.DefaultPosition, size = wx.Size( 477,130 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Квартал:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer7.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		quarter_choiceChoices = [ u"Первый (январь - март)", u"Второй (апрель - июнь)", u"Третий (июль - сентябрь)", u"Четвертый (октябрь - декабрь)" ]
		self.quarter_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, quarter_choiceChoices, 0 )
		self.quarter_choice.SetSelection( 0 )
		bSizer7.Add( self.quarter_choice, 1, wx.ALL|wx.EXPAND, 5 )
		
		year_choiceChoices = []
		self.year_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, year_choiceChoices, 0 )
		self.year_choice.SetSelection( 0 )
		bSizer7.Add( self.year_choice, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer6.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.cancelButton, 0, wx.ALL, 5 )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"ОК", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.okButton.SetDefault() 
		bSizer8.Add( self.okButton, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer8, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancelButton.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.okButton.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()
	
	def onOkButtonClick( self, event ):
		event.Skip()
	

