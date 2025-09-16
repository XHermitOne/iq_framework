#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx OGL diagram specification module.
"""

import wx

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxOglDiagram'

WXOGLDIAGRAM_STYLE= {
    # 'NO_BORDER': wx.NO_BORDER,
    # 'BORDER': wx.BORDER,
    'BORDER_DEFAULT': wx.BORDER_DEFAULT,    # The window class will decide the kind of border to show, if any
    'BORDER_SIMPLE': wx.BORDER_SIMPLE,      # Displays a thin border around the window
    'BORDER_SUNKEN': wx.BORDER_SUNKEN,      # Displays a sunken border
    'BORDER_RAISED': wx.BORDER_RAISED,      # Displays a raised border
    'BORDER_STATIC': wx.BORDER_STATIC,      # Displays a border suitable for a static control. Windows only
    'BORDER_THEME': wx.BORDER_THEME,        # Displays a native border suitable for a control,
                                            # on the current platform.
                                            # On Windows, this will be a themed border;
                                            # on most other platforms a sunken border will be used.
    'BORDER_NONE': wx.BORDER_NONE,          # Displays no border, overriding the default border style for the window
    'BORDER_DOUBLE': wx.BORDER_DOUBLE,      # This style is obsolete and should not be used
    'TRANSPARENT_WINDOW': wx.TRANSPARENT_WINDOW,    # The window is transparent, that is, it will not receive paint events. Windows only.
    'TAB_TRAVERSAL': wx.TAB_TRAVERSAL,      # This style is used by wxWidgets for the windows supporting TAB navigation among their children,
                                            # such as wx.Dialog and wx.Panel.
                                            # It should almost never be used in the application code.

    'WANTS_CHARS': wx.WANTS_CHARS,          # Use this to indicate that the window wants
                                            # to get all char/key events for all keys - even
                                            # for keys like TAB or ENTER which are usually used
                                            # for dialog navigation and which wouldn’t be
                                            # generated without this style.
                                            # If you need to use this style in order
                                            # to get the arrows or etc.,
                                            # but would still like to have normal keyboard navigation
                                            # take place, you should call Navigate in response
                                            # to the key events for Tab and Shift-Tab.

    'NO_FULL_REPAINT_ON_RESIZE': wx.NO_FULL_REPAINT_ON_RESIZE,  # On Windows, this style used to disable repainting
                                                                # the window completely when its size is changed.
                                                                # Since this behaviour is now the default,
                                                                # the style is now obsolete and no longer has an effect.

    'VSCROLL': wx.VSCROLL,      # Use this style to enable a vertical scrollbar.
                                # Notice that this style cannot be used with native
                                # controls which don’t support scrollbars nor with
                                # top-level windows in most ports.

    'HSCROLL': wx.HSCROLL,      # Use this style to enable a horizontal scrollbar.
                                # The same limitations as for wx.VSCROLL apply to this style.

    'ALWAYS_SHOW_SB': wx.ALWAYS_SHOW_SB,    # If a window has scrollbars, disable them instead
                                            # of hiding them when they are not needed
                                            # (i.e. when the size of the window is big
                                            # enough to not require the scrollbars to navigate it).
                                            # This style is currently implemented for wxMSW, wxGTK
                                            # and wxUniversal and does nothing on the other platforms.

    'CLIP_CHILDREN': wx.CLIP_CHILDREN,  # Use this style to eliminate flicker caused
                                        # by the background being repainted,
                                        # then children being painted over them. Windows only.

    'FULL_REPAINT_ON_RESIZE': wx.FULL_REPAINT_ON_RESIZE, # Use this style to force a complete
                                                         # redraw of the window whenever
                                                         # it is resized instead of redrawing
                                                         # just the part of the window affected
                                                         # by resizing. Note that this was
                                                         # the behaviour by default before 2.5.1
                                                         # release and that if you experience
                                                         # redraw problems with code which
                                                         # previously used to work you may want
                                                         # to try this. Currently this style
                                                         # applies on GTK+ 2 and Windows only,
                                                         # and full repainting is always done on other platforms.
}

WXOGLDIAGRAM_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'style': wx.BORDER_NONE,

    'is_draggable': True,
    'on_shape_dbl_click': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/sitemap_application',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'style': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': WXOGLDIAGRAM_STYLE,
        },

        'is_draggable': property_editor_id.CHECKBOX_EDITOR,

        'on_shape_dbl_click': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'is_draggable': u'Can drag and drop shapes?',

        'on_selected': u'Handler for double-clicking on a shape',
    },
}

SPC = WXOGLDIAGRAM_SPC
