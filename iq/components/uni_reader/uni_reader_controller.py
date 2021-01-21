#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Universal Remote Read Controller <UniReader Remote Service>.

This controller is used to read data from the UniReader service using XML-RPC.
"""

import xmlrpc.client

from ...util import log_func

__version__ = (0, 0, 0, 1)


# Default port used
DEFAULT_PORT = 8080

# Supported servers
RSLINX_SERVER = u'RSLinx OPC Server'
LOGIKA_DA_SERVER = u'Logika.DA.2'
SERVERS = (RSLINX_SERVER, LOGIKA_DA_SERVER)

# The names of the nodes used
OPC_SERVER_NODE = 'OPC_SERVER_NODE'
OPC_DA_NODE = 'OPC_DA'
NODES = (OPC_SERVER_NODE, OPC_DA_NODE)


class iqUniReaderControllerProto(object):
    """
    Universal Remote Read Controller <UniReader Remote Service>.
    """
    def __init__(self, host=None, port=DEFAULT_PORT, server=None, node=None, *args, **kwargs):
        """
        Constructor.

        :param host: Server host.
        :param port: Server port. Default 8080.
        :param server: Server name.
        :param node: Node name.
        """
        self.host = host
        self.port = port
        self.server = server
        self.node = node

    def printConnectionParam(self):
        """
        Display communication parameters UniReader Gateway.
        """
        log_func.info(u'UniReader <%s>. Communication parameters:' % str(self))
        log_func.info(u'\tHost <%s>' % self.host)
        log_func.info(u'\tPort <%s>' % self.port)
        log_func.info(u'\tNode <%s>' % self.node)
        log_func.info(u'\tServer <%s>' % self.server)

    def readTags(self, host=None, port=DEFAULT_PORT, server=None, node=None, **tags):
        """
        Read data from UniReader server.

        :param host: Server host.
        :param port: Server port. Default 8080.
        :param server: Server name.
        :param node: Node name.
        :param tags: Tags dictionary.
            {'tag_name': 'tag_address', ...}
        :return: Tags dictionary with data.
        """
        if host is None:
            host = self.host
            
        if server is None:
            server = self.server
            
        if node is None:
            node = self.node
            
        if not host:
            log_func.warning(u'UniReader. Not define host')
            return dict()
            
        if not server:
            log_func.warning(u'UniReader. Not define server name')
            return dict()

        if not node:
            log_func.warning(u'UniReader. Not define node')
            return dict()
            
        return self._readDataXMLRPC(host, port, server, node, **tags)
    
    def _readDataXMLRPC(self, host, port, server, node, **tags):
        """
        Read data from UniReader server. Using XML RPC.

        :param host: Server host.
        :param port: Server port. Default 8080.
        :param server: Server name.
        :param node: Node name.
        :param tags: Tags dictionary.
            {'tag_name': 'tag_address', ...}
        :return: Tags dictionary with data.
        """
        tag_items = tags.items()
        addresses = [tag_addr for tag_name, tag_addr in tag_items]
        tag_names = [tag_name for tag_name, tag_addr in tag_items]

        try:
            # Create OPC client
            opc = xmlrpc.client.ServerProxy('http://%s:%d' % (host, port))
            values = opc.sources.ReadValuesAsStrings(node, server, *addresses)

            if not isinstance(values, (tuple, list)):
                # [NOTE] If one tag then return one value.
                # log_func.debug(u'UniReader. Прочитанные данные %s : %s' % (str(values), type(values)))
                values = (values, )

            if not values:
                log_func.warning(u'UniReader. Empty values: %s' % str(values))
                log_func.warning(u'UniReader. Check type <%s> uni_reader service node' % node)

            result = dict([(tag_name, values[i] if values else u'') for i, tag_name in enumerate(tag_names)])
            return result
        except:
            log_func.fatal(u'Error read server data <%s:%d / %s>' % (host, port, server))
            return dict([(tag_name, u'') for tag_name in tag_names])

    def readTag(self, host=None, port=DEFAULT_PORT, server=None, node=None,
                address=None, typecast=True):
        """
        Read data from UniReader server. Using XML RPC.

        :param host: Server host.
        :param port: Server port. Default 8080.
        :param server: Server name.
        :param node: Node name.
        :param address: Tag address.
        :param typecast: An attempt was made to automatically detect and convert the value type.
        :return: The read tag value as a string, or None on error.
        """
        values = self.readTags(host=host, port=port, server=server, node=node,
                               read_tag=address)
        if values and 'read_tag' in values:
            value = values['read_tag']
            if typecast and isinstance(value, str):
                try:
                    # Attempt to typecast
                    value = eval(value)
                except:
                    # The attempt failed. We believe that this is a string
                    pass
            return value
        return None
