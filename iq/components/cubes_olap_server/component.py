#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cubes OLAP Framework Server component.
"""

import os
import os.path

from ... import object

from . import spc
from . import cubes_olap_server_proto

from ...util import log_func
from ...util import file_func

__version__ = (0, 0, 0, 1)


class iqCubesOLAPServer(cubes_olap_server_proto.iqCubesOLAPServerProto, object.iqObject):
    """
    Cubes OLAP Framework Server component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        cubes_olap_server_proto.iqCubesOLAPServerProto.__init__(self)

        self.createChildren()

    def getDBPsp(self):
        """
        Database object passport.
        """
        return self.getAttribute('db')

    def getDB(self):
        """
        Database object.
        """
        if self._db is None:
            db_psp = self.getDBPsp()
            if db_psp:
                kernel = self.getKernel()
                self._db = kernel.createByPsp(psp=db_psp)
            else:
                log_func.warning(u'Database object not define in <%s>' % self.getName())
        return self._db

    def getSrvPath(self):
        """
        The folder where the OLAP server settings files are located.
        """
        srv_path = self.getAttribute('srv_path')
        if not srv_path:
            srv_path = os.path.join(cubes_olap_server_proto.DEFAULT_OLAP_SERVER_DIRNAME, self.getName())
        if srv_path and not os.path.exists(srv_path):
            # Create folder
            file_func.createDir(srv_path)
        return srv_path

    def getINIFileName(self):
        """
        Get settings INI filename.
        """
        if not self._ini_filename:
            ini_base_filename = self.getAttribute('ini_filename')
            srv_path = self.getSrvPath()
            self._ini_filename = os.path.join(srv_path if srv_path else os.path.join(cubes_olap_server_proto.DEFAULT_OLAP_SERVER_DIRNAME,
                                                                                     self.getName()),
                                              ini_base_filename if ini_base_filename else cubes_olap_server_proto.DEFAULT_INI_FILENAME)
        return self._ini_filename

    def getModelFileName(self):
        """
        Get model filename.
        """
        if not self._model_filename:
            model_base_filename = self.getAttribute('model_filename')
            srv_path = self.getSrvPath()
            self._model_filename = os.path.join(srv_path if srv_path else os.path.join(cubes_olap_server_proto.DEFAULT_OLAP_SERVER_DIRNAME,
                                                                                       self.getName()),
                                                model_base_filename if model_base_filename else cubes_olap_server_proto.DEFAULT_MODEL_FILENAME)
        return self._model_filename

    def getLogFileName(self):
        """
        Get log filename.
        """
        return self.getAttribute('log_filename')

    def getLogLevel(self):
        """
        Logging level.
        """
        return self.getAttribute('log_level')

    def getHost(self):
        """
        Server host.
        """
        return self.getAttribute('host')

    def getPort(self):
        """
        Server port.
        """
        return self.getAttribute('port')

    def isReload(self):
        """
        """
        return self.getAttribute('reload')

    def isPrettyPrint(self):
        """
        Demonstration purposes.
        """
        return self.getAttribute('prettyprint')

    def getAllowCorsOrigin(self):
        """
        Resource sharing header.
        Other related headers are also added, if this option is present.
        """
        return self.getAttribute('allow_cors_origin')

    def getExec(self):
        """
        OLAP server startup file.
        """
        return self.getAttribute('exec')

    def getCubes(self):
        """
        List of OLAP server cube objects.
        """
        return self.getChildren()


COMPONENT = iqCubesOLAPServer
