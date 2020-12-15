#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Splitter window manager.
"""

import wx

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqSplitterWindowManager(object):
    """
    Splitter window manager.
    """
    def collapseSplitterWindowPanel(self, splitter, toolbar=None, collapse_tool=None, expand_tool=None,
                                    resize_panel=0, redraw=True):
        """
        Collapse the splitter panel.

        :param splitter: wx.SplitterWindow object.
        :param toolbar: ToolBar object.
        :param collapse_tool: Collapse tool.
        :param expand_tool: Expand tool.
        :param resize_panel: Resizable panel index.
        :param redraw: Redrawing object?
        :return: True/False.
        """
        assert issubclass(splitter.__class__, wx.SplitterWindow), u'SplitterWindow manager type error'

        setattr(self, '_last_sash_position_%s' % splitter.GetId(),
                splitter.GetSashPosition())

        if resize_panel == 0:
            # ATTENTION! It is impossible to indicate the position of the splitter as 0
            # otherwise, the panel collapse will not be complete
            #                        v
            splitter.SetSashPosition(1, redraw=redraw)
        elif resize_panel == 1:
            split_mode = splitter.GetSplitMode()
            sash_pos = splitter.GetSize().GetHeight() if split_mode == wx.SPLIT_HORIZONTAL else splitter.GetSize().GetWidth()
            splitter.SetSashPosition(sash_pos - 1, redraw=redraw)
        else:
            log_func.warning(u'Invalid rollup panel index')
            return False

        if toolbar and issubclass(toolbar.__class__, wx.ToolBar):
            if collapse_tool:
                toolbar.EnableTool(collapse_tool.GetId(), False)
            if expand_tool:
                toolbar.EnableTool(expand_tool.GetId(), True)
        return True

    def expandSplitterWindowPanel(self, splitter, toolbar=None, collapse_tool=None, expand_tool=None,
                                  resize_panel=0, redraw=True):
        """
        Expand the splitter panel.

        :param splitter: wx.SplitterWindow object.
        :param toolbar: ToolBar object.
        :param collapse_tool: Collapse tool.
        :param expand_tool: Expand tool.
        :param resize_panel: Resizable panel index.
        :param redraw: Redrawing object?
        :return: True/False.
        """
        assert issubclass(splitter.__class__, wx.SplitterWindow), u'SplitterWindow manager type error'

        last_sash_position_name = '_last_sash_position_%s' % splitter.GetId()
        if not hasattr(self, last_sash_position_name):
            log_func.warning(u'The previous position of the splitter panel is not determined')
            return False

        last_sash_position = getattr(self, last_sash_position_name)

        if resize_panel == 0:
            if last_sash_position != splitter.GetSashPosition():
                splitter.SetSashPosition(last_sash_position, redraw=redraw)
        elif resize_panel == 1:
            if last_sash_position != splitter.GetSashPosition():
                splitter.SetSashPosition(last_sash_position, redraw=redraw)
        else:
            log_func.warning(u'Invalid rollup panel index')
            return False

        if toolbar and issubclass(toolbar.__class__, wx.ToolBar):
            if collapse_tool:
                toolbar.EnableTool(collapse_tool.GetId(), True)
            if expand_tool:
                toolbar.EnableTool(expand_tool.GetId(), False)
        return True
