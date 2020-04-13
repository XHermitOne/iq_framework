#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gnuplot historical trend navigator component.
"""

import wx

from . import spc
from . import gnuplot_trend_navigator_proto
from .. import wx_panel

from ...util import log_func
from ...util import spc_func

__version__ = (0, 0, 0, 1)


class iqGnuplotTrendNavigator(gnuplot_trend_navigator_proto.iqGnuplotTrendNavigatorProto,
                              wx_panel.COMPONENT):
    """
    Gnuplot historical trend component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        wx_panel.COMPONENT.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        gnuplot_trend_navigator_proto.iqGnuplotTrendNavigatorProto.__init__(self, parent=parent)

        self.setAdaptScene()
        self.setSceneMin()
        self.setSceneMax()

        self.setXFormat()
        self.setYFormat()

        self.setXPrecision()
        self.setYPrecision()

        self.createChildren()

        # Feathers defined in the navigator pass the trend
        self.setPens(self.getResource()[spc_func.CHILDREN_ATTR_NAME])

        # If you need to remove / free resources when removing control,
        # then you need to use the wx.EVT_WINDOW_DESTROY event
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

    def onDestroy(self, event):
        """
        When removing the panel. Event handler.
        If you need to remove / free resources when removing control,
        then you need to use the wx.EVT_WINDOW_DESTROY event
        """
        self.saveTrendSplitterSashPos()

    def setPens(self, pens):
        """
        Set trend feathers.

        :param pens: Pen resources.
        :return: True/False.
        """
        self.setLegend(pens)
        return self.trend.setPens(pens)

    def getPens(self):
        """
        Trend pen objects.
        """
        return self.trend.getPens()

    def saveTrendSplitterSashPos(self):
        """
        Keep the position of the splitter of the separation of legend and trend.
        """
        return self.saveFormData(name=self.getName(), data=dict(sash_pos=self.trend_splitter.GetSashPosition()))

    def loadTrendSplitterSashPos(self, is_update_size=True):
        """
        Load legend and trend splitter position.

        :param is_update_size: Make a size update?
        """
        save_data = self.loadFormData(name=self.getName())
        default_sash_pos = self.trend_splitter.GetSashPosition() if self.isShowLegend() else 1
        result = self.trend_splitter.SetSashPosition(save_data.get('sash_pos', default_sash_pos))
        if is_update_size:
            self.trend_splitter.UpdateSize()
        return result

    def isShowLegend(self):
        """
        Show legend?
        :return: True/False.
        """
        return self.getAttribute('show_legend')

    def setXFormat(self, x_format=None):
        """
        Set X-axis data presentation format.

        :param x_format: X axis data presentation format.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if x_format is None:
            x_format = self.getAttribute('x_format')
        trend = self.getTrend()
        return trend.setXFormat(x_format)

    def setYFormat(self, y_format=None):
        """
        Set Y-axis data presentation format.

        :param y_format: Y axis data presentation format.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if y_format is None:
            y_format = self.getAttribute('y_format')
        trend = self.getTrend()
        return trend.setYFormat(y_format)

    def setSceneMin(self, scene_min=None):
        """
        Set the minimum values of the visible trend scene.

        :param scene_min: The minimum values of the visible trend scene.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if scene_min is None:
            scene_min = self.getAttribute('scene_min')
        trend = self.getTrend()
        return trend.setSceneMin(scene_min)

    def setSceneMax(self, scene_max=None):
        """
        Set the maximum values of the visible trend scene.

        :param scene_max: The maximum values of the visible trend scene.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if scene_max is None:
            scene_max = self.getAttribute('scene_max')
        trend = self.getTrend()
        return trend.setSceneMax(scene_max)

    def setAdaptScene(self, adapt_scene=None):
        """
        Set the sign of scene adaptation according to.

        :param adapt_scene: Sign of scene adaptation according to.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if adapt_scene is None:
            adapt_scene = self.getAttribute('adapt_scene')
        trend = self.getTrend()
        return trend.setAdaptScene(adapt_scene)

    def setXPrecision(self, x_precision=None):
        """
        Set X grid trend price.

        :param x_precision: X grid trend price.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if x_precision is None:
            x_precision = self.getAttribute('x_precision')
        trend = self.getTrend()
        return trend.setXPrecision(x_precision)

    def setYPrecision(self, y_precision=None):
        """
        Set Y grid trend price.

        :param y_precision: Y grid trend price.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if y_precision is None:
            y_precision = self.getAttribute('y_precision')
        trend = self.getTrend()
        return trend.setYPrecision(y_precision)


COMPONENT = iqGnuplotTrendNavigator
