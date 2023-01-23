#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource editor class module.
"""

import copy
import wx

__version__ = (0, 0, 0, 1)

CLIPBOARD = None


def toClipboard(cur_object, do_copy=False):
    """
    Put object in clipboard.

    :param cur_object: Object.
    :param do_copy: Put object copy?
    """
    global CLIPBOARD

    if isinstance(cur_object, str):
        txt_data_clipboard = wx.TextDataObject()
        txt_data_clipboard.SetText(cur_object)

        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(txt_data_clipboard)
        wx.TheClipboard.Close()

        CLIPBOARD = None
    else:
        CLIPBOARD = copy.deepcopy(cur_object) if do_copy else cur_object
        wx.TheClipboard.Open()
        wx.TheClipboard.Clear()
        wx.TheClipboard.Close()
    return True


def fromClipboard(clear=True):
    """
    Get object from clipboard.

    :param clear: Sign that content is cleared after extraction.
    """
    global CLIPBOARD

    if not isEmptyClipboard():
        buff = CLIPBOARD
        if clear:
            clearClipboard()
        if buff:
            return buff
    else:
        txt_data_clipboard = wx.TextDataObject()
        wx.TheClipboard.Open()
        success = wx.TheClipboard.GetData(txt_data_clipboard)
        wx.TheClipboard.Close()
        if success:
            txt_data = txt_data_clipboard.GetText()
            if clear:
                clearClipboard()
            return txt_data
    return None


def clearClipboard():
    """
    Clear clipboard.
    """
    global CLIPBOARD
    if CLIPBOARD:
        CLIPBOARD = None

    wx.TheClipboard.Open()
    wx.TheClipboard.Clear()
    wx.TheClipboard.Close()


def isEmptyClipboard():
    """
    Is empty clipboard?

    :return: True-empty clipboard.
        False-not empty.
    """
    global CLIPBOARD
    empty_my_buff = CLIPBOARD is None

    txt_data_clipboard = wx.TextDataObject()
    wx.TheClipboard.Open()
    empty_sys_clipboard = not wx.TheClipboard.GetData(txt_data_clipboard)
    wx.TheClipboard.Close()
    return empty_my_buff and empty_sys_clipboard
