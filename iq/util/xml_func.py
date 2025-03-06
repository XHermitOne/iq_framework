#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XML file manipulate functions.
"""

import os.path
import xml.etree.ElementTree

from . import log_func

__version__ = (0, 1, 1, 1)


def doXmlTreeElementWalkFunction(xml_element, walk_function=None):
    """
    Execute walk function with element.

    :param xml_element: Xml tree element.
    :param walk_function: Walk function as walk_function_name(xml_element, tag_name, attributes, value).
    :return: True/False.
    """
    if walk_function:
        try:
            result = walk_function(xml_element, xml_element.tag, xml_element.attrib, xml_element.text)
        except:
            log_func.fatal(u'XML. Error execute walk function')
            return False

    child_results = [doXmlTreeElementWalkFunction(child_element, walk_function) for child_element in xml_element]
    return all(child_results)


def runWalkXmlTree(xml_filename, do_save=True, walk_function=None):
    """
    Walk on XML tree fyl run walk function.

    :param xml_filename: XML file name.
    :param do_save: Save XML file after walking.
    :param walk_function: Walk function as walk_function_name(xml_element, tag_name, attributes, value).
    :return: True/False
    """
    if not os.path.exists(xml_filename):
        log_func.warning(u'XML file <%s> not found' % xml_filename)
        return False

    try:
        xml_tree = xml.etree.ElementTree.parse(xml_filename)
        root_node = xml_tree.getroot()
        result = doXmlTreeElementWalkFunction(xml_element=root_node, walk_function=walk_function)
        if do_save:
            # Save XML file
            xml_tree.write(xml_filename)
        return result
    except:
        log_func.fatal(u'Error walk on XML tree. XML file name <%s>' % xml_filename)
    return False