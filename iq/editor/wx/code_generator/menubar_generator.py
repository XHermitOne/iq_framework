#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python menubar generate functions.
"""

import os
import os.path
import inspect

from ....util import log_func
from ....util import py_func
from ....util import str_func
from ....util import txtfile_func

__version__ = (0, 0, 1, 2)


CREATE_MENUBAR_FUNC_BODY_FMT = u'''
def create%s():
    \"\"\"
    Create menubar.

    :return: MenuBar object or None if error.
    \"\"\"
    try:
        menubar = %s()
        menubar.init()
        return menubar
    except:
        log_func.fatal(u'Error create menubar <%s>')
    return None
'''


GEN_PY_MODULE_FMT = u'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
MenuBar module <%s>. 
Generated by the iqFramework module the wxFormBuider prototype menubar.
\"\"\"

import wx
from . import %s

import iq
from iq.util import log_func
from iq.util import global_func

from iq.engine.wx import menubar_manager

__version__ = (0, 0, 0, 1)


class %s(%s.%s, menubar_manager.iqMenuBarManager):
    \"\"\"
    MenuBar.
    \"\"\"
    def __init__(self, *args, **kwargs):
        \"\"\"
        Constructor.
        \"\"\"
        %s.%s.__init__(self, *args, **kwargs)

    def init(self):
        \"\"\"
        Init menubar.
        \"\"\"
        self.initImages()

        # Enable/Disable menuitems control block
        # user = global_func.getUser()
        is_admin = global_func.isAdministratorUser()

        menuitem_enable = {
            # self.about_menuItem.GetId(): is_admin,

        }
        self.enableMenuBarMenuItems(menubar=self, menuitem_enable=menuitem_enable)

    def initImages(self):
        \"\"\"
        Init images method.
        \"\"\"
        pass

%s
%s
'''

WXFB_PRJ_MENUBAR_FMT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<wxFormBuilder_Project>
    <FileVersion major="1" minor="15" />
    <object class="Project" expanded="1">
        <property name="class_decoration">; </property>
        <property name="code_generation">Python</property>
        <property name="disconnect_events">1</property>
        <property name="disconnect_mode">source_name</property>
        <property name="disconnect_php_events">0</property>
        <property name="disconnect_python_events">0</property>
        <property name="embedded_files_path">res</property>
        <property name="encoding">UTF-8</property>
        <property name="event_generation">connect</property>
        <property name="file">%s</property>
        <property name="first_id">1000</property>
        <property name="help_provider">none</property>
        <property name="indent_with_spaces"></property>
        <property name="internationalize">1</property>
        <property name="name">%s</property>
        <property name="namespace"></property>
        <property name="path">.</property>
        <property name="precompiled_header"></property>
        <property name="relative_path">1</property>
        <property name="skip_lua_events">1</property>
        <property name="skip_php_events">1</property>
        <property name="skip_python_events">1</property>
        <property name="ui_table">UI</property>
        <property name="use_enum">0</property>
        <property name="use_microsoft_bom">0</property>
        <object class="MenuBar" expanded="1">
            <property name="bg"></property>
            <property name="context_help"></property>
            <property name="context_menu">1</property>
            <property name="enabled">1</property>
            <property name="fg"></property>
            <property name="font"></property>
            <property name="hidden">0</property>
            <property name="id">wxID_ANY</property>
            <property name="label">%s</property>
            <property name="maximum_size"></property>
            <property name="minimum_size"></property>
            <property name="name">%s</property>
            <property name="pos"></property>
            <property name="size"></property>
            <property name="style"></property>
            <property name="subclass">; ; forward_declare</property>
            <property name="tooltip"></property>
            <property name="window_extra_style"></property>
            <property name="window_name"></property>
            <property name="window_style"></property>
            <object class="wxMenu" expanded="1">
                <property name="label">Help</property>
                <property name="name">help_menu</property>
                <property name="permission">protected</property>
                <object class="wxMenuItem" expanded="1">
                    <property name="bitmap"></property>
                    <property name="checked">0</property>
                    <property name="enabled">1</property>
                    <property name="help"></property>
                    <property name="id">wxID_ANY</property>
                    <property name="kind">wxITEM_NORMAL</property>
                    <property name="label">About...</property>
                    <property name="name">about_menuItem</property>
                    <property name="permission">none</property>
                    <property name="shortcut"></property>
                    <property name="unchecked_bitmap"></property>
                </object>
            </object>
        </object>
    </object>
</wxFormBuilder_Project>
'''


def genMenuBarClassName(src_class_name):
    """
    Generate menubar class name.

    :param src_class_name: Source menubar prototype class name.
    :return: New menubar class name.
    """
    dst_class_name = src_class_name
    dst_class_name = dst_class_name[:-9] if dst_class_name.endswith('Prototype') else dst_class_name
    dst_class_name = dst_class_name[:-5] if dst_class_name.endswith('Proto') else dst_class_name
    return dst_class_name


def genCreateFunctionBody(class_name):
    """
    Generate create function text body.

    :param class_name: MenuBar class name.
    :return: Function text body.
    """
    function_name = class_name[2:] if class_name.startswith('iq') else class_name
    frm_body_function = CREATE_MENUBAR_FUNC_BODY_FMT % (function_name, class_name, class_name)
    return frm_body_function


def genPythonMenuBar(src_module, src_class_name):
    """
    Generation of the menubar class text.

    :param src_module: Source module object.
    :param src_class_name: Source class name.
    :return: True/False.
    """
    log_func.info(u'Generate menubar class ... START')

    dst_class_name = genMenuBarClassName(src_class_name)
    src_class = getattr(src_module, src_class_name)

    # Handlers
    src_class_methods = [getattr(src_class, var_name) for var_name in dir(src_class)]
    src_class_events = [method for method in src_class_methods if inspect.isfunction(method) and
                        method.__name__ != '__init__' and
                        'event' in method.__code__.co_varnames and
                        method.__code__.co_argcount == 2]

    # A way to get the source code from a function object+
    #                                                    v
    body_functions = u'\n'.join(
        [u'\n'.join(inspect.getsourcelines(class_method)[0]) for class_method in src_class_events])
    body_functions = body_functions.replace(u'\t', u'    ').replace(u'( ', u'(').replace(u' )', u')')
    log_func.info(u'Append method in class <%s>:' % dst_class_name)
    log_func.debug(body_functions)

    create_body_function = genCreateFunctionBody(dst_class_name)

    py_txt = GEN_PY_MODULE_FMT % (src_class_name,
                                  src_module.__name__,
                                  dst_class_name, src_module.__name__, src_class_name,
                                  src_module.__name__, src_class_name,
                                  body_functions,
                                  create_body_function)
    log_func.info(u'Generate menubar class ... STOP')
    return py_txt


def genDefaultMenubarFormBuilderPrj(prj_filename=None, rewrite=False):
    """
    Generate default menubar wxFormBuilder project file.

    :param prj_filename: wxFormBuilder project filename.
    :param rewrite: Rewrite it if exists?
    :return: True/False.
    """
    if not prj_filename:
        log_func.warning(u'Not define wxFormBuilder project filename')
        return False

    package_dirname = os.path.dirname(prj_filename)
    py_func.createInitModule(package_path=package_dirname, rewrite=rewrite)

    menubar_name = os.path.splitext(os.path.basename(prj_filename))[0].lower()
    menubar_class_name = 'iq%s' % str_func.replaceLower2Upper(menubar_name)
    wxfb_menubar_txt = WXFB_PRJ_MENUBAR_FMT % (menubar_name,
                                               menubar_name,
                                               menubar_name,
                                               menubar_class_name)
    save_ok = txtfile_func.saveTextFile(txt_filename=prj_filename,
                                        txt=wxfb_menubar_txt,
                                        rewrite=rewrite)
    if save_ok:
        from .. import wxfb_manager
        wxformbuilder_manager = wxfb_manager.iqWXFormBuilderManager()
        return wxformbuilder_manager.generate(prj_filename=prj_filename, asynchro=False)

    return False
