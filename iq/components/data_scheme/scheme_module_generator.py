#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scheme python module generator.
"""

import os
import os.path

from ...util import log_func
from ...util import txtfile_func
from ...util import spc_func
from ...util import file_func
from ...dialog import dlg_func

__version__ = (0, 0, 0, 1)

SCHEME_TEXT_FMT = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
%s.
"""

# Scheme module python code generated with iqFramework

import sqlalchemy
import sqlalchemy.ext.declarative
# import sqlalchemy.orm
# import sqlalchemy.orm.exc

Base = sqlalchemy.ext.declarative.declarative_base()

%s'''

MODEL_TEXT_FMT = '''
class %s(Base):
    """
    %s.
    """
    __tablename__ = '%s'

%s
'''

COLUMN_TEXT_FMT = '    %s = sqlalchemy.Column(%s)'


class iqSchemeModuleGenerator(object):
    """
    Scheme python module generator.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._resource = dict()

    def getResource(self):
        """
        Get scheme resource.
        """
        return self._resource

    def setResource(self, resource):
        """
        Set resource.

        :param resource: Resource dictionary.
        """
        self._resource = resource

    def getName(self):
        """
        Get scheme name.
        """
        return self._resource.get('name', 'unknown')

    def genModuleFilename(self):
        """
        Generate scheme module filename.

        :return: Module filename.
        """
        name = self.getName()
        path = file_func.getProjectPath() if file_func.getProjectPath() else file_func.getFrameworkPath()
        return os.path.join(path, name + '.py')

    def existsModule(self, module_filename=None):
        """
        Exists scheme module?

        :param module_filename: Module filename.
            If None then generate module filename.
        :return: New module filename or None if error.
        """
        if module_filename is None:
            module_filename = self.genModuleFilename()
        return os.path.exists(module_filename)

    def genModule(self, module_filename=None):
        """
        Generate scheme module.

        :param module_filename: Module filename.
            If None then generate module filename.
        :return: New module filename or None if error.
        """
        log_func.info(u'Generate data scheme module <%s>' % module_filename)
        if module_filename is None:
            module_filename = self.genModuleFilename()

        try:
            resource = self.getResource()
            description = resource.get('description', '')

            modeles_text = [self.genModelTxt(model) for model in resource.get(spc_func.CHILDREN_ATTR_NAME, list())]
            scheme_text = SCHEME_TEXT_FMT % (description, u'\n'.join(modeles_text))

            result = txtfile_func.saveTextFile(txt_filename=module_filename,
                                               txt=scheme_text, rewrite=True)
            return module_filename if result else None
        except:
            log_func.fatal(u'Error generate scheme module')
        return None

    def genModelTxt(self, resource):
        """
        Generate model text.

        :param resource: Model resource.
        :return: Model text.
        """
        name = resource.get('name', 'Unknown')
        description = resource.get('name', '')
        tablename = resource.get('tablename', '')
        tablename = tablename if tablename else name.lower()
        columns_text = [self.genColumnTxt(column) for column in resource.get(spc_func.CHILDREN_ATTR_NAME, list())]
        return MODEL_TEXT_FMT % (name, description, tablename, os.linesep.join(columns_text))

    def genColumnTxt(self, resource):
        """
        Generate column text.

        :param resource: Column resource.
        :return: Column text.
        """
        name = resource.get('name', 'Unknown')
        description = resource.get('name', '')
        column_attrs = list()

        field_type = resource.get('field_type', None)
        field_attr = resource.get('field_attr', None)
        field_attr_txt = ''
        if field_attr is not None:
            field_attr_txt = '(%s)' % ', '.join(['%s = %s' % (attr_name, attr_value) for attr_name, attr_value in field_attr])
        type_txt = 'sqlalchemy.%s%s' % (field_type, field_attr_txt)
        column_attrs.append(type_txt)

        autoincrement = resource.get('autoincrement', None)
        if autoincrement not in (True, None):
            column_attrs.append('autoincrement=%s' % str(autoincrement))

        default = resource.get('default', None)
        if default is not None:
            column_attrs.append('default=%s' % str(default))

        key = resource.get('key', None)
        if key is not None:
            column_attrs.append('key=%s' % str(key))

        index = resource.get('index', None)
        if index not in (None, False):
            column_attrs.append('index=%s' % str(index))

        info = resource.get('info', None)
        if info is not None:
            column_attrs.append('info=%s' % str(info))

        nullable = resource.get('nullable', None)
        if nullable not in (True, None):
            column_attrs.append('nullable=%s' % str(nullable))

        onupdate = resource.get('onupdate', None)
        if onupdate is not None:
            column_attrs.append('onupdate=%s' % str(onupdate))

        primary_key = resource.get('primary_key', None)
        if primary_key not in (False, None):
            column_attrs.append('primary_key=%s' % str(primary_key))

        server_default = resource.get('server_default', None)
        if server_default:
            column_attrs.append('server_default=%s' % str(server_default))

        server_onupdate = resource.get('server_onupdate', None)
        if server_onupdate is not None:
            column_attrs.append('server_onupdate=%s' % str(server_onupdate))

        quote = resource.get('quote', None)
        if quote not in (False, None):
            column_attrs.append('quote=%s' % str(quote))

        unique = resource.get('unique', None)
        if unique not in (False, None):
            column_attrs.append('unique=%s' % str(unique))

        system = resource.get('system', None)
        if system not in (False, None):
            column_attrs.append('system=%s' % str(system))

        if description:
            column_attrs.append('doc=\'%s\'' % description)

        return COLUMN_TEXT_FMT % (name, ', '.join(column_attrs))


def genModule(module_filename=None, resource=None):
    """
    Generate module file.

    :param module_filename: Module filename.
    :param resource: Resource dictionary.
    :return: True/False.
    """
    generator = iqSchemeModuleGenerator()
    generator.setResource(resource)
    return generator.genModule(module_filename=module_filename)