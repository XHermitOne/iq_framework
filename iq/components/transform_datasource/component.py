#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transformation table data component.
"""

import datetime
import pandas

from ... import object

from . import spc
from . import transform_datasource_proto

from ...util import log_func
from ...util import exec_func

__version__ = (0, 0, 1, 2)


class iqTransformDataSource(transform_datasource_proto.iqTransformDataSourceProto,
                            object.iqObject):
    """
    Transformation table data component class.
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
        transform_datasource_proto.iqTransformDataSourceProto.__init__(self, *args, **kwargs)

    def getTabDataSourcePsp(self):
        """
        Get table datasource object passport.

        :return: Table datasource object passport or None if error.
        """
        return self.getAttribute('tab_datasource')

    def getTabDataSource(self):
        """
        Get table datasource object.

        :return: Table datasource object or None if error.
        """
        psp = self.getTabDataSourcePsp()
        if psp:
            kernel = self.getKernel()
            return kernel.getObject(psp, register=True)
        else:
            log_func.warning(u'Not define table datasource in transform datasource <%s>' % self.getName())
        return None

    def transform(self, dataframe=None, **kwargs):
        """
        Transform DataFrame object.

        :param dataframe: DataFrame object.
            If not defined then get current DataFrame object.
        :param kwargs: Data retrieval context.
        :return: Transformed DataFrame object or None if error.
        """
        if dataframe is None:
            table_datasource = self.getTabDataSource()
            log_func.info(u'Get table datasource <%s> for transform' % table_datasource.getName())
            dataset = table_datasource.getDataset(**kwargs) if table_datasource else list()
            self.importData(data=dataset)
            dataframe = self.getDataFrame()

        try:
            if self.isAttributeValue('transform'):
                context = self.getContext()
                context.update(kwargs)
                context['pandas'] = pandas
                context['pd'] = pandas
                context['datetime'] = datetime
                context['dt'] = datetime
                context['DATAFRAME'] = dataframe
                function_body = self.getAttribute('transform')

                if not dataframe.empty:
                    # log_func.debug(u'Before transform DataFrame:')
                    # log_func.debug(str(dataframe.empty))
                    self._dataframe = exec_func.execTxtFunction(function=function_body,
                                                                context=context)
                    # log_func.debug(u'After transform DataFrame:')
                    # log_func.debug(str(self._dataframe))
                else:
                    log_func.warning(u'DataFrame for transform <%s> is empty' % self.getName())

                return self._dataframe
            return dataframe
        except:
            log_func.fatal(u'Error transform method in <%s>' % self.getName())

        return None

    def test(self):
        """
        Object test function.

        :return: True/False.
        """
        from . import view_transform_data_source_dialog

        return view_transform_data_source_dialog.viewTransforDataSourceDlg(parent=None,
                                                                           component=self)


COMPONENT = iqTransformDataSource
