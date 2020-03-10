#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Property editor class module.
"""

import sys
import hashlib
import datetime
import os.path
import wx
import wx.propgrid

from ....util import log_func
from ....util import spc_func
from ....util import icon_func

from ... import property_editor_id

from ....engine.wx.dlg import wxdlg_func

from . import passport_property_editor
from . import libicon_property_editor

__version__ = (0, 0, 0, 1)

VALIDATE_ENABLE = True

CUSTOM_PROPERTY_EDITORS = (passport_property_editor.iqPassportPropertyEditor,
                           libicon_property_editor.iqLibraryIconPropertyEditor)


class iqPropertyEditorManager(object):
    """
    Property editor class.
    """
    def registerCustomEditors(self, property_editor=None, *editor_classes):
        """
        Register custom editors.

        :param property_editor: Property grid manager.
        :param editor_classes: Custom editors classes.
        """
        if not editor_classes:
            editor_classes = CUSTOM_PROPERTY_EDITORS
        #
        # Let's use some simple custom editor
        #
        # NOTE: Editor must be registered *before* adding a property that
        # uses it.
        if not getattr(sys, '_PropGridEditorsRegistered', False):
            for editor_class in editor_classes:
                if editor_class:
                    log_func.info(u'Register custom property editor <%s>' % editor_class.__name__)
                    editor_class.setPropertyEditManager(property_editor)
                    property_editor.RegisterEditor(editor_class, editor_class.__name__)
                else:
                    log_func.error(u'Custom property editor not defined')
            # ensure we only do it once
            sys._PropGridEditorsRegistered = True

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

    def createPropertyEditor(self, name, value, property_type=None, spc=None):
        """
        Create wx property.

        :param name: Attribute name.
        :param value: Attribute value.
        :param property_type: Property type.
        :param spc: Component specification.
        :return: wx.Property object.
        """
        wx_property = None

        if property_type is None and spc:
            property_type = self._getAttrEditorType(spc, name)

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
            # log_func.debug(u'Attribute <%s>' % name)
            choices = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('choices', list())
            if isinstance(choices, (list, tuple)):
                choices = [str(item) for item in choices]
            elif callable(choices):
                choices = choices(resource=spc)
            else:
                log_func.error(u'Property editor. Not support choices type <%s : %s>' % (name, type(choices)))
                choices = list()

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
            choices = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('choices', dict())
            if isinstance(choices, dict):
                choices = list(choices.keys())
            elif callable(choices):
                choices = choices()
            else:
                log_func.error(u'Property editor. Not support choices type <%s : %s>' % (name, type(choices)))
                choices = list()
            values = [name for name in choices if name in value]
            wx_property = wx.propgrid.MultiChoiceProperty(name, choices=choices, value=values)

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
            # wx_property.SetAttribute('Hint', 'This is a hint')
            # wx_property.SetAttribute('Password', True)

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

        elif property_type == property_editor_id.PASSPORT_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == property_editor_id.LIBICON_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            wx_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == property_editor_id.FLAG_EDITOR:
            choice_dict = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('choices', dict())
            choices = list(choice_dict.keys())

            values = list()
            for choice_name, code in choice_dict.items():
                if code & value:
                    values.append(choice_name)
            wx_property = wx.propgrid.MultiChoiceProperty(name, choices=choices, value=values)

        else:
            log_func.error(u'Property type <%s> not supported' % property_type)

        if wx_property:
            help_string = spc.get(spc_func.HELP_ATTR_NAME, dict()).get(name, name)
            wx_property.SetHelpString(help_string)
        return wx_property

    def _getAttrEditorType(self, resource, attr_name):
        """
        Get attribute editor type from resource.

        :param resource: Resource struct.
        :param attr_name: Attribute name.
        :return: Attribute editor type code.
        """
        editors = resource.get(spc_func.EDIT_ATTR_NAME, dict())
        edt_type = property_editor_id.READONLY_EDITOR
        if isinstance(editors, dict):
            edt_type = editors.get(attr_name, property_editor_id.READONLY_EDITOR)
            edt_type = edt_type.get('editor',
                                    property_editor_id.READONLY_EDITOR) if isinstance(edt_type,
                                                                                      dict) else edt_type
        else:
            log_func.warning(u'Not define attribute editors in resource component <%s>' % resource.get('type', None))
        # log_func.debug(u'Editor type [%d]' % edt_type)
        return edt_type

    def buildPropertyEditors(self, property_editor=None, resource=None):
        """
        Build all property editors.

        :param property_editor: Property grid manager.
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
            edt_type = self._getAttrEditorType(resource, attr_name)
            wx_property = self.createPropertyEditor(attr_name, resource.get(attr_name, None), edt_type, spc=resource)
            if wx_property is not None:
                prop_page.Append(wx_property)

        # ----------------------------------------
        #   2 - Special attributes
        prop_page.Append(wx.propgrid.PropertyCategory(u'2 - Special'))

        attributes = [attr_name for attr_name in self.getResourceAttributes(resource) if attr_name not in spc_func.BASIC_ATTRIBUTES]
        attributes.sort()
        # log_func.debug(u'Attributes: %s' % str(attributes))
        for attr_name in attributes:
            # log_func.debug(u'Attribute editor <%s> ...' % attr_name)
            edt_type = self._getAttrEditorType(resource, attr_name)
            wx_property = self.createPropertyEditor(attr_name, resource.get(attr_name, None), edt_type, spc=resource)
            if wx_property is not None:
                add_property = prop_page.Append(wx_property)
                # Advanced customization of property editors
                if edt_type == property_editor_id.PASSWORD_EDITOR:
                    # add_property.SetAttribute('Hint', 'This is a hint')
                    add_property.SetAttribute('Password', True)
                elif edt_type == property_editor_id.PASSPORT_EDITOR:
                    property_editor.SetPropertyEditor(attr_name, passport_property_editor.iqPassportPropertyEditor.__name__)
                elif edt_type == property_editor_id.LIBICON_EDITOR:
                    property_editor.SetPropertyEditor(attr_name, libicon_property_editor.iqLibraryIconPropertyEditor.__name__)
                # if edt_type == icDefInf.EDT_PY_SCRIPT:
                #     self.SetPropertyEditor(attr, icpyscriptproperty.icPyScriptPropertyEditor.__name__)
                # elif edt_type == icDefInf.EDT_USER_PROPERTY:
                #     self.SetPropertyEditor(attr, icedituserproperty.icEditUserPropertyEditor.__name__)

        bmp = wx.ArtProvider.GetBitmap('gtk-execute', wx.ART_MENU)
        methods_page = property_editor.AddPage(u'Methods', bmp)

        # ----------------------------------------
        #   3 - Methods page
        methods = self.getResourceMethods(resource)
        for method_name in methods:
            edt_type = self._getAttrEditorType(resource, method_name)
            wx_property = self.createPropertyEditor(method_name, resource.get(method_name, None), edt_type, spc=resource)
            if wx_property is not None:
                methods_page.Append(wx_property)
                # self.SetPropertyEditor(attr, icpyscriptproperty.icPyScriptPropertyEditor.__name__)

        bmp = wx.ArtProvider.GetBitmap('gtk-about', wx.ART_MENU)
        events_page = property_editor.AddPage(u'Events', bmp)

        # ----------------------------------------
        #   4 - Events page
        events = self.getResourceEvents(resource)
        for event_name in events:
            edt_type = self._getAttrEditorType(resource, event_name)
            wx_property = self.createPropertyEditor(event_name, resource.get(event_name, None), edt_type, spc=resource)
            if wx_property is not None:
                events_page.Append(wx_property)
                # self.SetPropertyEditor(attr, icpyscriptproperty.icPyScriptPropertyEditor.__name__)

    def getResourceAttributes(self, resource):
        """
        Get attribute names from resource.

        :param resource: Component resource dictionary.
        :return: Attribute name list.
        """
        edit_section = resource.get(spc_func.EDIT_ATTR_NAME, dict())
        # log_func.debug(u'Resource __edit__ section: %s' % str(edit_section))
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
        res_methods = [attr_name for attr_name,
                       editor_type in list(edit_section.items()) if
                       editor_type == property_editor_id.METHOD_EDITOR]
        res_methods.sort()
        return res_methods

    def getResourceEvents(self, resource):
        """
        Get event names from resource.

        :param resource: Component resource dictionary.
        :return: Event name list.
        """
        edit_section = resource.get(spc_func.EDIT_ATTR_NAME, dict())
        res_events = [attr_name for attr_name,
                      editor_type in list(edit_section.items()) if
                      editor_type == property_editor_id.EVENT_EDITOR]
        res_events.sort()
        return res_events

    def getConvertedValue(self, attr_name, str_value, property_type, spc=None):
        """
        Values converted to type in specification.

        :param attr_name: Attribute name.
        :param str_value: Value as string.
        :param property_type: Property editor type.
        :param spc: Component specification.
        :return: Converted property value or None if error.
        """
        value = None

        if property_type == property_editor_id.STRING_EDITOR:
            value = str_value

        elif property_type == property_editor_id.TEXT_EDITOR:
            value = str_value

        elif property_type == property_editor_id.INTEGER_EDITOR:
            try:
                value = int(str_value)
            except:
                log_func.fatal(u'Error casting to a integer <%s>' % str_value)
                value = 0

        elif property_type == property_editor_id.FLOAT_EDITOR:
            try:
                value = float(str_value.replace(',', '.'))
            except:
                log_func.fatal(u'Error casting to a real number <%s>' % str_value)
                value = 0.0

        elif property_type == property_editor_id.CHOICE_EDITOR:
            value = str_value

        elif property_type == property_editor_id.CHECKBOX_EDITOR:
            try:
                value = eval(str_value)
            except:
                log_func.fatal(u'Error casting to a boolean <%s>' % str_value)
                value = False

        elif property_type == property_editor_id.MULTICHOICE_EDITOR:
            try:
                value = eval(str_value)
            except:
                log_func.fatal(u'Error casting to a multichoice string list <%s>' % str_value)

        elif property_type == property_editor_id.STRINGLIST_EDITOR:
            try:
                value = eval(str_value)
            except:
                log_func.fatal(u'Error casting to a string list <%s>' % str_value)

        elif property_type == property_editor_id.READONLY_EDITOR:
            try:
                value = eval(str_value)
            except:
                value = str_value

        elif property_type == property_editor_id.EXTERNAL_EDITOR:
            value = str_value

        elif property_type == property_editor_id.CUSTOM_EDITOR:
            value = str_value

        elif property_type == property_editor_id.COLOUR_EDITOR:
            try:
                value = eval(str_value)
            except NameError:
                # If the colour is specified by name
                colour_name = str_value.upper()
                colour = wx.Colour(colour_name)
                value = (colour.Red(), colour.Green(), colour.Blue())

        elif property_type == property_editor_id.FONT_EDITOR:
            value = dict()
            value_list = str_value.split('; ')
            value['type'] = 'Font'
            value['name'] = 'default'
            value['size'] = value_list[0]
            value['face_name'] = value_list[1]
            value['style'] = value_list[2]
            value['weight'] = value_list[3]
            value['underline'] = value_list[4]
            value['family'] = value_list[5]

        elif property_type == property_editor_id.POINT_EDITOR:
            try:
                value = eval(str_value)
            except:
                log_func.fatal(u'Point value <%s> convert error' % str_value)
                value = (0, 0)

        elif property_type == property_editor_id.SIZE_EDITOR:
            try:
                value = eval(str_value)
            except:
                log_func.fatal(u'Size value <%s> convert error' % str_value)
                value = (0, 0)

        elif property_type == property_editor_id.PASSWORD_EDITOR:
            value = hashlib.md5(str_value.encode()).hexdigest()

        elif property_type == property_editor_id.FILE_EDITOR:
            value = str_value

        elif property_type == property_editor_id.DIR_EDITOR:
            value = str_value

        elif property_type == property_editor_id.IMAGE_EDITOR:
            value = str_value

        elif property_type == property_editor_id.SCRIPT_EDITOR:
            value = str_value

        elif property_type == property_editor_id.METHOD_EDITOR:
            value = str_value

        elif property_type == property_editor_id.EVENT_EDITOR:
            value = str_value

        elif property_type == property_editor_id.PASSPORT_EDITOR:
            value = str_value

        elif property_type == property_editor_id.LIBICON_EDITOR:
            lib_icon_path = icon_func.getIconPath()
            value = str_value.replace(lib_icon_path, '')
            if value.endswith(icon_func.ICON_FILENAME_EXT):
                value = value.replace(icon_func.ICON_FILENAME_EXT, '')
            if value.startswith(os.path.sep):
                value = value[1:]

        elif property_type == property_editor_id.FLAG_EDITOR:
            choice_dict = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(attr_name, dict()).get('choices', dict())
            values = [item.strip('"') for item in str_value.split(' ')]
            value = 0
            for value_name in values:
                value |= choice_dict.get(value_name, 0)

        else:
            log_func.error(u'Not support property editor. Code [%d]' % property_type)

        return value

    def convertPropertyValue(self, name, str_value, spc):
        """
        Convert the property value to the type specified in the specification.

        :param name: Attribute name.
        :param str_value: Value as string.
        :param spc: Component specification.
        """
        value = None
        if spc is None:
            log_func.error(u'Not define component specification')
            return None

        property_type = self.findPropertyType(name, spc)
        if property_type is None:
            # По умолчанию все не определенные атрибуты - скриптовые
            property_type = property_editor_id.SCRIPT_EDITOR
        value = self.getConvertedValue(name, str_value, property_type, spc)
        log_func.debug(u'Convert property value <%s : %s : %s>' % (name, str_value, property_type))
        return value

    def findPropertyEditor(self, name, spc):
        """
        Get property/attribute editor dictionary.

        :type name: C{string}
        :param name: Attribute name.
        :rtype: C{int}
        :param spc: Fill component specification.
        :return: Property/attribute editor dictionary or None if not found.
        """
        editor = None

        editors = spc.get(spc_func.EDIT_ATTR_NAME, dict())
        for attr_name, attr_editor in editors.items():
            if attr_name == name:
                editor = attr_editor
                break

        # Find in parent specification
        if editor is None and spc_func.PARENT_ATTR_NAME in spc:
            editor = self.findPropertyEditor(name, spc[spc_func.PARENT_ATTR_NAME])
        return editor

    def validatePropertyValue(self, name, value, spc):
        """
        Validate property value.

        :type name: C{string}
        :param name: Attribute name.
        :type value: C{string}
        :param value: Attribute value.
        :rtype: C{int}
        :param spc: Fill component specification.
        :return: True - valid / False - not valid.
        """
        if not VALIDATE_ENABLE:
            return True
        valid = True

        # Valid attribute type
        editor = self.findPropertyEditor(name, spc)

        if editor is None:
            msg = u'Not define attribute editor <%s>' % name
            log_func.error(msg)
            wxdlg_func.openErrBox(u'VALIDATION', msg)
            valid = False
        elif isinstance(editor, int):
            # No need to valid
            pass
        elif isinstance(editor, dict):
            if 'valid' in editor and callable(editor['valid']):
                try:
                    valid = editor['valid'](value)
                except:
                    msg = 'Valid property/attribute <%s : %s> error' % (name, value)
                    log_func.fatal(msg)
                    wxdlg_func.openFatalBox(u'VALIDATION', msg)
                    valid = False
        else:
            log_func.error(u'Not support property/attribute editor type <%s>' % type(editor))
            valid = False

        return valid

    def findPropertyType(self, name, spc):
        """
        Find in specification property/attribute type.

        :param name: Property/Attribute name.
        :param spc: Component specification.
        :return: Property editor type or None if not found.
        """
        property_type = None

        editors = spc.get(spc_func.EDIT_ATTR_NAME, dict())
        if name in editors:
            attr_editor = editors[name]

            if isinstance(attr_editor, int):
                property_type = attr_editor
            elif isinstance(attr_editor, dict):
                property_type = attr_editor.get('editor', None)
            else:
                log_func.error(u'Not supported property editor type <%s : %s> in <%s> specification' % (name,
                                                                                                        type(attr_editor),
                                                                                                        spc.get('type', None)))

        # Find in parent specification
        if property_type is None and spc_func.PARENT_ATTR_NAME in spc:
            property_type = self.findPropertyType(name, spc[spc_func.PARENT_ATTR_NAME])
        return property_type

    def getPropertyValueAsString(self, property, name, spc):
        """
        Get property value as string.

        :param property: Property object.
        :param name: Attribute name.
        :param spc: Component specification.
        :return: Property value as string.
        """
        editor = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, None)
        if editor == property_editor_id.PASSWORD_EDITOR:
            str_value = str(property.GetValue())
        else:
            str_value = property.GetValueAsString()
        # log_func.info(u'Property [%s]. New value <%s>' % (name, str_value))
        return str_value

