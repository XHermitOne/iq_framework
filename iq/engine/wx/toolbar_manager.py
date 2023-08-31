#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Toolbar manager.
"""

import wx

from ...util import log_func

from .import imglib_manager

__version__ = (0, 0, 1, 3)


class iqToolBarManager(imglib_manager.iqImageLibManager):
    """
    Toolbar manager.
    """
    def enableToolbarTools(self, toolbar, **tools):
        """
        Set on / off toolbar tools.

        :param toolbar: wx.ToolBar object.
        :param tools: Dictionary:
            {
                tool_name: True/False,
                ...
            }
            Tool name - name of the control in the wx.FormBuilder project.
            The tool object is searched among the form attributes by type wx.ToolBarToolBase.
        :return: True/False.
        """
        assert issubclass(toolbar.__class__, wx.ToolBar), u'ToolBar manager type error'

        result = True
        for tool_name, enable in tools.items():
            tool = getattr(self, tool_name) if hasattr(self, tool_name) else None
            if tool and isinstance(tool, wx.ToolBarToolBase):
                toolbar.EnableTool(tool.GetId(), enable)
                result = result and True
            else:
                log_func.warning(u'Tool <%s> not found' % tool_name)
                result = result and False

        return result

    def setToolBarLibImages(self, toolbar=None, **tools):
        """
        Set library pictures as pictures tools in wxToolBar.

        :param toolbar: wx.ToolBar object.
        :param tools: Dictionary of correspondence of tool names
            with the names of library image files.
            For example:
                edit_tool = 'fatcaw/document'
        :return: True/False.
        """
        assert issubclass(toolbar.__class__, wx.ToolBar), u'ToolBar manager type error'

        if not tools:
            log_func.warning(u'Not define tools for set images')
            return False

        result = True
        for tool_name, lib_img_name in tools.items():
            if hasattr(self, tool_name):
                # <wx.Tool>
                tool = getattr(self, tool_name)
                tool_id = tool.GetId()
                bmp = self.getImageLibImageBmp(lib_img_name)

                if bmp:
                    if toolbar is None:
                        toolbar = tool.getToolBar()
                    # ATTENTION! To change the tool image, you do not need to use
                    # the tool method < tool.SetNormalBitmap(bmp) > since DOES NOT WORK!
                    # To do this, call the toolbar method < toolbar.SetToolNormalBitmap(tool_id, bmp) >
                    toolbar.SetToolNormalBitmap(tool_id, bmp)
                else:
                    log_func.warning(u'Library icon <%s> not found' % lib_img_name)
                    result = False
            else:
                log_func.warning(u'Tool <%s> not found' % tool_name)
                result = False

        toolbar.Realize()
        return result

    def getToolbarToolLeftBottomPoint(self, toolbar, tool):
        """
        Define the point of the left-bottom edge of the button.
        Used to call up pop-up menus.

        :param toolbar: wx.ToolBar object.
        :param tool: wx.ToolBarToolBase toolbar tool object.
        """
        assert issubclass(toolbar.__class__, wx.ToolBar), u'ToolBar manager type error'
        if tool is None:
            log_func.warning(u'Not define tool')
            return None

        toolbar_pos = toolbar.GetScreenPosition()
        toolbar_size = toolbar.GetSize()
        tool_index = toolbar.GetToolPos(tool.GetId())
        tool_size = toolbar.GetToolSize()
        x_offset = 0
        for i in range(tool_index):
            prev_tool = toolbar.GetToolByPos(i)
            prev_ctrl = prev_tool.GetControl() if prev_tool.IsControl() else None
            x_offset += prev_ctrl.GetSize()[0] if prev_ctrl else tool_size[0]

        return wx.Point(toolbar_pos[0] + x_offset, toolbar_pos[1] + toolbar_size[1])

    def setToolBarToolHelp(self, toolbar, tool, short_help=u'', long_help=u''):
        """
        Set tool short and long help.
        An application might use short help for identifying the tool purpose in a tooltip.
        You might use the long help for displaying the tool purpose on the status line.

        :param toolbar: wx.ToolBar object.
        :param tool: wx.ToolBarToolBase toolbar tool object.
        :param short_help: Shot help.
        :param long_help: Long help.
        :return: True/False.
        """
        assert issubclass(toolbar.__class__, wx.ToolBar), u'ToolBar manager type error'
        if tool is None:
            log_func.warning(u'Not define tool')
            return False

        if isinstance(tool, wx.ToolBarToolBase):
            try:
                if isinstance(short_help, str):
                    toolbar.SetToolShortHelp(toolId=tool.GetId(), helpString=short_help)
                if isinstance(long_help, str):
                    toolbar.SetToolLongHelp(toolId=tool.GetId(), helpString=long_help)
                return True
            except:
                log_func.fatal(u'Error set help tool')
        else:
            log_func.warning(u'Tool type error set help')
        return False
