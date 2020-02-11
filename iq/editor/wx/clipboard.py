#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource editor class module.
"""

import wx

__version__ = (0, 0, 0, 1)

CLIPBOARD = None


def toClipboard(cur_object):
    """
    Put object in clipboard.

    :param cur_object: Object.
    """
    global CLIPBOARD
    if CLIPBOARD is None:
        CLIPBOARD = wx.Clipboard()
        CLIPBOARD.Open()

    if isinstance(cur_object, str):
        txt_data_clipboard = wx.TextDataObject()
        txt_data_clipboard.SetText(cur_object)

        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(txt_data_clipboard)
        wx.TheClipboard.Close()

        CLIPBOARD = None
    else:
        CLIPBOARD.SetData(cur_object)
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
    if CLIPBOARD is None:
        CLIPBOARD = wx.Clipboard()
        CLIPBOARD.Open()

    if not isEmptyClipboard():
        buff = CLIPBOARD.Get()
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
        CLIPBOARD.Clear()
        CLIPBOARD.Close()
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
    empty_my_buff = not CLIPBOARD.IsOpened() if CLIPBOARD else True

    txt_data_clipboard = wx.TextDataObject()
    wx.TheClipboard.Open()
    empty_sys_clipboard = not wx.TheClipboard.GetData(txt_data_clipboard)
    wx.TheClipboard.Close()
    return empty_my_buff and empty_sys_clipboard
