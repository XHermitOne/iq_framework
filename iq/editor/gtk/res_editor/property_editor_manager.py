#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Property editor manager class module.
"""

import sys
import hashlib
import datetime
import os.path

from ....util import log_func
from ....util import spc_func
from ....util import icon_func
from ....util import file_func
from ....util import lang_func

from ... import property_editor_id

from ....engine.gtk.dlg import gtk_dlg_func

from . import string_property_editor
from . import text_property_editor
from . import integer_property_editor
from . import float_property_editor
from . import choice_property_editor
from . import checkbox_property_editor
from . import multichoice_property_editor
from . import stringlist_property_editor
from . import script_property_editor
from . import readonly_property_editor
from . import password_property_editor

from . import size_property_editor
from . import point_property_editor
from . import dir_property_editor
from . import file_property_editor
from . import colour_property_editor
from . import font_property_editor
from . import image_property_editor
from . import icon_property_editor
from . import date_property_editor

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

VALIDATE_ENABLE = True

PROPERTY_EDITORS = (string_property_editor.iqStringPropertyEditor,
                    text_property_editor.iqTextPropertyEditor,
                    integer_property_editor.iqIntegerPropertyEditor,
                    float_property_editor.iqFloatPropertyEditor,
                    choice_property_editor.iqChoicePropertyEditor,
                    checkbox_property_editor.iqCheckBoxPropertyEditor,
                    multichoice_property_editor.iqMultiChoicePropertyEditor,
                    stringlist_property_editor.iqStringListPropertyEditor,
                    script_property_editor.iqScriptPropertyEditor,
                    readonly_property_editor.iqReadonlyPropertyEditor,

                    # color_property_editor.iqColorPropertyEditor,
                    # font_property_editor.iqFontPropertyEditor,
                    # point_property_editor.iqPointPropertyEditor,
                    # size_property_editor.iqSizePropertyEditor,
                    password_property_editor.iqPasswordPropertyEditor,
                    # file_property_editor.iqFilePropertyEditor,
                    # dir_property_editor.iqDirPropertyEditor,
                    # image_property_editor.iqImagePropertyEditor,
                    # date_property_editor.iqDatePropertyEditor,

                    # passport_property_editor.iqPassportPropertyEditor,
                    # libicon_property_editor.iqLibraryIconPropertyEditor,
                    # flag_property_editor.iqFlagPropertyEditor,
                    # single_choice_property_editor.iqSingleChoicePropertyEditor,
                    )


class iqPropertyEditorManager(object):
    """
    Property editor manager class.
    """
    def registerEditors(self, property_editor=None, *editor_classes):
        """
        Register custom editors.

        :param property_editor: Property grid manager.
        :param editor_classes: Custom editors classes.
        """
        if not editor_classes:
            editor_classes = PROPERTY_EDITORS
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
                    log_func.warning(u'Custom property editor not defined')
            # ensure we only do it once
            sys._PropGridEditorsRegistered = True

    def setSpecification(self, spc=None):
        """
        Set current component specification.

        :param spc: Component specification.
        """
        self._specification = spc

    def getSpecification(self):
        """
        Get current component specification.
        """
        if hasattr(self, '_specification'):
            return self._specification
        return None

    def setParentSpecification(self, spc=None):
        """
        Set parent component specification.

        :param spc: Component specification.
        """
        self._parent_specification = spc

    def getParentSpecification(self):
        """
        Get parent component specification.
        """
        if hasattr(self, '_parent_specification'):
            return self._parent_specification
        return None

    def createPropertyEditor(self, name, value, property_type=None, spc=None, parent_spc=None):
        """
        Create property editor.

        :param name: Attribute name.
        :param value: Attribute value.
        :param property_type: Property type.
        :param spc: Component specification.
        :param parent_spc: Parent component specification.
        :return: Property object.
        """
        obj_property = None

        if property_type is None and spc:
            property_type = self._getAttrEditorType(spc, name)

        if property_type == property_editor_id.STRING_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            obj_property = string_property_editor.iqStringPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.TEXT_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            obj_property = text_property_editor.iqTextPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.INTEGER_EDITOR:
            value = int(value) if value else 0
            obj_property = integer_property_editor.iqIntegerPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.FLOAT_EDITOR:
            value = float(value) if value else 0.0
            obj_property = float_property_editor.iqFloatPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.CHOICE_EDITOR:
            # log_func.debug(u'Attribute <%s>' % name)
            choices = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('choices', list())
            if isinstance(choices, (list, tuple)):
                choices = [str(item) for item in choices]
            elif callable(choices):
                choices = choices(resource=spc, parent_resource=parent_spc)
            else:
                log_func.warning(u'Property editor. Not support choices type <%s : %s>' % (name, type(choices)))
                choices = list()

            obj_property = choice_property_editor.iqChoicePropertyEditor(label=name, value=value, choices=choices)

        # elif property_type == property_editor_id.SINGLE_CHOICE_EDITOR:
        #     # log_func.debug(u'Attribute <%s>' % name)
        #     choices = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('choices', list())
        #     if isinstance(choices, (list, tuple)):
        #         choices = [str(item) for item in choices]
        #     elif callable(choices):
        #         choices = choices(resource=spc, parent_resource=parent_spc)
        #     else:
        #         log_func.warning(u'Property editor. Not support choices type <%s : %s>' % (name, type(choices)))
        #         choices = list()
        #
        #     if not isinstance(value, str):
        #         value = str(value)
        #     obj_property = single_choice_property.iqSingleChoiceProperty(label=name, name=name,
        #                                                                 choices=choices, value=value)

        elif property_type == property_editor_id.CHECKBOX_EDITOR:
            if isinstance(value, str):
                value = eval(value)
            value = bool(value)
            obj_property = checkbox_property_editor.iqCheckBoxPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.MULTICHOICE_EDITOR:
            choices = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('choices', dict())
            if isinstance(choices, dict):
                choices = list(choices.keys())
            elif callable(choices):
                choices = choices(resource=spc, parent_resource=parent_spc)
            else:
                log_func.warning(u'Property editor. Not support choices type <%s : %s>' % (name, type(choices)))
                choices = list()
            if value is None:
                value = list()
            values = [name for name in choices if name in value]
            obj_property = multichoice_property_editor.iqMultiChoicePropertyEditor(label=name, value=values, choices=choices)

        elif property_type == property_editor_id.STRINGLIST_EDITOR:
            value_list = []
            if isinstance(value, (list, tuple)):
                for item in value:
                    if not isinstance(item, str):
                        item = str(item)
                    value_list.append(item)
            obj_property = stringlist_property_editor.iqStringListPropertyEditor(label=name, value=value_list)

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
            obj_property = script_property_editor.iqPythonScriptPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.SQL_EDITOR:
            if value is None:
                value = u''
            elif isinstance(value, str):
                pass
            else:
                log_func.warning(u'Attribute [%s]. Property editor <SQL script> for type <%s> not supported' % (name, value.__class__.__name__))
                value = u''
            obj_property = script_property_editor.iqSqlPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.READONLY_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            obj_property = readonly_property_editor.iqReadonlyPropertyEditor(label=name, value=value)
            # obj_property.Enable(False)

        # elif property_type == property_editor_id.EXTERNAL_EDITOR:
        #     log_func.warning(u'Attribute [%s]. Property editor <External editor> not supported' % name)
        #
        # elif property_type == property_editor_id.CUSTOM_EDITOR:
        #     if not isinstance(value, str):
        #         value = str(value)
        #     obj_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == property_editor_id.COLOUR_EDITOR:
            value = value if value else 'black'
            log_func.debug(u'Colour %s' % str(value))
            obj_property = colour_property_editor.iqColourPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.FONT_EDITOR:
            value = value if value else dict()
            log_func.debug(u'Font %s' % str(value))
            obj_property = font_property_editor.iqFontPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.POINT_EDITOR:
            if isinstance(value, str):
                try:
                    value = eval(value)
                except:
                    log_func.fatal(u'Error point property editor value <%s>' % value)
                    value = (-1, -1)
            elif isinstance(value, (list, tuple)):
                pass
            else:
                log_func.warning(u'Error point property editor value type <%s>' % value.__class__.__name__)
                value = (-1, -1)
            obj_property = point_property_editor.iqPointPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.SIZE_EDITOR:
            if isinstance(value, str):
                try:
                    value = eval(value)
                except:
                    log_func.fatal(u'Error size property editor value <%s>' % value)
                    value = (-1, -1)
            elif isinstance(value, (list, tuple)):
                pass
            else:
                log_func.warning(u'Error size property editor value type <%s>' % value.__class__.__name__)
                value = (-1, -1)
            obj_property = size_property_editor.iqSizePropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.PASSWORD_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            obj_property = password_property_editor.iqPasswordPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.IMAGE_EDITOR:
            if not isinstance(value, str):
                value = None
            obj_property = image_property_editor.iqImagePropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.DATE_EDITOR:
            obj_property = date_property_editor.iqDatePropertyEditor(label=name, value=value)

        # elif property_type == property_editor_id.PASSPORT_EDITOR:
        #     if not isinstance(value, str):
        #         value = str(value)
        #     obj_property = wx.propgrid.StringProperty(name, value=value)

        elif property_type == property_editor_id.ICON_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            obj_property = icon_property_editor.iqIconPropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.FLAG_EDITOR:
            choice_dict = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, dict()).get('choices', dict())
            choices = list(choice_dict.keys())

            values = list()
            for choice_name, code in choice_dict.items():
                if code & value:
                    values.append(choice_name)
            obj_property = multichoice_property_editor.iqFlagPropertyEditor(label=name, value=values, choices=choices)

        elif property_type == property_editor_id.FILE_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            obj_property = file_property_editor.iqFilePropertyEditor(label=name, value=value)

        elif property_type == property_editor_id.DIR_EDITOR:
            if not isinstance(value, str):
                value = str(value)
            obj_property = dir_property_editor.iqDirPropertyEditor(label=name, value=value)

        else:
            log_func.warning(u'Property type <%s> not supported' % property_type)

        if obj_property:
            help_string = spc.get(spc_func.HELP_ATTR_NAME, dict()).get(name, name)
            obj_property.setHelpString(help_string)
        return obj_property

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

    def buildPropertyEditors(self, property_editor=None, resource=None, parent_resource=None):
        """
        Build all property editors.

        :param property_editor: Property grid manager.
        :param resource: Component resource.
        :param parent_resource: Parent component resource.
        :return: True/False.
        """
        if property_editor is None:
            log_func.warning(u'Not define property editor')
            return False

        if resource is None:
            log_func.warning(u'Not define component resource for edit')
            return False

        property_editor.clearProperties()

        # Set current component specification
        self.setSpecification(resource)

        # Set parent component specification
        self.setParentSpecification(parent_resource)

        # bmp = wx.ArtProvider.GetBitmap('gtk-index', wx.ART_MENU)
        # prop_page = property_editor.AddPage(_(u'Properties'), bmp)
        # ---------------------------------------
        #   1 - Basic attributes
        # prop_page.Append(wx.propgrid.PropertyCategory(u'1 - Basic'))

        attributes = spc_func.BASIC_ATTRIBUTES
        for attr_name in attributes:
            edt_type = self._getAttrEditorType(resource, attr_name)
            obj_property = self.createPropertyEditor(attr_name, resource.get(attr_name, None), edt_type,
                                                     spc=resource, parent_spc=parent_resource)
            if obj_property is not None:
                property_editor.getGtkObject('basic_property_box').add(obj_property.getGtkTopObject())

        # ----------------------------------------
        #   2 - Special attributes
        # prop_page.Append(wx.propgrid.PropertyCategory(u'2 - Special'))

        attributes = [attr_name for attr_name in self.getResourceAttributes(resource) if attr_name not in spc_func.BASIC_ATTRIBUTES]
        attributes.sort()
        # log_func.debug(u'Attributes: %s' % str(attributes))
        for attr_name in attributes:
            # log_func.debug(u'Attribute editor <%s> ...' % attr_name)
            edt_type = self._getAttrEditorType(resource, attr_name)
            obj_property = self.createPropertyEditor(attr_name, resource.get(attr_name, None), edt_type,
                                                     spc=resource, parent_spc=parent_resource)
            if obj_property is not None:
                # add_property = prop_page.Append(obj_property)
                property_editor.getGtkObject('special_property_box').add(obj_property.getGtkTopObject())

                # Advanced customization of property editors
                # if edt_type == property_editor_id.PASSWORD_EDITOR:
                #     # add_property.SetAttribute('Hint', 'This is a hint')
                #     add_property.SetAttribute('Password', True)
                # elif edt_type == property_editor_id.PASSPORT_EDITOR:
                #     property_editor.SetPropertyEditor(attr_name, passport_property_editor.iqPassportPropertyEditor.__name__)
                # elif edt_type == property_editor_id.ICON_EDITOR:
                #     property_editor.SetPropertyEditor(attr_name, libicon_property_editor.iqLibraryIconPropertyEditor.__name__)
                # elif edt_type == property_editor_id.FILE_EDITOR:
                #     property_editor.SetPropertyEditor(attr_name, file_property_editor.iqFilePropertyEditor.__name__)
                # elif edt_type == property_editor_id.DIR_EDITOR:
                #     property_editor.SetPropertyEditor(attr_name, dir_property_editor.iqDirPropertyEditor.__name__)
                # elif edt_type == property_editor_id.SCRIPT_EDITOR:
                #     property_editor.SetPropertyEditor(attr_name, script_property_editor.iqScriptPropertyEditor.__name__)

        # bmp = wx.ArtProvider.GetBitmap('gtk-execute', wx.ART_MENU)
        # methods_page = property_editor.AddPage(_(u'Methods'), bmp)

        # ----------------------------------------
        #   3 - Methods page
        methods = self.getResourceMethods(resource)
        for method_name in methods:
            edt_type = self._getAttrEditorType(resource, method_name)
            obj_property = self.createPropertyEditor(method_name, resource.get(method_name, None), edt_type,
                                                    spc=resource, parent_spc=parent_resource)
            if obj_property is not None:
                # methods_page.Append(obj_property)
                property_editor.getGtkObject('method_box').add(obj_property.getGtkTopObject())
                # property_editor.SetPropertyEditor(method_name, script_property_editor.iqScriptPropertyEditor.__name__)

        # bmp = wx.ArtProvider.GetBitmap('gtk-about', wx.ART_MENU)
        # events_page = property_editor.AddPage(_(u'Events'), bmp)

        # ----------------------------------------
        #   4 - Events page
        events = self.getResourceEvents(resource)
        for event_name in events:
            edt_type = self._getAttrEditorType(resource, event_name)
            obj_property = self.createPropertyEditor(event_name, resource.get(event_name, None), edt_type,
                                                     spc=resource, parent_spc=parent_resource)
            if obj_property is not None:
                # events_page.Append(obj_property)
                property_editor.getGtkObject('event_box').add(obj_property.getGtkTopObject())
                # property_editor.SetPropertyEditor(event_name, script_property_editor.iqScriptPropertyEditor.__name__)

        # Moves splitter as left as possible,
        # while still allowing all labels to be shown in full
        # property_editor.SetSplitterLeft()

    def getResourceAttributes(self, resource):
        """
        Get attribute names from resource.

        :param resource: Component resource dictionary.
        :return: Attribute name list.
        """
        edit_section = resource.get(spc_func.EDIT_ATTR_NAME, dict())
        # log_func.debug(u'Resource __edit__ section: %s' % str(edit_section))
        return [attr_name for attr_name, editor_type in list(edit_section.items()) if
                editor_type not in (property_editor_id.METHOD_EDITOR, property_editor_id.EVENT_EDITOR)]

    def getResourceMethods(self, resource):
        """
        Get method names from resource.

        :param resource: Component resource dictionary.
        :return: Method name list.
        """
        edit_section = resource.get(spc_func.EDIT_ATTR_NAME, dict())
        res_methods = [attr_name for attr_name, editor_type in list(edit_section.items()) if
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
        res_events = [attr_name for attr_name, editor_type in list(edit_section.items()) if
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

        elif property_type == property_editor_id.SINGLE_CHOICE_EDITOR:
            value = str_value

        elif property_type == property_editor_id.CHECKBOX_EDITOR:
            try:
                value = eval(str_value)
            except:
                log_func.fatal(u'Error casting to a boolean <%s>' % str_value)
                value = False

        elif property_type == property_editor_id.MULTICHOICE_EDITOR:
            try:
                # log_func.debug(u'Multichoice property. Value <%s>' % str_value)
                value = str_value
            except:
                log_func.fatal(u'Error casting to a multichoice string list <%s>' % str_value)

        elif property_type == property_editor_id.STRINGLIST_EDITOR:
            try:
                value = tuple([eval(item) if item.isdigit() else item for item in str_value.split(', ')])
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
                # colour = wx.Colour(colour_name)
                # value = (colour.Red(), colour.Green(), colour.Blue())
                value = colour_name

        elif property_type == property_editor_id.FONT_EDITOR:
            log_func.debug(u'Get font %s' % str_value)
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

        elif property_type == property_editor_id.IMAGE_EDITOR:
            value = str_value if str_value else None

        elif property_type == property_editor_id.SCRIPT_EDITOR:
            value = str_value if str_value else None

        elif property_type == property_editor_id.METHOD_EDITOR:
            value = str_value if str_value else None

        elif property_type == property_editor_id.EVENT_EDITOR:
            value = str_value if str_value else None

        elif property_type == property_editor_id.PASSPORT_EDITOR:
            value = str_value if str_value and str_value != str(None) else None

        elif property_type == property_editor_id.ICON_EDITOR:
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

        elif property_type == property_editor_id.FILE_EDITOR:
            framework_path = file_func.getFrameworkPath()
            if framework_path in str_value:
                value = str_value.replace(framework_path, '')
                if value.startswith(os.path.sep):
                    value = value[1:]
            else:
                value = str_value

        elif property_type == property_editor_id.DIR_EDITOR:
            framework_path = file_func.getFrameworkPath()
            if framework_path in str_value:
                value = str_value.replace(framework_path, '')
                if value.startswith(os.path.sep):
                    value = value[1:]
            else:
                value = str_value

        else:
            log_func.warning(u'Not support property editor. Code [%d]' % property_type)

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
            log_func.warning(u'Not define component specification')
            return None

        property_type = self.findPropertyType(name, spc)
        if property_type is None:
            # По умолчанию все не определенные атрибуты - скриптовые
            property_type = property_editor_id.SCRIPT_EDITOR
        value = self.getConvertedValue(name, str_value, property_type, spc)
        log_func.debug(u'Convert property value <%s : %s : %s : %s>' % (name, str_value, property_type, value))
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

    def validatePropertyValue(self, name, value, spc=None):
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

        if spc is None:
            spc = self.getSpecification()
        if spc is None:
            log_func.warning(u'Property editor. Current component specification not defined')
            return True

        # Valid attribute type
        editor = self.findPropertyEditor(name, spc)

        if editor is None:
            msg = _(u'Not define attribute editor') + ' <%s>' % name
            log_func.warning(msg)
            gtk_dlg_func.openErrBox(_(u'VALIDATION'), msg)
            valid = False
        elif isinstance(editor, int):
            # No need to valid
            pass
        elif isinstance(editor, dict):
            if 'valid' in editor and callable(editor['valid']):
                try:
                    valid = editor['valid'](value)
                except:
                    msg = _('Error valid property/attribute') + ' <%s : %s>' % (name, value)
                    log_func.fatal(msg)
                    gtk_dlg_func.openFatalBox(_(u'VALIDATION'), msg)
                    valid = False
        else:
            log_func.warning(u'Not support property/attribute editor type <%s>' % type(editor))
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
                log_func.warning(u'Not supported property editor type <%s : %s> in <%s> specification' % (name,
                                                                                                          type(attr_editor),
                                                                                                          spc.get('type', None)))

        # Find in parent specification
        if property_type is None and spc_func.PARENT_ATTR_NAME in spc:
            property_type = self.findPropertyType(name, spc[spc_func.PARENT_ATTR_NAME])
        return property_type

    def getPropertyValueAsString(self, property, name, spc=None):
        """
        Get property value as string.

        :param property: Property object.
        :param name: Attribute name.
        :param spc: Component specification.
        :return: Property value as string.
        """
        if spc is None:
            spc = self.getSpecification()

        editor = spc.get(spc_func.EDIT_ATTR_NAME, dict()).get(name, None)
        if editor == property_editor_id.PASSWORD_EDITOR:
            str_value = str(property.GetValue())
        else:
            str_value = property.GetValueAsString()
        # log_func.info(u'Property [%s]. New value <%s>' % (name, str_value))
        return str_value

    def setPropertyValueAsString(self, property, name, value, spc=None):
        """
        Set property value as string.

        :param property: Property object.
        :param name: Attribute name.
        :param value: Attribute value.
        :param spc: Component specification.
        :return: True/False.
        """
        property.SetValueFromString(str(value))
        return True

    def setPropertyValue(self, property, name, value, spc=None):
        """
        Set property value.

        :param property: Property object.
        :param name: Attribute name.
        :param value: Attribute value.
        :param spc: Component specification.
        :return: True/False.
        """
        property.SetValue(value)
        return True
