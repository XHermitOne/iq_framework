#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gnuplot historical trend component.
"""

from . import spc
from . import gnuplot_trend_proto
from .. import wx_panel

from ...util import log_func
from ...util import spc_func
from ...util import str_func

__version__ = (0, 0, 0, 1)


class iqGnuplotTrend(gnuplot_trend_proto.iqGnuplotTrendProto, wx_panel.COMPONENT):
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
        gnuplot_trend_proto.iqGnuplotTrendProto.__init__(self)

        self.createChildren()

        self.setAdaptScene()
        self.setSceneMin()
        self.setSceneMax()

        self.setXFormat()
        self.setYFormat()

        self.setXPrecision()
        self.setYPrecision()

    def setPens(self, pens):
        """
        Set trend pens.

        :param pens: Pen resources.
        :return: True/False.
        """
        self._resource[spc_func.CHILDREN_ATTR_NAME] = pens
        self.createChildren()

        if self.isAdaptScene():
            self.adaptScene()
        else:
            dt_min, y_min = self.getSceneMin()
            dt_max, y_max = self.getSceneMax()
            self.setScene(min_x=dt_min, min_y=y_min, max_x=dt_max, max_y=y_max)

        # Set the color of the feather lines
        self._setPensColour()

    def _setPensColour(self, pens=None, manager=None):
        """
        Set the color of the feather lines.

        :param pens: Pen objects.
        :param manager: Gnuplot program manager.
        :return: True/False.
        """
        if pens is None:
            pens = self.getChildren()
        if manager is None:
            manager = self._getManager()
        for i, pen in enumerate(pens):
            self._setPenColour(n_pen=i + 1, pen=pen, manager=manager)

    def _setPenColour(self, n_pen, pen, manager=None):
        """
        Set pen colour.

        :param n_pen: Pen number.
        :param pen: Pen object.
        :param manager: Gnuplot program manager.
        :return: True/False.
        """
        if manager is None:
            manager = self._getManager()
        try:
            str_colour = pen.getColourStr()
            log_func.debug(u'Pen colour [%d] <%s>' % (n_pen, str_colour))
            if str_colour:
                manager.setLineStyle(n_line=n_pen, line_color=str_colour)
        except:
            log_func.fatal(u'Error set pen colour <%d>' % n_pen)

    def getPens(self):
        """
        Trend pen list.
        """
        pens = self.getChildren()
        if not pens:
            log_func.error(u'Not define trend pens <%s>' % self.getName())
        return pens

    def isAdaptScene(self):
        """
        To adapt the trend scene according to the data?
        """
        if self.adapt_scene is None:
            self.adapt_scene = self.getAttribute('adapt_scene')
        return self.adapt_scene

    def getSceneMin(self):
        """
        Minimum scene values.
        """
        if self.scene_min:
            scene_min = self.scene_min
        else:
            scene_min = self.getAttribute('scene_min')
        if scene_min and isinstance(scene_min, str):
            try:
                scene_min = eval(scene_min)
            except:
                log_func.fatal(u'Scene minimum value num_format error')
                log_func.error(u'Minimum values must be specified by a tuple. For example (\'00:00:00\', 0.0)')
                scene_min = ('00:00:00', 0.0)
        elif scene_min and isinstance(scene_min, (list, tuple)):
            pass
        else:
            log_func.error(u'Error scene minimum value type <%s>' % type(scene_min))
        dt_min = self._str2dt(scene_min[0], self._x_format) if isinstance(scene_min[0], str) else scene_min[0]
        y_min = float(scene_min[1])
        self.scene_min = (dt_min, y_min)
        return dt_min, y_min

    def getSceneTimeMin(self):
        """
        The minimum value of the scene along the time axis.
        """
        scene_min = self.getSceneMin()
        return scene_min[0]

    def getSceneYMin(self):
        """
        The minimum value of the scene along the axis of values.
        """
        scene_min = self.getSceneMin()
        return scene_min[1]

    def getSceneMax(self):
        """
        Maximum scene values.
        """
        if self.scene_max:
            scene_max = self.scene_max
        else:
            scene_max = self.getAttribute('scene_max')
        if scene_max and isinstance(scene_max, str):
            try:
                scene_max = eval(scene_max)
            except:
                log_func.fatal(u'Scene maximum value num_format error')
                log_func.error(u'Maximum values must be specified by a tuple. For example (\'00:00:00\', 0.0)')
                scene_max = ('23:59:59', 100.0)
        elif scene_max and isinstance(scene_max, (list, tuple)):
            pass
        else:
            log_func.error(u'Error scene maximum value type <%s>' % type(scene_max))
        dt_max = self._str2dt(scene_max[0], self._x_format) if isinstance(scene_max[0], str) else scene_max[0]
        y_max = float(scene_max[1])
        self.scene_max = (dt_max, y_max)
        return dt_max, y_max

    def getSceneTimeMax(self):
        """
        The maximum value of the scene along the time axis.
        """
        scene_max = self.getSceneMax()
        return scene_max[0]

    def getSceneYMax(self):
        """
        The maximum value of the scene along the axis of values.
        """
        scene_max = self.getSceneMax()
        return scene_max[1]

    def setXFormat(self, x_format=None):
        """
        Set X-axis data presentation num_format.

        :param x_format: X axis data presentation num_format.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if x_format is None:
            x_format = self.getAttribute('x_format')
        return self.setFormats(x_format, self._y_format)

    def setYFormat(self, y_format=None):
        """
        Set Y-axis data presentation num_format.

        :param y_format: Y axis data presentation num_format.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if y_format is None:
            y_format = self.getAttribute('y_format')
        return self.setFormats(self._x_format, y_format)

    def setSceneMin(self, scene_min=None):
        """
        Set minimum values for the visible trend scene.

        :param scene_min: The minimum values of the visible trend scene.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if scene_min is None:
            scene_min = self.getAttribute('scene_min')
        self.scene_min = scene_min

    def setSceneMax(self, scene_max=None):
        """
        Set maximum values for the visible trend scene.

        :param scene_max: The minimum values of the visible trend scene.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if scene_max is None:
            scene_max = self.getAttribute('scene_max')
        self.scene_max = scene_max

    def setAdaptScene(self, adapt_scene=None):
        """
        Set the sign of scene adaptation according to.

        :param adapt_scene: Sign of scene adaptation according to.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if adapt_scene is None:
            adapt_scene = self.getAttribute('adapt_scene')
        self.adapt_scene = adapt_scene

    def setXPrecision(self, x_precision=None):
        """
        Set the price of the division of the trend grid on the X scale.

        :param x_precision: X grid trend price.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if x_precision is None:
            x_precision = self.getAttribute('x_precision')
        return self.setPrecisions(x_precision, self._y_precision)

    def setYPrecision(self, y_precision=None):
        """
        Set the price of the division of the trend grid on the Y scale.

        :param y_precision: Y grid trend price.
            If not defined, then taken from the resource description of the object.
        :return:
        """
        if y_precision is None:
            y_precision = self.getAttribute('y_precision')
        return self.setPrecisions(self._x_precision, y_precision)


COMPONENT = iqGnuplotTrend
