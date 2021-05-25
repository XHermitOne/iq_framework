#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Common interface for all OLAP servers.
"""

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqOLAPServerInterface:
    """
    Common interface for all OLAP servers.
    """
    def run(self):
        """
        Run server.

        :return: True/False.
        """
        log_func.warning(u'Not define run method OLAP server in <%s>' % self.__class__.__name__)
        return False

    def stop(self):
        """
        Stop server.

        :return: True/False.
        """
        log_func.warning(u'Not define stop method OLAP server in <%s>' % self.__class__.__name__)
        return False

    def isRunning(self):
        """
        Is the OLAP server running?

        :return: True/False.
        """
        log_func.warning(u'Not define isRunning method OLAP server in <%s>' % self.__class__.__name__)
        return False

    def restart(self):
        """
        Restart OLAP server.

        :return: True/False.
        """
        self.stop()
        return self.run()

    def getResponse(self, *args, **kwargs):
        """
        Request to receive data from the server.
        The function is too general.
        Therefore, its implementation must handle various requests in
        depending on the incoming data.

        :return: The requested data, or None on error.
        """
        log_func.warning(u'Not define getResponse method OLAP server in <%s>' % self.__class__.__name__)
        return None
