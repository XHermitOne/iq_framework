#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python frame generate functions.
"""

import inspect

from ....util import log_func

__version__ = (0, 0, 0, 1)


SHOW_FRAME_FUNC_BODY_FMT = u'''
def show%s(parent=None):
    \"\"\"
    Open frame.
    
    :param parent: Parent window.
    :return: True/False.
    \"\"\"
    try:
        if parent is None:
            parent = global_func.getMainWin()

        frame = %s(parent)
        frame.init()
        result = frame.Show()
        return True
    except:
        log_func.fatal(u'Error show frame <%s>')
    return False
'''

GEN_PY_MODULE_FMT = u'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
Frame module <%s>. 
Generated by the iqFramework modulo the wxFormBuider prototype form.
\"\"\"

import wx
from . import %s

import iq
from iq.util import log_func
from iq.util import global_func

from iq.engine.wx import form_manager

__version__ = (0, 0, 0, 1)


class %s(%s.%s, form_manager.iqFormManager):
    \"\"\"
    Frame.
    \"\"\"
    def __init__(self, *args, **kwargs):
        \"\"\"
        Constructor.
        \"\"\"
        %s.%s.__init__(self, *args, **kwargs)

    def init(self):
        \"\"\"
        Init frame.
        \"\"\"
        self.initImages()
        self.initControls()

    def initImages(self):
        \"\"\"
        Init images method.
        \"\"\"
        pass

    def initControls(self):
        \"\"\"
        Init controls method.
        \"\"\"
        pass

%s
%s
'''


def genFrameClassName(src_class_name):
    """
    Generate frame class name.

    :param src_class_name: Source frame prototype class name.
    :return: New frame class name.
    """
    dst_class_name = src_class_name
    dst_class_name = dst_class_name[:-9] if dst_class_name.endswith('Prototype') else dst_class_name
    dst_class_name = dst_class_name[:-5] if dst_class_name.endswith('Proto') else dst_class_name
    return dst_class_name


def genShowFunctionBody(class_name):
    """
    Generate show function text body.

    :param class_name: Frame class name.
    :return: Function text body.
    """
    function_name = class_name[2:] if class_name.startswith('iq') else class_name
    frm_body_function = SHOW_FRAME_FUNC_BODY_FMT % (function_name, class_name, class_name)
    return frm_body_function


def genPythonFrame(src_module, src_class_name):
    """
    Generation of the frame class text.

    :param src_module: Source module object.
    :param src_class_name: Source class name.
    :return: True/False.
    """
    log_func.info(u'Generate frame class ... START')

    dst_class_name = genFrameClassName(src_class_name)
    src_class = getattr(src_module, src_class_name)

    # Handlers
    src_class_methods = [getattr(src_class, var_name) for var_name in dir(src_class)]
    src_class_events = [method for method in src_class_methods if inspect.isfunction(method) and
                        method.__name__ != '__init__' and
                        'event' in method.__code__.co_varnames and
                        method.__code__.co_argcount == 2]

    # A way to get the source code from a function object+
    #                                                    v
    body_functions = u'\n'.join([u'\n'.join(inspect.getsourcelines(class_method)[0]) for class_method in src_class_events])
    body_functions = body_functions.replace(u'\t', u'    ').replace(u'( ', u'(').replace(u' )', u')')
    log_func.info(u'Append method in class <%s>:' % dst_class_name)
    log_func.debug(body_functions)

    frm_body_function = genShowFunctionBody(dst_class_name)

    py_txt = GEN_PY_MODULE_FMT % (src_class_name,
                                  src_module.__name__,
                                  dst_class_name, src_module.__name__, src_class_name,
                                  src_module.__name__, src_class_name,
                                  body_functions,
                                  frm_body_function)
    log_func.info(u'Generate frame class ... STOP')
    return py_txt
