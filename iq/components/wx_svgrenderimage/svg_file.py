#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SVG file class.
"""

import os.path

# import pysvg
import pysvg.parser

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqSVGFile(object):
    """
    SVG file class.
    """
    def __init__(self, svg_filename=None):
        """
        Constructor.

        :param svg_filename: SVG filename.
        """
        self._svg_filename = svg_filename

        self._root = None

    def loadSVG(self, svg_filename):
        """
        Load SVG file struct.

        :param svg_filename: SVG filename.
        :return: SVG file root object or None if error.
        """
        if not os.path.exists(svg_filename):
            log_func.warning(u'SVG file <%s> not found' % svg_filename)
            self._root = None
            return None

        try:
            self._root = pysvg.parser.parse(svg_filename)
            self._svg_filename = svg_filename
            return self._root
        except:
            log_func.fatal(u'Error load SVG file <%s>' % svg_filename)
        return None

    def saveSVG(self, svg_filename):
        """
        Save SVG file.

        :param svg_filename: SVG filename.
        :return: True/False.
        """
        try:
            if self._root is not None:
                self._root.save(svg_filename)
                self._svg_filename = svg_filename
                return True
            else:
                log_func.warning(u'Empty SVG data')
        except:
            log_func.fatal(u'Error save SVG file <%s>' % svg_filename)
        return False

    def findElementByID(self, element_id):
        """
        Find element by id in SVG data.

        :param element_id: Element ID.
        :return: Element object.
        """
        all_elements = self._root.getAllElementsOfHirarchy()
        for element in all_elements:
            if element.get_id() == element_id:
                return element
        log_func.warning(u'Element <%s> not found in SVG data' % element_id)
        return None

    def setElementStyleOption(self, element, option_name, option_value):
        """
        Set element style option.

        :param element: Element object.
        :param option_name: Option name.
        :param option_value: Option value.
        :return: True/False.
        """
        try:
            style = element.get_style()
            style_dict = dict([option.split(':') for option in style.split(';')])
            style_dict[option_name] = option_value

            style_str = ';'.join(['%s:%s' % (opt_name, opt_value) for opt_name, opt_value in style_dict.items()])
            element.set_style(style_str)
            return True
        except:
            log_func.fatal(u'Error set element style option')
        return False

    def setElementStyleOptions(self, element, **options):
        """
        Set element style options.

        :param element: Element object.
        :param options: Dictionary {Option name: Option value, ...}.
        :return: True/False.
        """
        try:
            style = element.get_style()
            style_dict = dict([option.split(':') for option in style.split(';')])

            for option_name, option_value in options.items():
                style_dict[option_name] = option_value

            style_str = ';'.join(['%s:%s' % (opt_name, opt_value) for opt_name, opt_value in style_dict.items()])
            element.set_style(style_str)
            return True
        except:
            log_func.fatal(u'Error set element style options')
        return False
