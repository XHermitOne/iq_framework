#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plotly-express chart manager prototype.
"""

import os.path
import pandas
import plotly.express

from ...util import log_func
from ...util import file_func
from ...util import id_func

__version__ = (0, 0, 0, 1)

DEFAULT_CHART_TYPE = 'bar'
DEFAULT_OUTPUT_FILE_TYPE = 'png'

CHART_TYPE2DRAW_FUNCTION = {
    'scatter': plotly.express.scatter,
    'density_contour': plotly.express.density_contour,
    'density_heatmap': plotly.express.density_heatmap,
    'line': plotly.express.line,
    'area': plotly.express.area,
    'bar': plotly.express.bar,
    'timeline': plotly.express.timeline,
    'histogram': plotly.express.histogram,
    'ecdf': plotly.express.ecdf,
    'violin': plotly.express.violin,
    'box': plotly.express.box,
    'strip': plotly.express.strip,
    'scatter_3d': plotly.express.scatter_3d,
    'line_3d': plotly.express.line_3d,
    'scatter_ternary': plotly.express.scatter_ternary,
    'line_ternary': plotly.express.line_ternary,
    'scatter_polar': plotly.express.scatter_polar,
    'line_polar': plotly.express.line_polar,
    'bar_polar': plotly.express.bar_polar,
    'choropleth': plotly.express.choropleth,
    'scatter_geo': plotly.express.scatter_geo,
    'line_geo': plotly.express.line_geo,
    'scatter_mapbox': plotly.express.scatter_mapbox,
    'choropleth_mapbox': plotly.express.choropleth_mapbox,
    'density_mapbox': plotly.express.density_mapbox,
    'line_mapbox': plotly.express.line_mapbox,
    'scatter_matrix': plotly.express.scatter_matrix,
    'parallel_coordinates': plotly.express.parallel_coordinates,
    'parallel_categories': plotly.express.parallel_categories,
    'pie': plotly.express.pie,
    'sunburst': plotly.express.sunburst,
    'treemap': plotly.express.treemap,
    'icicle': plotly.express.icicle,
    'funnel': plotly.express.funnel,
    'funnel_area': plotly.express.funnel_area,
}


class iqPlotlyExpressChartProto(object):
    """
    Plotly-express chart manager prototype.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        self.chart_type = DEFAULT_CHART_TYPE
        self.width = None
        self.height = None
        self.args = dict()
        self.output_type = DEFAULT_OUTPUT_FILE_TYPE
        self.output_image_filename = None

    def getChartType(self):
        """
        Get chart type.
        """
        return self.chart_type

    def setChartType(self, chart_type=DEFAULT_CHART_TYPE):
        """
        Set chart type.
        """
        self.chart_type = chart_type

    def getWidth(self):
        """
        Get output file width.
        """
        return self.width

    def setWidth(self, width=None):
        """
        Set output file width.
        """
        self.width = width

    def getHeight(self):
        """
        Get output file height.
        """
        return self.height

    def setHeight(self, height=None):
        """
        Set output file height.
        """
        self.height = height

    def getSize(self):
        """
        Get output file size.
        """
        return self.width, self.height

    def setSize(self, width=None, height=None):
        """
        Set output file size.
        """
        self.width = width
        self.height = height

    def getOutputType(self):
        """
        Get output file type.
        """
        return self.output_type

    def setOutputType(self, output_type=DEFAULT_OUTPUT_FILE_TYPE):
        """
        Set output file type.
        """
        self.output_type = output_type

    def getChartArguments(self):
        """
        Get chart function arguments.
        """
        if isinstance(self.args, dict):
            return self.args
        log_func.error(u'Not valid chart function arguments type <%s>' % self.args.__class__.__name__)
        return dict()

    def setChartArguments(self, **args):
        """
        Set chart function arguments.
        """
        self.args = args

    def genOutputImageFilename(self):
        """
        Generate output image filename.
        """
        prj_profile_path = file_func.getProjectProfilePath()
        psp = self.getPassport()
        if psp is not None:
            output_basename = '%s.%s' % (psp.getAsStr(), self.getOutputType())
            return os.path.join(prj_profile_path, output_basename)
        output_basename = '%s.%s' % (self.__class__.__name__ + id_func.genGUID(), self.getOutputType())
        return os.path.join(prj_profile_path, output_basename)

    def getOutputImageFilename(self):
        """
        Get output image filename.
        """
        return self.output_image_filename

    def drawDataFrame(self, dataframe, output_filename=None):
        """
        Draw output image file from pandas.DataFrame.

        :param dataframe: pandas.DataFrame object.
        :param output_filename: Output image filename.
            If None then generate output image filename.
        :return: True/False.
        """
        if output_filename is None:
            output_filename = self.genOutputImageFilename()

        output_ext = '.' + self.getOutputType()
        output_filename = file_func.setFilenameExt(output_filename, output_ext)
        self.output_image_filename = output_filename

        try:
            chart_type = self.getChartType()
            if chart_type in CHART_TYPE2DRAW_FUNCTION:
                chart_func = CHART_TYPE2DRAW_FUNCTION[chart_type]
                args = self.getChartArguments()
                chart = chart_func(dataframe, **args)
                chart.write_image(output_filename)
                return True
            else:
                log_func.warning(u'Not supported chart type <%s>' % chart_type)
        except:
            log_func.fatal(u'Error draw output image file <%s> from pandas.DataFrame' % output_filename)
            log_func.error(str(dataframe))
        return False

    def drawDataset(self, dataset, output_filename=None):
        """
        Draw output image file from dataset (list of dictionaries).

        :param dataset: Dataset (list of dictionaries).
        :param output_filename: Output image filename.
            If None then generate output image filename.
        :return: True/False.
        """
        dataframe = pandas.DataFrame(dataset)
        return self.drawDataFrame(dataframe=dataframe, output_filename=output_filename)

    def draw(self, dataset, *args, **kwargs):
        """
        Draw dataset.

        :param dataset: Dataset (list of dictionaries) or pandas.DataFrame object.
        :return: True/False.
        """
        if isinstance(dataset, (tuple, list)):
            self.drawDataset(dataset, *args, **kwargs)
        return self.drawDataFrame(dataset, *args, **kwargs)
