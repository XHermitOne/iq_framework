#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx python key combins.

Use for accelerator tables (wx.AcceleratorTable).
For combin use <_> symbol. For example CTRL_F1.
"""

import wx

from ...util import log_func

# Keys
F1 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F1, label='F1')
F2 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F2, label='F2')
F3 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F3, label='F1')
F4 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F4, label='F1')
F5 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F5, label='F1')
F6 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F6, label='F1')
F7 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F7, label='F1')
F8 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F8, label='F1')
F9 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F9, label='F1')
F10 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F10, label='F1')
F11 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F11, label='F1')
F12 = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_F12, label='F1')

ESC = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_ESCAPE, label='ESC')
SPACE = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_SPACE, label='SPACE')

# The main ENTER cannot be activated.
# Used in wx controls ------------------------v
ENTER = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_NUMPAD_ENTER, label='ENTER')
INS = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_INSERT, label='INS')
DEL = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_DELETE, label='DEL')
HOME = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_HOME, label='HOME')
END = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_END, label='END')
BACKSPACE = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_BACK, label='BACKSPACE')
PAGEUP = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_PAGEUP, label='PAGEUP')
PAGEDOWN = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_PAGEDOWN, label='PAGEDOWN')
SHIFT = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_SHIFT, label='SHIFT')
ALT = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_ALT, label='ALT')
LEFT = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_LEFT, label='LEFT')
RIGHT = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_RIGHT, label='RIGHT')
UP = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_UP, label='UP')
DOWN = dict(mode=wx.ACCEL_NORMAL, key=wx.WXK_DOWN, label='DOWN')

# Key combins
CTRL_UP = dict(mode=wx.ACCEL_CTRL, key=wx.WXK_UP, label='CTRL+UP')
CTRL_DOWN = dict(mode=wx.ACCEL_CTRL, key=wx.WXK_DOWN, label='CTRL+DOWN')
CTRL_LEFT = dict(mode=wx.ACCEL_CTRL, key=wx.WXK_LEFT, label='CTRL+LEFT')
CTRL_RIGHT = dict(mode=wx.ACCEL_CTRL, key=wx.WXK_RIGHT, label='CTRL+RIGHT')

KEY_COMBUNE_NAME_SEPARATOR = '_'


def getKeyCombine(key_combin_name):
    """
    Get key combins.

    :param key_combin_name: Key combin name.
        Use for accelerator tables (wx.AcceleratorTable).
        For combin use <_> symbol. For example CTRL_F1.
    :return: Key combin dictionary or None if combin not defined.
        Dictionary:
        {
            'mode': Key combin mode
                    wx.ACCEL_NORMAL - Single key
                    wx.ACCEL_CTRL - Pressed <Control>
                    wx.ACCEL_ALT - Pressed <Alt>
                    wx.ACCEL_SHIFT - Pressed <Shift>
            'key': Key. wx.WXK_... constant.
                For example wx.WXK_F1
                or ORD code. For example ord('Q').
            'label': Key combin for help.
        }
    """
    key_combin = globals().get(key_combin_name, None)
    if key_combin is None:
        # Parse key combin
        key_combin_list = key_combin_name.split(KEY_COMBUNE_NAME_SEPARATOR)

        ctrl_key = key_combin_list[-1]
        wx_key = 'WXK_' + ctrl_key
        combin_key = getattr(wx, wx_key) if hasattr(wx, wx_key) else globals().get(ctrl_key, ord(ctrl_key))

        if key_combin_list[:-1]:
            combin_mode = 0
            for ctrl_key in key_combin_list[:-1]:
                if ctrl_key == 'CTRL':
                    combin_mode |= wx.ACCEL_CTRL
                elif ctrl_key == 'ALT':
                    combin_mode |= wx.ACCEL_ALT
                elif ctrl_key == 'SHIFT':
                    combin_mode |= wx.ACCEL_SHIFT
                else:
                    log_func.warning(u'Unsupported key <%s> in combin' % ctrl_key)
        else:
            # Single key
            combin_mode = wx.ACCEL_NORMAL
        key_combin = dict(mode=combin_mode, key=combin_key,
                          label=key_combin_name.replace(KEY_COMBUNE_NAME_SEPARATOR, '+'))

    return key_combin
