#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UniWriter controller.

This controller is used to write tag values
using XML-RPC data from the UniWriter service."""

import xmlrpc.client

from ...util import log_func

__version__ = (0, 0, 0, 1)


# Default port
DEFAULT_PORT = 8081

# Supported servers
RSLINX_SERVER = u'RSLinx OPC Server'
LOGIKA_DA_SERVER = u'Logika.DA.2'
SERVERS = (RSLINX_SERVER, LOGIKA_DA_SERVER)

# The names of the nodes used
OPC_SERVER_NODE = 'OPC_SERVER_NODE'
OPC_DA_NODE = 'OPC_DA'
NODES = (OPC_SERVER_NODE, OPC_DA_NODE)

# Tag types
INT2_TAG_TYPE = 'int2'
INT4_TAG_TYPE = 'int4'
STRING_TAG_TYPE = 'string'
BOOL_TAG_TYPE = 'bool'
TAG_TYPES = (INT2_TAG_TYPE, INT4_TAG_TYPE, STRING_TAG_TYPE, BOOL_TAG_TYPE)


class iqUniWriterControllerProto(object):
    """
    Universal Remote Writer Controller <UniWriter Remote Service>.
    """
    def __init__(self, host=None, port=DEFAULT_PORT, server=None, node=None, *args, **kwargs):
        """
        Constructor.

        :param host: Server host.
        :param port: Server port. Default 8081.
        :param server: Server name.
        :param node: Node name.
        """
        self.host = host
        self.port = port
        self.server = server
        self.node = node

    def printConnectionParam(self):
        """
        Display communication parameters UniWriter Gateway.
        """
        log_func.info(u'UniWriter <%s>. Communication parameters:' % str(self))
        log_func.info(u'\tHost <%s>' % self.host)
        log_func.info(u'\tPort <%s>' % self.port)
        log_func.info(u'\tNode <%s>' % self.node)
        log_func.info(u'\tServer <%s>' % self.server)

    def writeTags(self, host=None, port=DEFAULT_PORT, server=None, node=None,
                  *tags_tuple, **tags_dict):
        """
        Write tags to UniWriter server.

        :param host: Server host.
        :param port: Server port. Default 8081.
        :param server: Server name.
        :param node: Node name.
        :param tags_tuple: Tags list. Format:
            (('tag address', tag value, 'tag type'), ...)
            The tag type may not be specified.
            Then the tag type is determined by the value type.
        :param tags_dict: Tags dictionary. Format:
            {'tag name': ('Tag address', tag_value, 'tag type'), ...}
            The tag type may not be specified.
            Then the tag type is determined by the value type.
        :return: True - write was successful / False - data write error.
        """
        if host is None:
            host = self.host
            
        if server is None:
            server = self.server
            
        if node is None:
            node = self.node
            
        if not host:
            log_func.warning(u'UniWriter. Not define host')
            return dict()
            
        if not server:
            log_func.warning(u'UniWriter. Not define server name')
            return dict()

        if not node:
            log_func.warning(u'UniWriter. Not define node name')
            return dict()
            
        return self._writeDataXMLRPC(host, port, server, node,
                                     *tags_tuple, **tags_dict)
    
    def _writeDataXMLRPC(self, host, port, server, node, *tags_tuple, **tags_dict):
        """
        Writing data to the UniWriter server. Using XML RPC.

        :param host: Server host.
        :param port: Server port. Default 8081.
        :param server: Server name.
        :param node: Node name.
        :param tags_tuple: Tags list. Format:
            (('tag address', tag value, 'tag type'), ...)
            The tag type may not be specified.
            Then the tag type is determined by the value type.
        :param tags_dict: Tags dictionary. Format:
            {'tag name': ('Tag address', tag_value, 'tag type'), ...}
            The tag type may not be specified.
            Then the tag type is determined by the value type.
        :return: True - write was successful / False - data write error.
        """
        tag_values = tags_tuple if tags_tuple else tags_dict.values()
        check_types = all([isinstance(tag_data, (list, tuple)) and len(tag_data) >= 2 for tag_data in tag_values])
        if not check_types:
            log_func.warning(u'Incorrect tag values')
            log_func.warning(u'Tag dictionary format: {\'tag_name\': (\'tag address\', tag_value, \'tag_type\'), ...}')
            return False

        try:
            # Create OPC client
            opc = xmlrpc.client.ServerProxy('http://%s:%d' % (host, port))

            results = list()
            for tag_value in tag_values:
                if len(tag_value) >= 3:
                    address = tag_value[0]
                    value = tag_value[1]
                    tag_type = tag_value[2]
                else:
                    address = tag_value[0]
                    value = tag_value[1]
                    tag_type = None

                if tag_type == INT2_TAG_TYPE:
                    result = opc.destinations.WriteValueAsInt2(node, server, address, int(value))
                elif tag_type == INT4_TAG_TYPE:
                    result = opc.destinations.WriteValueAsInt4(node, server, address, int(value))
                elif isinstance(value, int):
                    # Default 2-byte
                    result = opc.destinations.WriteValueAsInt2(node, server, address, int(value))
                elif isinstance(value, bool) or tag_type == BOOL_TAG_TYPE:
                    result = opc.destinations.WriteValueAsBoolean(node, server, address,
                                                                  eval(value) if isinstance(value, str) else bool(value))
                elif isinstance(value, str) or tag_type == STRING_TAG_TYPE:
                    result = opc.destinations.WriteValueAsString(node, server, address, str(value))
                else:
                    log_func.warning(u'UniWriter. Unsupported tag type <%s : %s>' % (tag_type, type(value)))
                    result = False
                results.append(result)

            return all(results)
        except:
            log_func.fatal(u'UniWriter. Error write data UniWriter <%s:%d / %s>' % (host, port, server))
        return False

    def writeTag(self, host=None, port=DEFAULT_PORT, server=None, node=None,
                 address=None, tag_type=None, value=None):
        """
        Writing data to the UniWriter server. Using XML RPC.

        :param host: Server host.
        :param port: Server port. Default 8081.
        :param server: Server name.
        :param node: Node name.
        :param address: Tag address.
        :param tag_type: Tag type.
        :param value: Tag value.
        :return: True - write was successful / False - data write error.
        """
        return self.writeTags(host=host, port=port, server=server, node=node,
                              write_tag=(address, value, tag_type))
