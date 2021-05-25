#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PieCtrl component.
"""

import math
import wx
import wx.lib.agw.piectrl

from ..wx_widget import component

from . import spc

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqWxPieCtrl(wx.lib.agw.piectrl.PieCtrl, component.iqWxWidget):
    """
    Wx PieCtrl component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        component.iqWxWidget.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        position = self.getPosition()
        if not position or position[0] <= 0 or position[1] <= 0:
            position = wx.DefaultPosition
        size = self.getSize()
        if not size or size[0] <= 0 or size[1] <= 0:
            size = wx.Size(180, 270)
        # log_func.debug(u'Position: %s : %s\tSize: %s : %s' % (str(position), type(position),
        #                                                       str(size), type(size)))

        wx.lib.agw.piectrl.PieCtrl.__init__(self, parent=parent, id=wx.NewId(),
                                            pos=position, size=size,
                                            *args, **kwargs)

        show_legend = self.getShowLegend()
        if show_legend:
            self.GetLegend().Show()
        else:
            self.GetLegend().Hide()

        legend_transparent = self.getLegendTransparent()
        self.GetLegend().SetTransparent(legend_transparent)

        self.GetLegend().SetHorizontalBorder(self.getLegendHorizontalBorder())
        self.GetLegend().SetVerticalBorder(self.getLegendVerticalBorder())

        self.GetLegend().SetWindowStyle(self.getLegendWindowStyle())

        font = self.getLegendLabelFont()
        if font:
            self.GetLegend().SetLabelFont(font)

        colour = self.getLegendLabelColour()
        if colour:
            self.GetLegend().SetLabelColour(colour)
        colour = self.getLegendBackgroundColour()
        if colour:
            self.GetLegend().SetBackgroundColour(colour)

        angle = self.getAngle()
        if angle >= 0:
            self.SetAngle(float(angle)/180.0 * math.pi)

        rotation_angle = self.getRotationAngle()
        if rotation_angle >= 0:
            self.SetRotationAngle(float(rotation_angle)/180.0 * math.pi)

        show_edges = self.getShowEdges()
        self.SetShowEdges(show_edges)

        colour = self.getBackgroundColour()
        if colour:
            self.SetBackColour(colour)

        self.defaultDraw()

    def defaultDraw(self):
        """
        Default draw.

        :return: True/False.
        """
        self.clear()
        return self.addPart(label=u'No data', value=300)

    def getAngle(self):
        """
        Orientation angle, in degree.
        """
        angle = self.getAttribute('angle')
        return max(0.0, min(angle, 90.0))

    def getRotationAngle(self):
        """
        The angle at which the first sector starts, in degree.
        """
        angle = self.getAttribute('rotation_angle')
        return max(0.0, min(angle, 360.0))

    def getShowEdges(self):
        """
        Whether the control edges are visible or not.

        :return: True/False.
        """
        return self.getAttribute('show_edges')

    def getShowLegend(self):
        """
        Show legend?

        :return: True/False.
        """
        return self.getAttribute('show_legend')

    def getLegendTransparent(self):
        """
        Toggles the legend transparency (visibility).

        :return: True/False.
        """
        return self.getAttribute('legend_transparent')

    def getLegendHorizontalBorder(self):
        """
        The legend’s horizontal border, in pixels.
        """
        border = self.getAttribute('legend_horizontal_border')
        return border if border >= 0 else 0

    def getLegendVerticalBorder(self):
        """
        The legend’s vertical border, in pixels.
        """
        border = self.getAttribute('legend_vertical_border')
        return border if border >= 0 else 0

    def getLegendWindowStyle(self):
        """
        The legend’s window style.
        """
        return self.getAttribute('legend_window_style')

    def getLegendLabelFont(self):
        """
        The legend label font.
        """
        return self.getAttribute('legend_label_font')

    def getLegendLabelColour(self):
        """
        The legend label colour.
        """
        return self.getAttribute('legend_label_colour')

    def getLegendBackgroundColour(self):
        """
        The legend background colour.
        """
        return self.getAttribute('legend_background_colour')

    def clear(self):
        """
        Clear control.

        :return: True/False.
        """
        self._series.clear()
        return True

    def addPart(self, label=u'Unknown', value=100, colour=None):
        """
        Add part.

        :param label: Part label.
        :param value: Part value.
        :param colour: Part colour.
            If not define then get wx.LIGHT_GREY colour.
        :return: True/False.
        """
        try:
            part = wx.lib.agw.piectrl.PiePart()

            part.SetLabel(label if isinstance(label, str) else u'Unknown')
            part.SetValue(value)
            if colour is None:
                colour = wx.LIGHT_GREY
            elif isinstance(colour, str):
                colour = wx.Colour(colour)

            if not isinstance(colour, wx.Colour):
                log_func.warning(u'Error type colour <%s>' % type(colour))
                colour = wx.LIGHT_GREY
            part.SetColour(colour)

            self._series.append(part)
            return True
        except:
            log_func.fatal(u'Error add part to control <%s : %s>' % (self.__class__.__name__, self.getName()))
        return False


COMPONENT = iqWxPieCtrl
