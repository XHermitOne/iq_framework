#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Property editor class module.
"""

import datetime
import wx
import wx.propgrid

from ....util import log_func
from ....util import spc_func

from ... import property_editor_id

__version__ = (0, 0, 0, 1)


class iqPropertyEditorManager(object):
    """
    Property editor class.
    """
    def clearProperties(self, property_editor=None):
        """
        Clear property editor.

        :return: True/False
        """
        if property_editor:
            property_editor.Clear()
            bmp = wx.ArtProvider.GetBitmap('gtk-index', wx.ART_MENU)
            property_editor.AddPage(u'Properties', bmp)
            bmp = wx.ArtProvider.GetBitmap('gtk-execute', wx.ART_MENU)
            property_editor.AddPage(u'Methods', bmp)
            bmp = wx.ArtProvider.GetBitmap('gtk-about', wx.ART_MENU)
            property_editor.AddPage(u'Events', bmp)
            return True
        else:
            log_func.error(u'Not define property editor')
        return False

    def createPropertyEditor(self, name, value, property_type, spc=None):
        """
        Create wx property.

        :param name: Attribute name.
        :param value: Attribute value.
        :param property_type: Property type.
        :param spc: Component specification.
        :return: wx.Property object.
        """
        wx_property = None

        if property_type == property_editor_id.STRING_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == property_editor_id.TEXT_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            wx_property = wx.propgrid.LongStringProperty(name, value=value)

        elif property_type == property_editor_id.INTEGER_EDITOR:
            value = int(value) if value else 0
            wx_property = wx.propgrid.IntProperty(name, value=value)

        elif property_type == property_editor_id.FLOAT_EDITOR:
            value = float(value) if value else 0.0
            wx_property = wx.propgrid.FloatProperty(name, value=value)

        elif property_type == property_editor_id.CHOICE_EDITOR:
            choices = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('choices', list())
            choices = [str(item) for item in choices]
            idx = choices.index(value) if value in choices else 0
            wx_property = wx.propgrid.EnumProperty(name, name, choices,
                                                   [i for i in range(len(choices))], idx)

        elif property_type == property_editor_id.CHECKBOX_EDITOR:
            if isinstance(value, str):
                value = eval(value)
            value = bool(value)
            wx_property = wx.propgrid.BoolProperty(name, value=value)
            wx_property.SetAttribute('UseCheckbox', True)

        elif property_type == property_editor_id.MULTICHOICE_EDITOR:
            # choice_list = None
            # codes = None
            # value_list = []

            choices_dict = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('choices', dict())
            choices = list(choices_dict.keys())
            str_value_lst = [key for key, code in choices_dict.items() if code & value]
            wx_property = wx.propgrid.MultiChoiceProperty(name, choices=choices, value=str_value_lst)

        elif property_type == property_editor_id.STRINGLIST_EDITOR:
            value_list = []
            if isinstance(value, (list, tuple)):
                for item in value:
                    if not isinstance(item, str):
                        item = str(item)
                    value_list.append(item)
            wx_property = wx.propgrid.ArrayStringProperty(name, value=value_list)

        elif property_type in (property_editor_id.SCRIPT_EDITOR,
                               property_editor_id.METHOD_EDITOR,
                               property_editor_id.EVENT_EDITOR):
            if value is None:
                value = str(value)
            elif isinstance(value, str):
                pass
            elif isinstance(value, (int, float, list, tuple, dict, bool)):
                value = str(value)
            elif isinstance(value, datetime.datetime):
                # Если указывается время, то скорее всего это текущее время
                value = u'datetime.datetime.now()'
            elif isinstance(value, datetime.date):
                # Если указывается день, то скорее всего это сегодняшний
                value = u'datetime.date.today()'
            else:
                log_func.warning(u'Attribute [%s]. Property editor <Python script> for type <%s> not supported' % (name, value.__class__.__name__))
                value = u''
            wx_property = wx.propgrid.LongStringProperty(name, value=value)

        elif property_type == property_editor_id.READONLY_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)
            wx_property.Enable(False)

        elif property_type == property_editor_id.EXTERNAL_EDITOR:
            log_func.warning(u'Attribute [%s]. Property editor <External editor> not supported' % name)

        elif property_type == property_editor_id.CUSTOM_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == property_editor_id.COLOUR_EDITOR:
            colour = None
            if isinstance(value, (list, tuple)):
                colour = wx.Colour(*value)
            wx_property = wx.propgrid.ColourProperty(name, value=colour)

        elif property_type == property_editor_id.FONT_EDITOR:
            value = value if value else dict()
            font = wx.Font(value)
            wx_property = wx.propgrid.FontProperty(name, value=font)

        elif property_type == property_editor_id.POINT_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == property_editor_id.SIZE_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == property_editor_id.PASSWORD_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)
            wx_property.SetAttribute('Hint', 'This is a hint')
            wx_property.SetAttribute('Password', True)

        elif property_type == property_editor_id.FILE_EDITOR:
            if not isinstance(value, str):
                value = u''
            wx_property = wx.propgrid.FileProperty(name, value=value)

        elif property_type == property_editor_id.DIR_EDITOR:
            if not isinstance(value, str):
                value = u''
            wx_property = wx.propgrid.DirProperty(name, value=value)

        elif property_type == property_editor_id.IMAGE_EDITOR:
            if not isinstance(value, str):
                value = u''
            wx_property = wx.propgrid.ImageFileProperty(name, value=value)

        elif property_type == property_editor_id.DATE_EDITOR:
            wx_property = wx.propgrid.DateProperty(name, value=value)

        else:
            log_func.error(u'Property type <%s> not supported' % property_type)

        if wx_property:
            help_string = spc.get(spc_func.HELP_ATTR_NAME, dict()).get(name, name)
            wx_property.SetHelpString(help_string)
        return wx_property

    def buildPropertyEditors(self, property_editor=None, resource=None):
        """
        Build all property editors.

        :param resource: Component resource.
        :return: True/False.
        """
        if property_editor is None:
            log_func.error(u'Not define property editor')
            return False

        if resource is None:
            log_func.warning(u'Not define component resource for edit')
            return False

        property_editor.Clear()

        bmp = wx.ArtProvider.GetBitmap('gtk-index', wx.ART_MENU)
        prop_page = property_editor.AddPage(u'Properties', bmp)
        # ---------------------------------------
        #   1 - Basic attributes
        prop_page.Append(wx.propgrid.PropertyCategory(u'1 - Basic'))

        attributes = spc_func.BASIC_ATTRIBUTES
        for attr_name in attributes:
            edt_type = resource.get(spc_func.EDIT_ATTR_NAME, dict())
            if isinstance(edt_type, dict):
                edt_type = edt_type.get('editor', property_editor_id.READONLY_EDITOR)
            wx_property = self.createPropertyEditor(attr_name, resource.get(attr_name, None), edt_type, spc=resource)
            if wx_property is not None:
                prop_page.Append(wx_property)

        # ----------------------------------------
        #   2 - Special attributes
        prop_page.Append(wx.propgrid.PropertyCategory(u'2 - Special'))

        attributes = [attr_name for attr_name in self.getResourceAttributes(resource) if attr_name not in spc_func.BASIC_ATTRIBUTES]
        for attr_name in attributes:
            edt_type = resource.get(spc_func.EDIT_ATTR_NAME, dict())
            if isinstance(edt_type, dict):
                edt_type = edt_type.get('editor', property_editor_id.READONLY_EDITOR)
            wx_property = self.createPropertyEditor(attr_name, resource.get(attr_name, None), edt_type, spc=resource)
            if wx_property is not None:
                prop_page.Append(wx_property)
                # if edt_type == icDefInf.EDT_PY_SCRIPT:
                #     # Связывать расширенный редактор со свойством можно только после добавления
                #     # свойства
                #     self.SetPropertyEditor(attr, icpyscriptproperty.icPyScriptPropertyEditor.__name__)
                # elif edt_type == icDefInf.EDT_USER_PROPERTY:
                #     # Связывать расширенный редактор со свойством можно только после добавления
                #     # свойства
                #     self.SetPropertyEditor(attr, icedituserproperty.icEditUserPropertyEditor.__name__)

        bmp = wx.ArtProvider.GetBitmap('gtk-execute', wx.ART_MENU)
        methods_page = property_editor.AddPage(u'Methods', bmp)

        # ----------------------------------------
        #   3 - Methods page
        methods = self.getResourceMethods(resource)
        for method_name in methods:
            edt_type = resource.get(spc_func.EDIT_ATTR_NAME, dict())
            if isinstance(edt_type, dict):
                edt_type = edt_type.get('editor', property_editor_id.READONLY_EDITOR)
            wx_property = self.createPropertyEditor(method_name, resource.get(method_name, None), edt_type, spc=resource)
            if wx_property is not None:
                methods_page.Append(wx_property)
                # Связывать расширенный редактор со свойством можно только после добавления
                # свойства
                # self.SetPropertyEditor(attr, icpyscriptproperty.icPyScriptPropertyEditor.__name__)

        bmp = wx.ArtProvider.GetBitmap('gtk-about', wx.ART_MENU)
        events_page = property_editor.AddPage(u'Events', bmp)

        # ----------------------------------------
        #   4 - Events page
        events = self.getResourceEvents(resource)
        for event_name in events:
            edt_type = resource.get(spc_func.EDIT_ATTR_NAME, dict())
            if isinstance(edt_type, dict):
                edt_type = edt_type.get('editor', property_editor_id.READONLY_EDITOR)
            wx_property = self.createPropertyEditor(event_name, resource.get(event_name, None), edt_type, spc=resource)
            if wx_property is not None:
                events_page.Append(wx_property)
                # Связывать расширенный редактор со свойством можно только после добавления
                # свойства
                # self.SetPropertyEditor(attr, icpyscriptproperty.icPyScriptPropertyEditor.__name__)

    def getResourceAttributes(self, resource):
        """
        Get attribute names from resource.

        :param resource: Component resource dictionary.
        :return: Attribute name list.
        """
        edit_section = resource.get(spc_func.EDIT_ATTR_NAME, dict())
        return [attr_name for attr_name,
                              editor_type in list(edit_section.items()) if
                editor_type not in (property_editor_id.METHOD_EDITOR,
                                    property_editor_id.EVENT_EDITOR)]

    def getResourceMethods(self, resource):
        """
        Get method names from resource.

        :param resource: Component resource dictionary.
        :return: Method name list.
        """
        edit_section = resource.get(spc_func.EDIT_ATTR_NAME, dict())
        return [attr_name for attr_name,
                              editor_type in list(edit_section.items()) if
                editor_type == property_editor_id.METHOD_EDITOR]

    def getResourceEvents(self, resource):
        """
        Get event names from resource.

        :param resource: Component resource dictionary.
        :return: Event name list.
        """
        edit_section = resource.get(spc_func.EDIT_ATTR_NAME, dict())
        return [attr_name for attr_name,
                              editor_type in list(edit_section.items()) if
                editor_type == property_editor_id.EVENT_EDITOR]
