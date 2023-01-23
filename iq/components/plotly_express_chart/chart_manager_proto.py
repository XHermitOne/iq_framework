#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chart manager prototype class.
"""

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqChartManagerProto(object):
    """
    Chart manager prototype.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        self.chart_type = None
        self.width = None
        self.height = None
        self.output_type = None
        self.output_image_filename = None

    def getChartType(self):
        """
        Get chart type.
        """
        return self.chart_type

    def setChartType(self, chart_type=None):
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

    def setOutputType(self, output_type=None):
        """
        Set output file type.
        """
        self.output_type = output_type

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
        log_func.error(u'Not supported chart method <drawDataFrame> in <%s>' % self.__class__.__name__)
        return False

    def drawDataset(self, dataset, output_filename=None):
        """
        Draw output image file from dataset (list of dictionaries).

        :param dataset: Dataset (list of dictionaries).
        :param output_filename: Output image filename.
            If None then generate output image filename.
        :return: True/False.
        """
        log_func.error(u'Not supported chart method <drawDataset> in <%s>' % self.__class__.__name__)
        return False

    def draw(self, dataset, *args, **kwargs):
        """
        Draw dataset.

        :param dataset: Dataset (list of dictionaries) or pandas.DataFrame object.
        :return: True/False.
        """
        log_func.error(u'Not supported chart method <draw> in <%s>' % self.__class__.__name__)
        return False
