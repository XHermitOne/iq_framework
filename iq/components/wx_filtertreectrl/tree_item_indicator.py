#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Class to support the indicator of tree elements.

The indicator is a description
post processing filtered recordset
in order to change the picture / text color / background color
form indication controls.
Indicator description is a list of indicator states,
each of which consists of a condition check expression and
descriptions of the picture / text color / background color.

Filter indicator description format:
[
    {
        'name': The name of the state,
        'image': Image file,
        'text_color': A tuple (R, G, B) of the text color,
        'background_color': A tuple (R, G, B) of the background color,
        'expression': The text of the status check expression code block,
    },
    ...
]


The expression must return True / False.
True - the indicator is in the current state and no further verification is needed.
False - the indicator is not in the current state,
further checking of other states occurs.
From this it is clear that the most critical conditions must be checked first.
Those. they should be in the first place in the list of state descriptions,
and then less critical.

When an expression is executed, a RECORDS object is present in its environment.
RECORDS - a list of dictionaries of records filtered by the current filter.
"""

import os.path
import wx

from ...util import log_func
from ...util import lang_func

from ...engine.wx import wxbitmap_func
from ...engine.wx import wxcolour_func

from . import indicator_constructor_dlg

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

UNKNOWN_STATE_NAME = _('State name not defined')


def createIndicator():
    """
    Creating an indicator list.

    :return: Empty indicator list.
    """
    return list()


def newIndicatorState(indicator=None,
                      name=UNKNOWN_STATE_NAME, img_filename=None,
                      text_color=None, background_color=None,
                      expression=None):
    """
    Add a new state to the indicator list.

    :param indicator: Indicator list.
    :param name: State name.
    :param img_filename: Image filename.
    :param text_color: Text color as (R, G, B).
    :param background_color: Background color as (R, G, B).
    :param expression: The code block text of the status check expression.
    :return: Modified indicator list.
    """
    if text_color is None:
        text_color = wxcolour_func.wxColour2RGB(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
    if background_color is None:
        background_color = wxcolour_func.wxColour2RGB(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

    if indicator is None:
        indicator = createIndicator()
    new_state = dict(name=name, image=img_filename,
                     text_color=text_color, background_color=background_color,
                     expression=expression)
    indicator.append(new_state)
    return indicator


def findIndicatorState(indicator, name):
    """
    Search for an indicator state in the indicator list by name.

    :param indicator: Indicator list.
    :param name: State name.
    :return: A state data structure, or None if there is no state with that name.
    """
    names = [state.get('name', None) for state in indicator]
    find_state = indicator[names.index(name)] if name in names else None
    return find_state


class iqTreeItemIndicator(object):
    """
    Tree element indicator.
    """
    def __init__(self, indicator=None):
        """
        Constructor.

        :param indicator: Current indicator.
        """
        self._indicator = indicator

    def editIndicator(self, parent=None, indicator=None):
        """
        Edit filter indicator.

        :param parent: Parent window.
        :param indicator: Current indicator.
            If not specified, then the description of the internal indicator is taken.
        :return: Edited filter indicator.
        """
        if parent is None:
            app = wx.GetApp()
            parent = app.GetTopWindow()

        if indicator is None:
            indicator = self._indicator

        indicator = indicator_constructor_dlg.editIndicatorConstructorDlg(parent=parent, indicator=indicator)

        return indicator

    def getIndicator(self):
        """
        Set current filter indicator.
        """
        return self._indicator

    def getLabelIndicator(self, indicator=None):
        """
        Get indicator label.

        :param indicator: Current indicator.
            If not specified, then the description of the internal indicator is taken.
        :return: Label filter indicator.
        """
        if indicator is None:
            indicator = self._indicator

        label = u'<%s>' % u', '.join([state_indicator.get('name', UNKNOWN_STATE_NAME) for state_indicator in indicator])
        return label

    def getStateIndicator(self, records=None, indicator=None):
        """
        Determine the state of the indicator by a set of records.

        :param records: Record list.
            It is a list of dictionaries of entries.
        :param indicator: Current indicator.
            If not specified, then the description of the internal indicator is taken.
        :return: State dictionary:
            {
            'name': State name,
            'image': Image filename,
            'text_color': Text color as (R, G, B),
            'background_color': Background color as (R, G, B),
            }
            If the recordset does not match any of the states, then None is returned.
        """
        if indicator is None:
            indicator = self._indicator

        if records is None:
            records = list()

        RECORDS = records

        for state_indicator in indicator:
            state_name = state_indicator.get('name', UNKNOWN_STATE_NAME)
            expression = state_indicator.get('expression', None)
            exp_result = False
            if expression:
                try:
                    exp_result = eval(expression, globals(), locals())
                except:
                    log_func.error(u'Error execute expression:')
                    log_func.fatal(expression)
            else:
                log_func.warning(u'Indicator state expression not defined <%s>' % state_name)

            if exp_result:
                # The condition matches, return a description of the state
                return state_indicator
        # None of the conditions were confirmed
        return None

    def getStateIndicatorObjects(self, records=None, indicator=None):
        """
        Define indicator state objects by a set of records.

        :param records: Record list.
            It is a list of dictionaries of entries.
        :param indicator: Current indicator.
            If not specified, then the description of the internal indicator is taken.
        :return: A tuple of state objects:
            (
                State name,
                Image state as wx.Bitmap object,
                Text color as wx.Colour object,
                Background color as wx.Colour object
            )
            If the recordset does not match any of the states, then it returns (None, None, None, None).
        """
        state_indicator = self.getStateIndicator(records=records, indicator=indicator)
        if state_indicator is None:
            return None, None, None, None

        # Name
        name = state_indicator.get('name', UNKNOWN_STATE_NAME)

        # Image
        image = None
        img_filename = state_indicator.get('image', None)
        if img_filename:
            if os.path.exists(img_filename):
                # Image file specified as an absolute filename
                image = wxbitmap_func.createBitmap(img_filename)
            elif img_filename == os.path.basename(img_filename):
                # Image file specified as the name of the library file
                image = wxbitmap_func.createIconBitmap(img_filename)
            else:
                log_func.warning(u'Incorrect image filename <%s>' % img_filename)

        # Text color
        rgb = state_indicator.get('text_color', None)
        text_colour = wx.Colour(tuple(rgb)) if rgb else None

        # Background color
        rgb = state_indicator.get('background_color', None)
        background_colour = wx.Colour(tuple(rgb)) if rgb else None

        return name, image, text_colour, background_colour
