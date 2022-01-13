#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert XML -> python dictionary functions.
"""

import os
import os.path
import xmltodict
from xml.sax import xmlreader
import xml.sax.handler

from . import log_func
from . import str_func
from . import txtfile_func
from . import spc_func

__version__ = (0, 0, 1, 2)

DEFAULT_XML_TAG = 'Excel'

TAG_KEY = 'name'
CHILDREN_KEY = spc_func.CHILDREN_ATTR_NAME
VALUE_KEY = 'value'


def XmlFile2Dict(xml_filename, encoding='utf-8'):
    """
    The function of converting Excel files in xml format to the Python dictionary.

    :param xml_filename: xml file name.
    :return: The function returns a completed dictionary, or None if error.
    """
    xml_file = None
    try:
        xml_file = open(xml_filename, 'r')

        input_source = xmlreader.InputSource()
        input_source.setEncoding(encoding)
        input_source.setByteStream(xml_file)
        log_func.debug(u'Parse XML <%s>. Encoding <%s : %s>' % (xml_filename, encoding, input_source.getEncoding()))

        xml_reader = xml.sax.make_parser()
        xml_parser = iqXML2DICTReader(encoding=encoding)
        xml_reader.setContentHandler(xml_parser)

        # enable namespaces option
        xml_reader.setFeature(xml.sax.handler.feature_namespaces, 1)
        xml_reader.parse(input_source)
        xml_file.close()

        return xml_parser.getData()
    except:
        if xml_file:
            xml_file.close()
        log_func.fatal(u'Error read file <%s>' % xml_filename)
    return None


class iqXML2DICTReader(xml.sax.handler.ContentHandler):
    """
    Excel-xml file analyzer class.
    """
    def __init__(self, encoding='utf-8', *args, **kws):
        """
        Constructor.
        """
        xml.sax.handler.ContentHandler.__init__(self, *args, **kws)

        # Result data
        self._data = {TAG_KEY: DEFAULT_XML_TAG, CHILDREN_KEY: []}
        # Current populated node
        self._cur_path = [self._data]

        # Current parsed value
        self._cur_value = None

        # code page
        self.encoding = encoding

    def setName(self, name):
        self._data[TAG_KEY] = name

    def getName(self):
        return self._data[TAG_KEY]

    def getData(self):
        """
        Result data dictionary.
        """
        return self._data

    def _evalValue(self, value):
        """
        An attempt to cast data types.
        """
        try:
            return eval(value)
        except:
            # It is string
            return value
        
    def characters(self, content):
        """
        Данные.
        """
        if content.strip():
            if self._cur_value is None:
                self._cur_value = ''
            self._cur_value += content

    def startElementNS(self, name, qname, attrs):
        """
        Parsing the start of a tag.
        """
        # The element name is specified by the tuple
        if isinstance(name, tuple):
            # Item name
            element_name = name[1]

            # Create a structure corresponding to the element
            self._cur_path[-1][CHILDREN_KEY].append({TAG_KEY: element_name, CHILDREN_KEY: []})
            self._cur_path.append(self._cur_path[-1][CHILDREN_KEY][-1])
            cur_node = self._cur_path[-1]

            # Parameter names
            element_qnames = attrs.getQNames()
            if element_qnames:
                # Parsing item parameters
                for cur_qname in element_qnames:
                    # Parameter name
                    element_qname = attrs.getNameByQName(cur_qname)[1]
                    # Parameter value
                    element_value = attrs.getValueByQName(cur_qname)
                    cur_node[element_qname] = element_value

    def endElementNS(self, name, qname): 
        """
        Parsing the closing tag.
        """
        # Save parsed value
        if self._cur_value is not None:
            self._cur_path[-1][VALUE_KEY] = self._cur_value
            self._cur_value = None

        del self._cur_path[-1]


def _stripXmlDictKeys(xml_dict):
    """
    Remove excess from dictionary keys.

    :param xml_dict: Processed XML Data Dictionary.
        The keys in this dictionary are presented as:
        u'http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01:Documents'
    :return: Processed Dictionary.
        The keys in this dictionary are presented as:
        u'Documents'
    """
    result = dict()
    for key, value in xml_dict.items():
        new_key = key.split(u':')[-1]
        if isinstance(value, dict):
            new_value = _stripXmlDictKeys(value)
        elif isinstance(value, list):
            new_value = list()
            for item in value:
                new_value.append(_stripXmlDictKeys(item))
        else:
            new_value = value
        result[new_key] = new_value
    return result


def convertXmlText2Dict(xml_text_data, codepage='utf-8'):
    """
    Easily convert XML text to dictionary.

    :param xml_text_data: XML text data.
    :param codepage: XML code page.
    :return: Vocabulary matching XML text.
    """
    result_dict = xmltodict.parse(xml_text_data, codepage, process_namespaces=True)
    # It is necessary to convert dictionary keys and remove unnecessary
    return _stripXmlDictKeys(result_dict)


def convertXmlFile2Dict(xml_filename, codepage='utf-8'):
    """
    Simple conversion of an XML file to a dictionary.

    :param xml_filename: XML filename.
    :param codepage: XML code page.
    :return: Vocabulary matching XML text.
    """
    if not os.path.exists(xml_filename):
        log_func.warning(u'XML file <%s> not found' % xml_filename)
        return dict()

    body_xml = txtfile_func.loadTextFile(xml_filename)

    # Recode text if necessary
    src_codepage = str_func.getCodepage(body_xml)
    if src_codepage and src_codepage.lower() != codepage:
        log_func.info(u'Recode XML file <%s> from <%s> to <%s> code page' % (xml_filename, src_codepage, codepage))
        body_xml = str_func.recodeText(body_xml, src_codepage, codepage)
    elif not src_codepage:
        log_func.warning(u'It is not possible to define the code page of an XML file <%s>' % xml_filename)

    return convertXmlText2Dict(body_xml, codepage)
