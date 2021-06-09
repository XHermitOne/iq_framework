#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cubes OLAP Framework Server.

Sorces:
https://github.com/DataBrewery/cubes
Official:
http://cubes.databrewery.org/

Install:
pip3 install cubes
pip3 install cubes[all]

Run OLAP server:
slicer serve slicer.ini
or
~/.local/bin/slicer serve slicer.ini

Master data and analytic functions are available through the following queries :
- /cube/<name>/aggregate – aggregation of measures, provide summary, generate drilldown, slices and cubes, ...
- /cube/<name>/members/<dim> – list dimension items
- /cube/<name>/facts – list of facts inside the cell
- /cube/<name>/fact – single fact
- /cube/<name>/cell – cell description

Options:
- cut - cell specificatioon. For example: cut=date:2004,1|category:2|entity:12345
- drilldown - measurement to be "drilled". For example drilldown=date will give rows for each value
    next level of measurement date. You can explicitly specify the level for granularity in the form: dimension:level,
    such as: drilldown=date:month.
    To specify the hierarchy use  dimension@hierarchy as
    drilldown=date@ywd for implicit level or drilldown=date@ywd:week explicitly indicate the level.
- aggregates – list of aggregates for calculation. Shared with |.
    For example: aggergates=amount_sum|discount_avg|count
- measures – a list of measures for which their respective aggregates will be calculated (see below).
    Shared with |. For example: aggergates=proce|discount
- page - page number for pagination
- pagesize - page size for pagination
- order - list of attributes for order
- split – split cell, the same syntax as slice, defines a virtual binary (flag) dimension,
     which indicates whether the cell belongs to a split section (true) or not (false).
     The dimension attribute is named __within_split__.
     Refer to the backend you are using for more information,
     whether this feature is supported or not.
"""

import os.path

from . import olap_server_interface
from . import pivot_dataframe_manager

from ...util import file_func
from ...util import log_func
from ...util import ini_func
from ...util import sys_func
from ...util import str_func
from ...util import json_func

from ..virtual_spreadsheet import v_spreadsheet

__version__ = (0, 0, 0, 1)

DEFAULT_SLICER_EXEC = 'slicer'
ALTER_SLICER_EXEC = file_func.getNormalPath(os.path.join(file_func.getHomePath(),
                                                         '.local', 'bin', 'slicer'))

DEFAULT_INI_FILENAME = 'slicer.ini'
DEFAULT_MODEL_FILENAME = 'model.json'
START_COMMAND_FMT = '%s serve %s &'

DEFAULT_OLAP_SERVER_DIRNAME = file_func.getNormalPath(os.path.join(file_func.getProjectProfilePath(),
                                                                   'OLAP'))

LOG_LEVELS = ('info', 'debug', 'warn', 'error')

FULL_URL_PREFIX = 'http://'
OLAP_SERVER_URL_FMT = 'http://%s:%d/%s'
OLAP_SERVER_SUBURL_FMT = 'cube/%s/%s'


class iqCubesOLAPServerProto(olap_server_interface.iqOLAPServerInterface,
                             pivot_dataframe_manager.iqPivotDataFrameManager):
    """
    Cubes OLAP Framework server prototype class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        pivot_dataframe_manager.iqPivotDataFrameManager.__init__(self)

        # OLAP cubes database
        self._db = None

        # OLAP server settings filename
        self._ini_filename = None

        # OLAP server cube definition JSON filename
        self._model_filename = None

    def getExec(self):
        """
        OLAP server startup file.
        """
        return DEFAULT_SLICER_EXEC

    def getRunCommand(self):
        """
        Get OLAP server run command.
        """
        exec_file = self.getExec()
        ini_filename = self.getINIFileName()

        command = START_COMMAND_FMT % (exec_file, ini_filename)
        return command

    def run(self):
        """
        Run OLAP server.
        The settings file and model are saved when the server starts.

        :return: True/False.
        """
        if self.isRunning():
            # If the server is already running, then there is no need to start
            log_func.info(u'OLAP server <%s> already launched' % self.getName())
            return True

        self.saveINI()
        self.saveModel()

        run_command = self.getRunCommand()

        try:
            log_func.info(u'Run OLAP server command <%s>' % run_command)
            os.system(run_command)
            return True
        except:
            log_func.fatal(u'Error run OLAP server command <%s>' % run_command)
        return False

    def stop(self):
        """
        Stop OLAP server.

        :return: True/False.
        """
        log_func.warning(u'Not define stop method OLAP server in <%s>' % self.__class__.__name__)
        return False

    def isRunning(self):
        """
        Is the OLAP server running?

        :return: True/False.
        """
        exec_filename = self.getExec()
        log_func.info(u'Checking a running OLAP server using <%s>' % exec_filename)
        return sys_func.isActiveProcess(exec_filename)

    def getRequestURL(self, request=None):
        """
        Get the URL of the request to the OLAP server by its structural description.

        :return: Dictionary of query parameters to the OLAP server.
             If not specified, then it is taken from controls.
        """
        if request is None:
            log_func.warning(u'Request to OLAP server to get URL not defined')
            return None

        request_url = u''

        cube_name = request.get('cube', None)
        method_name = request.get('method', None)
        if cube_name and method_name:
            request_url = OLAP_SERVER_SUBURL_FMT % (cube_name, method_name)
        dimension_name = request.get('dimension', None)
        if dimension_name:
            request_url += '/%s' % dimension_name

        # Set params
        params = list()

        param = request.get('cut', None)
        if param:
            params.append('cut=' + param)
        param = request.get('drilldown', None)
        if param:
            params.append('drilldown=' + param)
        param = request.get('aggregates', None)
        if param:
            params.append('aggregates=' + param)
        param = request.get('measures', None)
        if param:
            params.append('measures=' + param)
        param = request.get('page', None)
        if param:
            params.append('page=' + param)
        param = request.get('pagesize', None)
        if param:
            params.append('pagesize=' + param)
        param = request.get('order', None)
        if param:
            params.append('order=' + param)
        param = request.get('split', None)
        if param:
            params.append('split=' + param)

        if params:
            params_url = '&'.join(params)
            request_url += '?%s' % params_url

        try:
            full_request_url = self._getRequestURL(request_url)
            return full_request_url
        except:
            log_func.fatal(u'Error getting full URL request to OLAP server <%s>' % self.getName())

        return request_url

    def _getRequestURL(self, request_url):
        """
        Receive a full request to receive data from the server by URL.

        :param request_url: URL of the request to the OLAP server.
        :return: Complete generated request.
        """
        url = OLAP_SERVER_URL_FMT % (self.getHost(), self.getPort(),
                                     request_url)
        if self.isPrettyPrint():
            url += '&prettyprint=true' if '?' in url else '?prettyprint=true'
        return url

    def getResponse(self, request_url):
        """
        Request to receive data from the server by URL.

        :param request_url: URL of the request to the OLAP server.
            Can be specified as a complete URL  (начинается с http://)
            never complete (/cube/...)
        :return: The requested data, or None on error.
        """
        url = self._getRequestURL(request_url) if not request_url.startswith(FULL_URL_PREFIX) else request_url
        log_func.debug(u'Specified JSON by URL <%s>' % url)
        return json_func.getJSONAsDictByURL(url)

    def getName(self):
        """
        Get object name.
        """
        return u''

    def getDBPsp(self):
        """
        Get database passport.
        """
        return None

    def getDB(self):
        """
        Get database object.
        """
        return self._db

    def getINIFileName(self):
        """
        Get settings INI filename.
        """
        return self._ini_filename

    def getModelFileName(self):
        """
        The name of the cube description file.
        """
        return self._model_filename

    def getLogFileName(self):
        """
        Get log filename.
        """
        return None

    def getLogLevel(self):
        """
        Logging level.
        """
        return None

    def getHost(self):
        """
        Get server host.
        """
        return None

    def getPort(self):
        """
        Get server port.
        """
        return None

    def isReload(self):
        """
        """
        return True

    def isPrettyPrint(self):
        """
        Demonstration purposes.
        """
        return True

    def getAllowCorsOrigin(self):
        """
        Resource sharing header.
        Other related headers are also added, if this option is present.
        """
        return '*'

    def _saveINI(self, ini_filename=None, rewrite=True):
        """
        Save the OLAP server configuration file.
        
        :param ini_filename: The full INI name of the OLAP server settings file.
             If not specified, then we take the file name from the object description.
        :param rewrite: Overwrite existing file?
        :return: True/False.
        """
        if ini_filename is None:
            ini_filename = self.getINIFileName()

        ini_dirname = os.path.dirname(ini_filename)
        if not os.path.exists(ini_dirname):
            file_func.createDir(ini_dirname)

        ini_content = dict(workspace=dict(),
                           server=dict(),
                           store=dict(type='sql'),
                           models=dict())

        log_filename = self.getLogFileName()
        if log_filename:
            ini_content['workspace']['log'] = log_filename
        log_level = self.getLogLevel()
        if log_level:
            ini_content['workspace']['log_level'] = log_level

        # Server
        host = self.getHost()
        if host:
            ini_content['server']['host'] = host
        port = self.getPort()
        if port:
            ini_content['server']['port'] = port
        reload = self.isReload()
        if reload:
            ini_content['server']['reload'] = reload
        prettyprint = self.isPrettyPrint()
        if prettyprint:
            ini_content['server']['prettyprint'] = prettyprint
        allow_cors_origin = self.getAllowCorsOrigin()
        if allow_cors_origin:
            ini_content['server']['allow_cors_origin'] = allow_cors_origin

        # Database
        db = self.getDB()
        if db:
            db_url = db.getDBUrl()
            ini_content['store']['url'] = db_url
        else:
            log_func.warning(u'Database of storage of OLAP table of cube is not defined <%s>' % self.getName())

        model_filename = self.getModelFileName()
        if model_filename:
            ini_content['models']['main'] = model_filename
        else:
            log_func.warning(u'OLAP server cube deployment file not defined <%s>' % self.getName())

        return ini_func.Dict2INI(ini_content, ini_filename, rewrite=rewrite)

    def saveINI(self, ini_filename=None, rewrite=True):
        """
        Save the OLAP server configuration file.
        The settings file and model are saved when the server starts.

        :param ini_filename: The full INI name of the OLAP server settings file.
             If not specified, then we take the file name from the object description.
        :param rewrite: Overwrite existing file?
        :return: True/False.
        """
        try:
            return self._saveINI(ini_filename=ini_filename, rewrite=rewrite)
        except:
            log_func.fatal(u'Error saving OLAP server configuration file <%s>' % ini_filename)
        return False

    def _saveModel(self, model_filename=None, rewrite=True):
        """
        Save the OLAP server cube description file.
        
        :param model_filename: The fully qualified JSON name of the OLAP server cube description file.
             If not specified, then we take the file name from the object description.
        :param rewrite: Overwrite existing file?
        :return: True/False.
        """
        if model_filename is None:
            model_filename = self.getModelFileName()

        json_content = dict(cubes=list(),
                            dimensions=list())

        # Filling cubes
        for cube in self.getCubes():
            cube_content = self._getModelCube(cube)
            json_content['cubes'].append(cube_content)

            dimensions = cube.getDimensions()
            for dimension in dimensions:
                dimension_content = self._getModelDimension(dimension)
                json_content['dimensions'].append(dimension_content)

        return json_func.saveDictAsJSON(model_filename, json_content, rewrite)

    def _getModelCube(self, cube):
        """
        Content of the cube model.

        :param cube: Cube object.
        :return: A dictionary of the contents of the model corresponding to the cube.
        """
        dimensions = cube.getDimensions()
        cube_content = dict(name=cube.getTableName(),
                            dimensions=[dimension.getName() for dimension in dimensions])

        label = cube.getLabel()
        if label:
            cube_content['label'] = label

        # Filling in the facts
        measures = cube.getMeasures()
        if measures:
            if 'measures' not in cube_content:
                cube_content['measures'] = list()
            for measure in measures:
                measure_content = self._getModelMeasure(measure)
                cube_content['measures'].append(measure_content)

        for dimension in dimensions:
            # Filling in measurements
            dimension_detail_tabname = dimension.getDetailTableName()
            if dimension_detail_tabname:
                dimension_detail_fldname = dimension.getDetailFieldName()
                if dimension_detail_fldname:
                    if 'joins' not in cube_content:
                        cube_content['joins'] = list()

                    # Configure communication
                    dimension_fld_name = dimension.getFieldName()
                    dimension_join = dict(master=dimension_fld_name,
                                          detail='%s.%s' % (dimension_detail_tabname,
                                                            dimension_detail_fldname))
                    cube_content['joins'].append(dimension_join)

            # Populating the mappings
            dimension_mapping = dimension.getMapping()
            if dimension_mapping:
                if 'mappings' not in cube_content:
                    cube_content['mappings'] = dict()
                dimension_name = dimension.getName()
                cube_content['mappings'][dimension_name] = dimension_mapping
            for dimension_level in dimension.getLevels():
                dimension_level_mapping = dimension_level.getMapping()
                if dimension_level_mapping:
                    if 'mappings' not in cube_content:
                        cube_content['mappings'] = dict()
                    dimension_name = dimension.getName()
                    mapping_key = '%s.%s' % (dimension_name, dimension_level.getName())
                    cube_content['mappings'][mapping_key] = dimension_level_mapping

        # Populating aggregations
        aggregates = cube.getAggregates()
        if aggregates:
            if 'aggregates' not in cube_content:
                cube_content['aggregates'] = list()
            for aggregate in aggregates:
                aggregate_content = self._getModelAggregate(aggregate)
                cube_content['aggregates'].append(aggregate_content)
        return cube_content

    def _getModelMeasure(self, measure):
        """
        The content of the measure / actual model

        :param measure: Measure object .
        :return: Dictionary of the contents of the model corresponding to the measure.
        """
        measure_content = dict(name=measure.getFieldName())
        measure_label = measure.getLabel()
        if measure_label:
            measure_content['label'] = measure_label
        return measure_content

    def _getModelAggregate(self, aggregate):
        """
        Content of the data aggregation model.

        :param aggregate: Aggregate object.
        :return: A dictionary of the contents of the model corresponding to the data aggregation.
        """
        aggregate_content = dict(name=aggregate.getName())
        aggregate_function = aggregate.getFunctionName()
        if aggregate_function:
            aggregate_content['function'] = aggregate_function
        aggregate_measure = aggregate.getMeasureName()
        if aggregate_measure:
            aggregate_content['measure'] = aggregate_measure
        aggregate_expression = aggregate.getExpressionCode()
        if aggregate_expression:
            aggregate_content['expression'] = aggregate_expression
        return aggregate_content

    def _getModelDimension(self, dimension):
        """
        Dimension model content.

        :param dimension: Dimension object.
        :return: A dictionary of the contents of the model corresponding to the dimension.
        """
        dimension_content = dict(name=dimension.getName())
        label = dimension.getLabel()
        if label:
            dimension_content['label'] = label
        dimension_attributes = dimension.getAdditionalAttributes()
        if dimension_attributes:
            dimension_content['attributes'] = dimension_attributes
        dimension_levels = dimension.getLevels()
        if dimension_levels:
            dimension_content['levels'] = [self._getModelDimensionLevel(level) for level in dimension_levels]
        dimension_hierarchies = dimension.getHierarchies()
        if dimension_hierarchies:
            dimension_content['hierarchies'] = [self._getModelDimensionHierarchy(hierarchy) for hierarchy in dimension_hierarchies]
            # By default, consider the first hierarchy
            dimension_content['default_hierarchy_name'] = dimension_hierarchies[0].getName()
        return dimension_content

    def _getModelDimensionLevel(self, level):
        """
        Content of the dimension level model.

        :param level: Level object.
        :return: A dictionary of the contents of the model corresponding to the dimension level.
        """
        level_content = dict(name=level.getName())
        level_attributes = level.getAdditionalAttributes()
        if level_attributes:
            level_content['attributes'] = level_attributes
        key = level.getKey()
        if key:
            level_content['key'] = key
        label_attribute = level.getLabelAttribute()
        log_func.debug(u'Label attribute <%s>' % label_attribute)
        if label_attribute:
            level_content['label_attribute'] = label_attribute
        return level_content

    def _getModelDimensionHierarchy(self, hierarchy):
        """
        Content of the dimension level hierarchy model.

        :param hierarchy: Hierarchy object.
        :return: A dictionary of the contents of the model corresponding to the hierarchy.
        """
        hierarchy_content = dict(name=hierarchy.getName())
        hierarchy_levels = hierarchy.getLevelNames()
        if hierarchy_levels:
            hierarchy_content['levels'] = hierarchy_levels
        return hierarchy_content

    def saveModel(self, model_filename=None, rewrite=True):
        """
        Save the OLAP server cube description file.
        The settings file and model are saved at startup server.

        :param model_filename: The fully qualified JSON name of the OLAP server cube description file.
             If not specified, then we take the file name from the object description.
        :param rewrite: Overwrite existing file?
        :return: True/False.
        """
        try:
            return self._saveModel(model_filename=model_filename, rewrite=rewrite)
        except:
            log_func.fatal(u'Error saving OLAP server cube description file <%s>' % model_filename)
        return False

    def getCubes(self):
        """
        List of OLAP server cube objects.
        """
        return list()

    def getCubesCount(self):
        """
        The number of OLAP server cubes.
        """
        return len(self.getCubes())

    def findCube(self, cube_name=None):
        """
        Find a cube object by its name.

        :param cube_name: The name of the cube. If not specified, then the first cube is simply taken.
        :return: A cube object, or None if no cube with that name was found.
        """
        cube = None
        if cube_name is None:
            cubes = self.getCubes()
            cube = cubes[0] if cubes else None
            if cube is None:
                log_func.warning(u'Cubes not define')
                return None
        else:
            find_cube = [cube for cube in self.getCubes() if cube.getName() == cube_name]
            cube = find_cube[0] if find_cube else None
        return cube

    def _prepareSpreadsheet(self, spreadsheet_manager):
        """
        Prepare the Spreadsheet structure for further filling.

        :param spreadsheet_manager: SpreadSheet structure control object.
        :return: True/False.
        """
        # Create workbook
        workbook = spreadsheet_manager.createWorkbook()
        # Create worksheet in workbook
        worksheet = workbook.createWorksheet()
        # Create styles
        styles = workbook.createStyles()
        # Append styles
        for default_style_attr in v_spreadsheet.DEFAULT_STYLES:
            style = styles.createStyle()
            style_id = default_style_attr.get('ID', None)
            if style_id:
                style.setID(style_id)
            # log_func.debug(u'1. Style %s' % str(style.get_attributes()))
            style.update_attributes(default_style_attr)
            # log_func.debug(u'2. Style %s' % str(style.get_attributes()))
        return True

    def _createSpreadsheetTable(self, spreadsheet_manager, worksheet, row_count, col_count):
        """
        Create SpreadSheet table.
        
        :param spreadsheet_manager: SpreadSheet structure control object.
        :param worksheet: Worksheet object.
        :param row_count: Number of rows.
        :param col_count: Number of columns.
        :return: Table object.
        """
        # Create table
        table = worksheet.createTable()
        # Create columns
        spreadsheet_manager.createDefaultColumns(table, count=col_count)
        # Create rows
        spreadsheet_manager.createDefaultRows(table, count=row_count)
        return table

    def toPivotDataFrame(self, json_dict, row_dimension=None, col_dimension=None, debug=True):
        """
        Preparing data for a pivot table.
        Data manipulation is done using the pandas library.

        :param json_dict: Results of a query to the OLAP server as a JSON dictionary.
        :param row_dimension: Measurement / measurements to be displayed line by line.
        :param col_dimension: Measurement / Measurements to be displayed column by column.
        :param debug: Output debug information to the console?
        :return: pandas.DataFrame object.
        """
        # attributes = json_dict.get('attributes', list())
        aggregates = json_dict.get('aggregates', list())
        # levels = json_dict.get('levels', dict())
        cells = json_dict.get('cells', list())

        row_dimension_list = list(row_dimension) if row_dimension else list()
        col_dimension_list = list(col_dimension) if col_dimension else list()
        col_names = row_dimension_list + col_dimension_list + aggregates
        rows = [[cell.get(col_name, None) for col_name in col_names] for cell in cells]
        data_frame = None
        try:
            # Create table
            data_frame = self.createDataFrame(rows, column_names=col_names)
            # Setting dimension indices
            data_frame = self.setPivotDimensions(row_dimension=row_dimension, col_dimension=col_dimension)
            # Replace NaN with 0
            data_frame = self.fillNaNValue(0)
            # data_frame = self.aggregate_dimensions('sum')
        except:
            log_func.error(u'Pivot table filling error: ')
            log_func.error(str(data_frame))
            log_func.fatal()
            return None

        if debug:
            log_func.debug(u'')
            log_func.debug(u'Row dimensions: %s' % str(row_dimension))
            log_func.debug(u'Column dimensions: %s' % str(col_dimension))
            log_func.debug(u'Pivot table:')
            log_func.debug('\n' + str(data_frame))
        return data_frame

    def normPivotDataFrame(self, dataframe, cube=None, row_dimension=None, col_dimension=None):
        """
        Normalize the pivot table.

        :param dataframe: Pivot table pandas.DataFrame object.
        :param cube: Cube object. If not specified, then the first cube in the list is taken.
        :param row_dimension: Measurement / measurements to be displayed line by line.
        :param col_dimension: Measurement / Measurements to be displayed column by column.
        :return: pandas.DataFrame object.
        """
        if cube is None:
            cubes = self.getCubes()
            cube = cubes[0] if cubes else None
        if cube is None:
            log_func.warning(u'Cube not defined to normalize pivot table data')
            return dataframe

        if row_dimension:
            # Checking string dimensions
            for row in dataframe.index:
                print(row)
                for name in row_dimension:
                    if '.' in name:
                        dimension_name, level_name = name.split('.')
                        dimension = cube.findDimension(dimension_name)
                        level = dimension.findLevel(level_name) if dimension else None
                        normal_data = level.getNormal()
                        if normal_data:
                            print(normal_data)

        return dataframe

    def pivotToSpreadsheet(self, json_dict=None, cube=None, dataframe=None):
        """
        Converting OLAP server query results to structure pivot table in spreadSheet format.

        :param json_dict: Results of a query to the OLAP server as a JSON dictionary.
        :param cube: Cube. If not specified, then the first is taken.
        :param dataframe: pandas.DataFrame object.
            If not specified, then the internal object is taken.
        :return: Dictionary of the SpreadSheet structure.
        """
        try:
            return self._toPivotSpreadsheet(json_dict=json_dict, cube=cube,
                                            dataframe=dataframe)
        except:
            log_func.fatal(u'Error converting query results to OLAP server to Pivot SpreadSheet structure')
        return None

    def _toPivotSpreadsheet(self, json_dict, cube=None, dataframe=None):
        """
        Converting OLAP Server Query Results to Structure
        Pivot Table in SpreadSheet forma

        :param json_dict: Results of a query to the OLAP server as a JSON dictionary.
        :param cube: Cube. If not specified, then the first is taken.
        :param dataframe: pandas.DataFrame object.
            If not specified, then the internal object is taken.
        :return: Dictionary of the SpreadSheet structure.
        """
        if cube is None:
            cubes = self.getCubes()
            cube = cubes[0] if cubes else None
            if cube is None:
                log_func.warning(u'Convert to SpreadSheet structure. Cube not defined')
                return None

        if dataframe is None:
            dataframe = self.getPivotDataFrame()

        # SpreadSheet structure control object
        spreadsheet_manager = v_spreadsheet.iqVSpreadsheet()
        self._prepareSpreadsheet(spreadsheet_manager)
        worksheet = spreadsheet_manager.getWorkbook().getWorksheetIdx()

        # Create table
        row_count, col_count = self.getPivotTableSize(dataframe)
        log_func.debug(u'Pivot table size [%d x %d]' % (row_count, col_count))
        table = self._createSpreadsheetTable(spreadsheet_manager, worksheet, row_count, col_count)

        # Filling the header
        self._createPivotSpreadsheetHeader(table, json_dict, cube, dataframe=dataframe)
        # Create rows
        self._createPivotSpreadsheetDetail(table, json_dict, dataframe=dataframe)
        # Filling the footer
        self._createPivotSpreadsheetFooter(table, json_dict, dataframe=dataframe)

        return spreadsheet_manager.getData()

    def _createPivotSpreadsheetHeader(self, table, json_dict, cube, dataframe=None):
        """
        Create the data header of the Pivot SpreadSheet structure.

        :param table: Table object.
        :param json_dict: Results of a query to the OLAP server as a JSON dictionary.
        :param cube: Cube object.
        :param dataframe: pandas.DataFrame object.
            If not specified, then the internal object is taken.
        :return: True/False
        """
        if dataframe is None:
            dataframe = self.getPivotDataFrame()

        # Filling columns by levels
        for i_col_level in range(dataframe.columns.nlevels):
            col_level = dataframe.columns.get_level_values(i_col_level)
            # Filling in a part of string dimensions
            for i, level_name in enumerate(col_level.names):
                cell = table.getCell(i_col_level + 1, i + 1)
                cell.setStyleID('HEADER')

                label = u''
                if level_name:
                    label = self._getPivotLabel(cube, level_name)
                cell.setValue(label)

            # Fill unused header cells
            col_label_count = len(col_level.names)
            not_use_col_count = len(dataframe.index.names) - col_label_count
            for i in range(not_use_col_count):
                cell = table.getCell(i_col_level + 1,
                                     col_label_count + i + 1)
                cell.setStyleID('HEADER')
                cell.setValue(u'')

            # Filling in a part of a columnar dimension
            prev_label = None
            i_span = 0
            for i, col_name in enumerate(col_level.to_list()):
                cell = table.getCell(i_col_level + 1,
                                     dataframe.index.nlevels + i + 1)
                cell.setStyleID('HEADER')
                label = self._getPivotLabel(cube, col_name)
                if label != prev_label:
                    cell.setValue(label)

                if prev_label is None or prev_label == label:
                    i_span += 1
                elif i_span > 1:
                    row = i_col_level + 1
                    col = dataframe.index.nlevels + i - i_span + 1

                    merge_cell = table.getCell(row, col)
                    merge_cell.setMerge(i_span - 1, 0)
                    i_span = 1
                prev_label = label
            if i_span > 1:
                row = i_col_level + 1
                col = dataframe.index.nlevels + len(col_level.to_list()) - i_span + 1

                merge_cell = table.getCell(row, col)
                merge_cell.setMerge(i_span - 1, 0)

        # Row dimension column label
        for i, level_name in enumerate(dataframe.index.names):
            cell = table.getCell(dataframe.columns.nlevels + 1,
                                 i + 1)
            cell.setStyleID('GROUP')
            label = u''
            if level_name:
                label = self._getPivotLabel(cube, level_name)
            cell.setValue(label)
        row_level_count = len(dataframe.index.names)
        for i in range(len(dataframe.columns)):
            cell = table.getCell(dataframe.columns.nlevels + 1,
                                 row_level_count + i + 1)
            cell.setStyleID('GROUP')
            cell.setValue(u'')

        return True

    def _getPivotLabel(self, cube, name):
        """
        Get cell label by name.

        :param cube: Cube object.
        :param name: Dimension/aggregation name .
        :return: Text or blank line if not possible to determine.
        """
        label = u''
        try:
            if not name:
                return label

            if str_func.isLATText(name):
                # Level name defined
                if '.' in name:
                    # This is the level of measurement
                    dimension_name, level_name = name.split('.')
                    dimension = cube.findDimension(dimension_name)
                    level = dimension.findLevel(level_name) if dimension else None
                    label = level.getLabel() if level else name
                else:
                    # It's just a measurement
                    dimension = cube.findChild(name)
                    label = dimension.getLabel() if dimension else name
            else:
                label = str(name)
        except:
            log_func.fatal(u'Dimension/aggregation label definition error <%s>' % str(name))
        return label

    def _createPivotSpreadsheetDetail(self, table, json_dict, dataframe=None):
        """
        Create the body of the tabular data part of the Pivot SpreadSheet structure.

        :param table: Table object.
        :param json_dict: Results of a query to the OLAP server as a JSON dictionary.
        :param dataframe: pandas.DataFrame object.
            If not specified, then the internal object is taken.
        :return: True/False
        """
        if dataframe is None:
            dataframe = self.getPivotDataFrame()

        header_row_count = dataframe.columns.nlevels + 1 if any(dataframe.index.names) else 0
        records = list(dataframe.to_records())
        prev_values = [None] * dataframe.index.nlevels
        i_span = [0] * dataframe.index.nlevels
        for i, record in enumerate(records):
            for i_col in range(len(record)):
                value = record[i_col]
                cell = table.getCell(header_row_count + i + 1,
                                     i_col + 1)
                if i_col >= dataframe.index.nlevels:
                    # Data
                    cell.setStyleID('CELL')
                else:
                    # Row measurement level columns
                    cell.setStyleID('GROUP')

                    if prev_values[i_col] is None or prev_values[i_col] == value:
                        i_span[i_col] = i_span[i_col] + 1
                    elif i_span[i_col] > 1:
                        row = header_row_count + i + 1 - i_span[i_col]
                        col = i_col + 1

                        merge_cell = table.getCell(row, col)
                        merge_cell.setMerge(0, i_span[i_col] - 1)
                        i_span[i_col] = 1
                    prev_values[i_col] = value
                cell.setValue(value)
        for i_col in range(dataframe.index.nlevels):
            if i_span[i_col] > 1:
                row = header_row_count + len(records) + 1 - i_span[i_col]
                col = i_col + 1

                merge_cell = table.getCell(row, col)
                merge_cell.setMerge(0, i_span[i_col] - 1)
        return True

    def _createPivotSpreadsheetFooter(self, table, json_dict, dataframe=None):
        """
        Create a footer/summary row of data for the Pivot SpreadSheet structure.

        :param table: Table object.
        :param json_dict: Results of a query to the OLAP server as a JSON dictionary.
        :param dataframe: pandas.DataFrame object.
            If not specified, then the internal object is taken.
        :return: True/False
        """
        if dataframe is None:
            dataframe = self.getPivotDataFrame()

        header_row_count = dataframe.columns.nlevels + 1 if any(dataframe.index.names) else 0
        records = list(dataframe.to_records())
        for i, record in enumerate(records):
            for i_col in range(len(record)):
                cell = table.getCell(header_row_count + i + 1,
                                     i_col + 1)
                # Total rows are determined by the value of the first column in the row
                if record[0] == pivot_dataframe_manager.TOTAL_LABEL:
                    # Data
                    cell.setStyleID('FOOTER')
        return True
