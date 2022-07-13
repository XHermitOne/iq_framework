#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python gui class generate functions.
"""

import os
import os.path
import inspect

from ....util import log_func
from ....util import str_func
from ....util import xml2dict
from ....util import txtfile_func
from ....dialog import dlg_func

__version__ = (0, 0, 1, 2)

DEFAULT_SRC_CLASS_NAME = u'iqUnknown'

EMPTY_PY_MODULE_FMT = u'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
Module <%s>. 
Generated by the iqFramework module the Glade prototype.
\"\"\"

import os
import os.path
import signal
import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from iq.util import log_func

from iq.engine.gtk import gtk_handler
# from iq.engine.gtk import gtktreeview_manager
# from iq.engine.gtk import gtkwindow_manager

__version__ = (0, 0, 0, 1)


class iq%s(gtk_handler.iqGtkHandler):
    """
    Unknown class.
    """
    def __init__(self, *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), '%s')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='%s',  
                                          *args, **kwargs)
                                          
    def init(self):
        """
        Init form.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images of controls on form.
        """
        pass

    def initControls(self):
        """
        Init controls method.
        """
        pass

%s

def open%s():
    """
    Open %s.

    :return: True/False.
    """
    result = False
    obj = None
    try:
        obj = iq%s()
        obj.init()
        obj.getGtkTopObject().run()
        result = True
    except:
        log_func.fatal(u'Error open window <%s>')

    if obj and obj.getGtkTopObject() is not None:
        obj.getGtkTopObject().destroy()
    return result                    
'''

HANDLER_PY_MODULE_FMT = '''    def %s(self, widget):
        """
        """
        pass
'''

DEFAULT_HANDLER_NAME = u'onUnknown'

GTK_TOP_WIDGET_TYPES = ('GtkWindow',
                        'GtkOffscreenWindow',
                        'GtkApplicationWindow',
                        'GtkDialog',
                        # 'GtkAboutDialog',
                        # 'GtkFileChooserDialog',
                        # 'GtkColorChooserDialog',
                        # 'GtkFontChooserDialog',
                        # 'GtkMessageDialog',
                        # 'GtkRecentChooserDialog',
                        # 'GtkAssistent',
                        # 'GtkAppChooserDialog',

                        'GtkBox',
                        'GtkGrid',
                        'GtkFlowBox',
                        'GtkListBox')

GLADE_CSS_SIGNATURE = '<!-- interface-css-provider-path '

EMPTY_MAINFORM_PY_MODULE_FMT = u'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
Module <%s>. 
Generated by the iqFramework module the Glade prototype.
\"\"\"

import os
import os.path
import signal
import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from iq.util import log_func

from iq.engine.gtk import gtk_handler
# from iq.engine.gtk import gtktreeview_manager
# from iq.engine.gtk import gtkwindow_manager

__version__ = (0, 0, 0, 1)


class iq%s(gtk_handler.iqGtkHandler):
    """
    Unknown class.
    """
    def __init__(self, *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), '%s')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='%s',  
                                          *args, **kwargs)

    def init(self):
        """
        Init form.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images of controls on form.
        """
        pass

    def initControls(self):
        """
        Init controls method.
        """
        pass

%s

def open%s():
    """
    Open %s.

    :return: True/False.
    """
    result = False
    obj = None
    try:
        obj = iq%s()
        obj.init()
        obj.getGtkTopObject().run()
        result = True
    except:
        log_func.fatal(u'Error open window <%s>')

    if obj and obj.getGtkTopObject() is not None:
        obj.getGtkTopObject().destroy()
    return result                    
'''


def getGladeProjectCSSFilename(filename, do_realpath=True):
    """
    Get the CSS filename in glade project file.

    :param filename: Glade project filename.
    :param do_realpath: Return real path to css file?
    :return: CSS filename or None if not found.
    """
    search_lines = txtfile_func.searchLinesInTextFile(filename, GLADE_CSS_SIGNATURE)
    if search_lines:
        search_line = search_lines[0].strip()
        search_line_list = [item for item in search_line.split(' ') if '.css' in item or '.CSS' in item]
        css_filename = search_line_list[0] if search_line_list else None
        if do_realpath:
            if not os.path.exists(css_filename):
                # CSS file is relative path
                css_filename = os.path.join(os.path.dirname(filename), css_filename)
        return css_filename
    return None


def hasGladeProjectCSSFilename(filename):
    """
    Has glade project file the CSS filename.

    :param filename: Glade project filename.
    :return: True/False.
    """
    css_filename = getGladeProjectCSSFilename(filename, do_realpath=False)
    return css_filename is not None


def genPyModuleName(src_name):
    """
    Generate the file name from the form class name.

    :param src_name: Source object Id/name.
    :return:
    """
    dst_module_name = src_name
    dst_module_name = dst_module_name[2:] if dst_module_name.startswith('iq') else dst_module_name
    dst_module_name = dst_module_name[:-9] if dst_module_name.endswith('Prototype') else dst_module_name
    dst_module_name = dst_module_name[:-5] if dst_module_name.endswith('Proto') else dst_module_name
    dst_module_name = dst_module_name[:-10] if dst_module_name.endswith('_prototype') else dst_module_name
    dst_module_name = dst_module_name[:-6] if dst_module_name.endswith('_proto') else dst_module_name
    dst_module_name = str_func.replaceUpper2Lower(dst_module_name)
    return dst_module_name


def _getSignalHandler(signal_xml_content, sender_name='', sender_type=''):
    """
    Get signal handler.

    :param signal_xml_content: Glade signal content.
    :param sender_name: Sender object name.
    :param sender_type: Sender class name.
    """
    if isinstance(signal_xml_content, (list, tuple)):
        for i, signal in enumerate(signal_xml_content):
            signal_xml_content[i]['sender_name'] = sender_name
            signal_xml_content[i]['sender_type'] = sender_type
        return signal_xml_content
    elif isinstance(signal_xml_content, dict):
        signal_xml_content['sender_name'] = sender_name
        signal_xml_content['sender_type'] = sender_type
        return [signal_xml_content]
    else:
        log_func.warning(u'Not parsed XML content object <%s>' % signal_xml_content)
    return list()


def _getSignalHandlers(object_xml_content):
    """
    Get signal handler list.

    :param object_xml_content: Glade object tree.
    """
    signal_handlers = list()
    if isinstance(object_xml_content, (list, tuple)):
        for child in object_xml_content:
            signal_handler = _getSignalHandlers(child)
            signal_handlers += signal_handler
    elif isinstance(object_xml_content, dict):
        if 'signal' in object_xml_content:
            signal_handler = _getSignalHandler(object_xml_content['signal'],
                                               sender_name=object_xml_content.get('@id', ''),
                                               sender_type=object_xml_content.get('@class', ''))
            signal_handlers += signal_handler
        if 'child' in object_xml_content:
            children = [object_xml_content['child']] if isinstance(object_xml_content['child'], dict) else object_xml_content['child']
            for child in children:
                signal_handler = _getSignalHandlers(child['object'] if 'object' in child else child)
                signal_handlers += signal_handler
    else:
        log_func.warning(u'Not parsed XML content object <%s>' % object_xml_content)
    return signal_handlers


def gen(src_filename=None, dst_filename=None, src_name=None, parent=None, rewrite=False):
    """
    Generation of GUI frame python module by Glade project.

    :param src_filename: Glade project filename.
    :param dst_filename: Result python frame module filename.
    :param src_name: Source object Id/name.
    :param parent: Parent form.
    :param rewrite: Rewrite result file if exists?
    :return: New python filename or None if error.
    """
    log_func.info(u'Generate python GUI module ... START')
    if not os.path.exists(src_filename):
        log_func.warning(u'Generation Python file. File <%s> not found' % src_filename)
        return None

    try:
        # src_module_name = os.path.splitext(os.path.basename(src_filename))[0]
        src_module_path = os.path.dirname(src_filename)

        # Get Glade xml project file as dictionary
        glade_xml_content = xml2dict.convertXmlFile2Dict(src_filename)
        glade_top_widgets = []
        if isinstance(glade_xml_content['interface']['object'], (list, tuple)):
            glade_top_widgets = [dict(id=obj['@id'], classname=obj['@class']) for obj in glade_xml_content['interface']['object'] if obj.get('@class', None) in GTK_TOP_WIDGET_TYPES]
        elif isinstance(glade_xml_content['interface']['object'], dict):
            obj = glade_xml_content['interface']['object']
            if obj.get('@class', None) in GTK_TOP_WIDGET_TYPES:
                # Gen top window widgets
                glade_top_widgets.append(dict(id=obj['@id'], classname=obj['@class']))
        else:
            log_func.warning(u'Not parsed XML content objects')

        signal_handlers = _getSignalHandlers(glade_xml_content['interface']['object'])
        signal_handlers_txt = os.linesep.join([HANDLER_PY_MODULE_FMT % signal.get('@handler', DEFAULT_HANDLER_NAME) for signal in signal_handlers])

        if src_name is None:
            if len(glade_top_widgets) == 1:
                # Only one class per module
                src_name = glade_top_widgets[0]['id']
                # src_type = glade_top_widgets[0]['classname'].lstrip('Gtk')
            elif len(glade_top_widgets) > 1:
                choices = [frm_name for frm_name, frm_type in glade_top_widgets]
                choices.sort()
                src_name = dlg_func.getSingleChoiceDlg(parent=parent,
                                                       title=u'GENERATOR',
                                                       prompt_text=u'Select prototype object:',
                                                       choices=choices)
                if not src_name:
                    # Cancel pressed
                    return
                # src_type = glade_top_widgets[choices.index(src_name)]['classname']
            else:
                log_func.warning(u'GUI module generator. Empty top object list')

        if dst_filename is None:
            # If the output file name is not defined, then generate the file name from the form class name
            dst_module_name = genPyModuleName(src_name)
            dst_filename = os.path.join(src_module_path, '%s.py' % dst_module_name)

        if os.path.exists(dst_filename) and rewrite:
            # Delete result file if exists
            os.remove(dst_filename)
            log_func.info(u'Python file <%s> is deleted' % dst_filename)

        if not os.path.exists(dst_filename):
            src_class_name = str_func.replaceLower2Upper(src_name)
            src_class_name = src_class_name[2:] if src_class_name.lower().startswith('iq') else src_class_name

            py_txt = EMPTY_PY_MODULE_FMT % (os.path.basename(dst_filename),
                                            src_class_name,
                                            os.path.basename(src_filename),
                                            src_name,
                                            signal_handlers_txt,
                                            src_class_name,
                                            src_name, src_class_name, src_name)
            log_func.info(u'Save file <%s>' % dst_filename)

            result = txtfile_func.saveTextFile(dst_filename, txt=py_txt)
            if result:
                return dst_filename
            else:
                log_func.warning(u'Error save file <%s>' % dst_filename)
        else:
            msg = u'Python file <%s> exists. Generation not possible' % dst_filename
            log_func.warning(msg)
            dlg_func.openErrBox(u'GENERATOR', msg)
    except:
        log_func.fatal(u'Error generation of gui python module by Glade project')

    log_func.info(u'Generate python GUI module ... STOP')
    return None


def genMainForm(src_filename=None, dst_filename=None, src_class_name=None, parent=None, rewrite=False):
    """
    Generation of the main form module by Glade project.

    :param src_filename: Glade project filename.
    :param dst_filename: Result python main form module filename.
    :param src_class_name: Source class name.
    :param parent: Parent form.
    :param rewrite: Rewrite result file if exists?
    :return: New python filename or None if error.
    """
    log_func.info(u'Generate python GUI module ... START')
    if not os.path.exists(src_filename):
        log_func.warning(u'Glade project file. File <%s> not found' % src_filename)
        return None

    try:
        src_name = None
        # src_module_name = os.path.splitext(os.path.basename(src_filename))[0]
        src_module_path = os.path.dirname(src_filename)

        # Get Glade xml project file as dictionary
        glade_xml_content = xml2dict.convertXmlFile2Dict(src_filename)
        glade_top_widgets = []
        if isinstance(glade_xml_content['interface']['object'], (list, tuple)):
            glade_top_widgets = [dict(id=obj['@id'], classname=obj['@class']) for obj in glade_xml_content['interface']['object'] if obj.get('@class', None) in GTK_TOP_WIDGET_TYPES]
        elif isinstance(glade_xml_content['interface']['object'], dict):
            obj = glade_xml_content['interface']['object']
            if obj.get('@class', None) in GTK_TOP_WIDGET_TYPES:
                # Gen top window widgets
                glade_top_widgets.append(dict(id=obj['@id'], classname=obj['@class']))
        else:
            log_func.warning(u'Not parsed XML content objects')

        signal_handlers = _getSignalHandlers(glade_xml_content['interface']['object'])
        signal_handlers_txt = os.linesep.join([HANDLER_PY_MODULE_FMT % signal.get('@handler', DEFAULT_HANDLER_NAME) for signal in signal_handlers])

        if len(glade_top_widgets) == 1:
            # Only one class per module
            src_name = glade_top_widgets[0]['id']
            # src_type = glade_top_widgets[0]['classname'].lstrip('Gtk')
        elif len(glade_top_widgets) > 1:
            choices = [frm_name for frm_name, frm_type in glade_top_widgets]
            choices.sort()
            src_name = dlg_func.getSingleChoiceDlg(parent=parent,
                                                   title=u'GENERATOR',
                                                   prompt_text=u'Select prototype object:',
                                                   choices=choices)
            if not src_name:
                # Cancel pressed
                return None
        else:
            log_func.warning(u'GUI module generator. Empty top object list')

        if dst_filename is None:
            # If the output file name is not defined, then generate the file name from the form class name
            dst_module_name = genPyModuleName(src_name)
            dst_filename = os.path.join(src_module_path, '%s.py' % dst_module_name)

        if os.path.exists(dst_filename) and rewrite:
            # Delete result file if exists
            os.remove(dst_filename)
            log_func.info(u'Python file <%s> is deleted' % dst_filename)

        if not os.path.exists(dst_filename):
            src_class_name = str_func.replaceLower2Upper(src_name)
            src_class_name = src_class_name[2:] if src_class_name.lower().startswith('iq') else src_class_name

            py_txt = EMPTY_MAINFORM_PY_MODULE_FMT % (os.path.basename(dst_filename),
                                                     src_class_name,
                                                     os.path.basename(src_filename),
                                                     src_name,
                                                     signal_handlers_txt,
                                                     src_class_name,
                                                     src_name, src_class_name, src_name)
            log_func.info(u'Save file <%s>' % dst_filename)

            result = txtfile_func.saveTextFile(dst_filename, txt=py_txt)
            if result:
                return dst_filename
            else:
                log_func.warning(u'Error save file <%s>' % dst_filename)
        else:
            msg = u'Python file <%s> exists. Generation not possible' % dst_filename
            log_func.warning(msg)
            dlg_func.openErrBox(u'GENERATOR', msg)
    except:
        log_func.fatal(u'Error generation of gui python module by Glade project')

    log_func.info(u'Generate python GUI module ... STOP')
    return None
