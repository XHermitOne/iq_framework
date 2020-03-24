#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trend navigation panel based on gnuplot utility.
"""

import os
import os.path
import wx

from . import gnuplot_trend_navigator_panel_proto

from ...util import log_func

from ...engine.wx import listctrl_manager
from ...engine.wx import splitter_manager
from ...engine.wx import form_manager

__version__ = (0, 0, 0, 1)

UNKNOWN_PEN_LABEL = u'Not defined by the developer'

VIEW_REPORT_FILE_FMT = 'evince %s &'
# PRINT_REPORT_FILE_FMT = 'evince --preview %s &'


class iqGnuplotTrendNavigatorProto(gnuplot_trend_navigator_panel_proto.iqGnuplotTrendNavigatorPanelProto,
                                   listctrl_manager.iqListCtrlManager,
                                   splitter_manager.iqSplitterWindowManager,
                                   form_manager.iqFormManager):
    """
    Trend navigation panel based on gnuplot utility.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        gnuplot_trend_navigator_panel_proto.iqGnuplotTrendNavigatorPanelProto.__init__(self, *args, **kwargs)

        # There must be at least one column in the legend
        self.setListCtrlColumns(listctrl=self.legend_listCtrl,
                                cols=(dict(label=u'', width=self.legend_listCtrl.GetSize().GetWidth()), ))

        # Legend display switch
        self.__is_show_legend = False

    def setIsShowLegend(self, is_show):
        """
        Set the legend display switch.

        :param is_show: True - show / False - hide.
        :return:
        """
        return self.showLegend(is_show)

    def draw(self, redraw=True):
        """
        The main method of plotting a trend.

        :param redraw: Forced drawing.
        """
        return self.trend.draw(redraw)

    def getTrend(self):
        """
        Trend object.
        """
        return self.trend

    def setStartDT(self, new_dt):
        """
        The start date-time of the trend.

        :param new_dt: New value.
        """
        return self.trend.setStartDT(new_dt=new_dt)

    def setStopDT(self, new_dt):
        """
        The final date and time of the trend.

        :param new_dt: New value.
        """
        return self.trend.setStopDT(new_dt=new_dt)

    def getStartDT(self):
        """
        The start date-time of the trend.
        """
        return self.trend.getStartDT()

    def getStopDT(self):
        """
        The final date and time of the trend.
        """
        return self.trend.getStopDT()

    def getPenData(self, pen_index=0):
        """
        Data relevant to pen.

        :param pen_index: Pen index. By default, the first pen is taken.
        :return: List (Time, Value).
        """
        return self.trend.getPenData(pen_index=pen_index)

    def setLegend(self, pens=None):
        """
        Set legend.

        :param pens: Pen list.
        :return: True/False.
        """
        if pens is None:
            pens = self.trend.child

        # Clear Legend List Lines
        self.clearListCtrl(listctrl=self.legend_listCtrl)

        try:
            for pen in pens:
                pen_colour_rgb = pen.get('colour', (128, 128, 128))
                # Define the pen inscription in the legend
                pen_label = pen.get('legend', UNKNOWN_PEN_LABEL)
                pen_label = pen_label if pen_label else str(pen.get('description', UNKNOWN_PEN_LABEL))
                self.appendListCtrlRow(listctrl=self.legend_listCtrl, row=(pen_label, ))

                row = self.getListCtrlItemCount(self.legend_listCtrl) - 1
                if isinstance(pen_colour_rgb, tuple) or isinstance(pen_colour_rgb, wx.Colour):
                    self.setListCtrlRowForegroundColour(listctrl=self.legend_listCtrl,
                                                        item=row, colour=pen_colour_rgb)
                elif isinstance(pen_colour_rgb, str):
                    self.setListCtrlRowForegroundColour(listctrl=self.legend_listCtrl,
                                                        item=row, colour=wx.Colour(pen_colour_rgb))
                else:
                    log_func.error(u'Color setting mode not supported')
            return True
        except:
            log_func.fatal(u'Error filling trend legend')
        return False

    def showLegend(self, is_show=True, redraw=True):
        """
        Display legend?

        :param is_show: True - show / False - hide
        :param redraw: Redraw splitter.
        :return: True/False.
        """
        self.__is_show_legend = is_show
        if is_show:
            result = self.expandSplitterWindowPanel(splitter=self.trend_splitter, redraw=redraw)
        else:
            result = self.collapseSplitterWindowPanel(splitter=self.trend_splitter, redraw=redraw)

        # if redraw:
        #     self.trend_splitter.Refresh()
        return result

    def onLegendButtonClick(self, event):
        """
        Legend on / off handler.
        """
        self.showLegend(not self.__is_show_legend)
        event.Skip()

    def onTrendSize(self, event):
        """
        The handler of the trend control change.
        """
        width, height = self.getTrend().GetSize()
        log_func.debug(u'Redraw trend [%d x %d]' % (width, height))
        self.getTrend().draw(size=(width, height))
        # self.showLegend(self.__is_show_legend)
        event.Skip()

    def onPrintButtonClick(self, event):
        """
        Trend print button handler.
        """
        frame_filename = self.getReport()

        if frame_filename and os.path.exists(frame_filename):
            printerfunc.printPDF(frame_filename)

        event.Skip()

    def getReport(self):
        """
        Get the report as a PDF file.

        :return: PDF or None file name in case of error.
        """
        try:
            width, height = self.getTrend().GetSize()
            line_data = self.getTrend().getPenData()
            frame_filename = self.getTrend().reportFrame(size=(width, height),
                                                         scene=self.getTrend().getCurScene(),
                                                         points=line_data)
            return frame_filename
        except:
            log_func.fatal(u'Error receiving report')
        return None

    def onViewButtonClick(self, event):
        """
        Button handler for viewing a trend report.
        """
        frame_filename = self.getReport()

        if frame_filename and os.path.exists(frame_filename):
            cmd = VIEW_REPORT_FILE_FMT % frame_filename
            log_func.info(u'Command execution <%s>' % cmd)
            try:
                os.system(cmd)
            except:
                log_func.fatal(u'Command execution error <%s>' % cmd)

        event.Skip()

    def onSettingsButtonClick(self, event):
        """
        Button handler for advanced trend settings.
        """
        dlgfunc.openWarningBox(_(u'SETTINGS'),
                               _(u'This feature has not yet been implemented'))
        event.Skip()

    def onUpButtonClick(self, event):
        """
        Move the scene up.
        """
        self.getTrend().moveSceneY(step=1)
        event.Skip()

    def onDownButtonClick(self, event):
        """
        Scene moving down.
        """
        self.getTrend().moveSceneY(step=-1)
        event.Skip()

    def onZoomInButtonClick(self, event):
        """
        Scaling. Magnification.
        """
        self.getTrend().zoomY(step=-1)
        event.Skip()

    def onZoomOutButtonClick(self, event):
        """
        Scaling. Decrease.
        """
        self.getTrend().zoomY(step=1)
        event.Skip()

    def onFirstButtonClick(self, event):
        """
        Move the scene to the beginning of the data.
        """
        self.getTrend().moveSceneFirst()
        event.Skip()

    def onLastButtonClick(self, event):
        """
        Move the scene to the end of the data.
        """
        self.getTrend().moveSceneLast()
        event.Skip()

    def onPrevButtonClick(self, event):
        """
        Move the scene to the left.
        """
        self.getTrend().moveSceneX(step=-1)
        event.Skip()

    def onNextButtonClick(self, event):
        """
        Move the scene to the right.
        """
        self.getTrend().moveSceneX(step=1)
        event.Skip()

    def onTimeZoomInButtonClick(self, event):
        """
        Scaling. Timeline magnification (X-bar).
        """
        self.getTrend().zoomX(step=-1)
        event.Skip()

    def onTimeZoomOutButtonClick(self, event):
        """
        Scaling. Zoom out on the timeline (X scale).
        """
        self.getTrend().zoomX(step=1)
        event.Skip()

