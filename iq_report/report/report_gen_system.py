#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report generator system functions module.

The keys of the query table can be:
    '__variables__': Report variables dictionary,
    '__coord_fill__': Dictionary of coordinate replacements,
    '__sql__': SQL query table,
        The SQL expression is specified without the SQL_SIGNATURE signature.
        As an SQL expression like <SELECT>,
    '__fields__': A list of field descriptions for the query table,
    '__data__': List of query table entries,

All these keys are processed during the report generation process.
"""

import os
import os.path
import re
import shutil
import sqlalchemy

from iq.util import log_func
from iq.util import exec_func
from iq.util import file_func
from iq.util import res_func
from iq.util import str_func
from iq.util import txtgen_func

from iq.dialog import dlg_func

from . import report_template

__version__ = (0, 0, 0, 1)

DEFAULT_REP_TMPL_FILE = os.path.join(os.path.dirname(__file__), 'new_report_template.ods')

OFFICE_OPEN_CMD_FORMAT = 'libreoffice %s'

ODS_TEMPLATE_EXT = '.ods'
XLS_TEMPLATE_EXT = '.xls'
XML_TEMPLATE_EXT = '.xml'
DEFAULT_TEMPLATE_EXT = ODS_TEMPLATE_EXT
DEFAULT_REPORT_TEMPLATE_EXT = '.rprt'

DEFAULT_REPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                                  'reports'))

# Report bend values signatures (Length 4 symbol)
DB_URL_SIGNATURE = 'URL:'
SQL_SIGNATURE = 'SQL:'
CODE_SIGNATURE = 'PRG:'
PY_SIGNATURE = 'PY:'


class iqReportGeneratorSystem(object):
    """
    Reporting system class. Abstract class.
    """
    def __init__(self, report=None, parent=None):
        """
        Constructor.

        :param report: Report template.
        :param parent: Parent window.
        """
        # Report template
        self._report_template = report
        # Query table
        self._query_table = None

        # Parent window
        self._parent_window = parent

        # # Preview
        # self.PrintPreview = None

    def getReportDir(self):
        """
        Get report folder.
        """
        return DEFAULT_REPORT_DIR

    def getProfileDir(self):
        """
        Get profile path.
        """
        return file_func.getProjectProfilePath()

    def getGeneratorType(self):
        """
        Type of reporting system.
        """
        my_generator_type = self._report_template.get('generator', None) if self._report_template else None
        if my_generator_type is None:
            log_func.error(u'Failed to determine the type of reporting system in <%s>' % self.__class__.__name__)
        elif isinstance(my_generator_type, str):
            my_generator_type = my_generator_type.lower()
        return my_generator_type

    def sameGeneratorType(self, generator_type):
        """
        Check for the same type of reporting system as specified.

        :param generator_type: Type of reporting system.
            The type is specified by the template source file extension.
            As '.ods', '.xml', '.xls' etc.
        :return: True/False
        """
        my_generator_type = self.getGeneratorType()
        return my_generator_type == generator_type.lower()

    def getReportDescription(self):
        """
        Get report description.

        :return: The description of the report or
            its name if the description is not defined.
        """
        description = u''
        if self._report_template:
            description = self._report_template.get('description', self._report_template.get('name', u''))
        return description

    def setParent(self, parent):
        """
        Set parent window.
        """
        self._parent_window = parent
        
    def getParent(self):
        """
        Get parent window.
        """
        return self._parent_window
        
    def reloadRepData(self, tmpl_filename=None):
        """
        Reload report data.

        :param tmpl_filename: Report template filename.
        """
        self._report_template = res_func.loadRuntimeResource(tmpl_filename)
        
    def setRepData(self, report):
        """
        Set report template data.
        """
        self._report_template = report

    def selectAction(self, report=None, *args, **kwargs):
        """
        Start report generation and then select an action.

        :param report: Report template data.
        """
        return

    def preview(self, report=None, *args, **kwargs):
        """
        Preview report.

        :param report: Report template data.
        """
        return

    def print(self, report=None, *args, **kwargs):
        """
        Print report.

        :param report: Report template data.
        """
        return 

    def setPageSetup(self):
        """
        Set page setup.
        """
        return

    def convert(self, report=None, to_filename=None, *args, **kwargs):
        """
        Convert report.

        :param report: Report template data.
        :param to_filename: Destination report filename.
        """
        return

    def export(self, report=None, to_filename=None, *args, **kwargs):
        """
        Export report.

        :param report: Report template data.
        :param to_filename: Destination report filename.
        """
        return self.convert(report, to_filename)

    def createNew(self, dst_path=None):
        """
        Create new report.

        :param dst_path: Destination report folder path.
        """
        return self.createNewByOffice(dst_path)
        
    def createNewByOffice(self, dst_path=None):
        """
        Create a new report using LibreOffice Calc.

        :param dst_path: Destination report folder path.
        """
        try:
            src_filename = DEFAULT_REP_TMPL_FILE
            new_filename = dlg_func.getTextEntryDlg(self._parent_window,
                                                    u'Create new',
                                                    u'Enter a file name for the report template')
            if os.path.splitext(new_filename)[1] != '.ods':
                new_filename += '.ods'

            if dst_path is None:
                # It is necessary to determine the resulting path
                dst_path = dlg_func.getDirDlg(self._parent_window,
                                              u'Report folder')
                if not dst_path:
                    dst_path = os.getcwd()

            dst_filename = os.path.join(dst_path, new_filename)
            if os.path.exists(dst_filename):
                if dlg_func.openAskBox(u'Rewrite existing file?'):
                    shutil.copyfile(src_filename, dst_filename)
            else:
                shutil.copyfile(src_filename, dst_filename)

            cmd = OFFICE_OPEN_CMD_FORMAT % dst_filename
            log_func.debug(u'Command <%s>' % str_func.toUnicode(cmd))
            os.system(cmd)

            return True
        except:
            log_func.fatal(u'Error create new report template by LibreOffice Calc')

    def edit(self, report=None):
        """
        Edit report.

        :param report: Report template data.
        """
        return

    def update(self, tmpl_filename=None):
        """
        Update report template.

        :param tmpl_filename: Report template filename.
            If None then select this file.
        :return: Report template filename or None if error.
        """
        try:
            return self._update(tmpl_filename)
        except:
            log_func.fatal(u'Error update report template <%s>' % tmpl_filename)
        return None

    def _update(self, tmpl_filename=None):
        """
        Обновить шаблон отчета в системе генератора отчетов.

        :param tmpl_filename: Report template filename.
            If None then select this file.
        :return: Report template filename or None if error.
        """
        if tmpl_filename is None:
            filename = dlg_func.getFileDlg(parent=self._parent_window,
                                           title=u'Select report template:',
                                           wildcard_filter=u'Open document spreadsheet ODF (*.ods)|*.ods|Microsoft Excel 2003 XML (*.xml)|*.xml',
                                           default_path=self.getReportDir())
        else:
            filename = os.path.abspath(os.path.normpath(tmpl_filename))

        if os.path.isfile(filename):
            log_func.info(u'Start convert <%s>' % filename)
            tmpl_filename = None
            template = None
            if os.path.exists(os.path.splitext(filename)[0] + DEFAULT_TEMPLATE_EXT):
                tmpl_filename = os.path.splitext(filename)[0] + DEFAULT_TEMPLATE_EXT
                template = report_template.iqODSReportTemplate()
            elif os.path.exists(os.path.splitext(filename)[0] + ODS_TEMPLATE_EXT):
                tmpl_filename = os.path.splitext(filename)[0] + ODS_TEMPLATE_EXT
                template = report_template.iqODSReportTemplate()
            elif os.path.exists(os.path.splitext(filename)[0] + XLS_TEMPLATE_EXT):
                tmpl_filename = os.path.splitext(filename)[0] + XLS_TEMPLATE_EXT
                template = report_template.iqXLSReportTemplate()
            elif os.path.exists(os.path.splitext(filename)[0] + XML_TEMPLATE_EXT):
                tmpl_filename = os.path.splitext(filename)[0] + XML_TEMPLATE_EXT
                template = report_template.iqlXMLSpreadSheetReportTemplate()
            else:
                log_func.error(u'Report template not found <%s>' % filename)

            new_filename = None
            if template:
                rep_template = template.read(tmpl_filename)
                new_filename = os.path.splitext(filename)[0]+DEFAULT_REPORT_TEMPLATE_EXT
                res_func.saveResourcePickle(new_filename, rep_template)
            log_func.info(u'End convert')
            return new_filename
        else:
            log_func.error(u'Report template file not found <%s>' % filename)
        return None
   
    def openModule(self, tmpl_filename=None):
        """
        Open report module in editor.
        """
        if tmpl_filename is None:
            log_func.error(u'Report template file not defined')

        module_file = os.path.abspath(os.path.splitext(tmpl_filename)[0]+'.py')
        if os.path.exists(module_file):
            try:
                self._parent_window.GetParent().ide.OpenFile(module_file)
            except:
                log_func.fatal(u'Error open report module <%s>' % module_file)
        else:
            dlg_func.openErrBox(u'Report module file not found <%s>' % module_file)
        
    def generate(self, report=None, db_url=None, sql=None, stylelib=None, vars=None, *args, **kwargs):
        """
        Run report generator.

        :param report: Report template.
        :param db_url: Connection string as url.
            For example:
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: SQL query.
        :param stylelib: Style library.
        :param vars: Report variables dictionary.
        :return: Generated report data or None if error.
        """
        return None

    def generateReport(self, report=None, *args, **kwargs):
        """
        Generate report.

        :param report: Report template.
        :return: Generated report data or None if error.
        """
        return None

    def initRepTemplate(self, report, query_table=None):
        """
        Read report template data.

        :param report: Report temlate data.
        :param query_table: Query table.
        """
        # 1. Report template data
        self._report_template = report
        # 2. Query table
        self._query_table = query_table

        # 3. Adjust the template for normal processing by the generator
        res = res_func.loadRuntimeResource(res_func.icGetTabResFileName())
        self._report_template = self.RepSQLObj2SQLite(self._report_template, res)

        # 5. Correction of database and query parameters
        # self._report_template['data_source'] = ic_exec.ExecuteMethod(self._report_template['data_source'], self)
        # self._report_template['query'] = ic_exec.ExecuteMethod(self._report_template['query'], self)

        # Checking if a query function returns an SQL query
        # if type(self._report_template['query'])==type(''):
        #     self._report_template['query']=ic.db.tabrestr.icQueryTxtSQLObj2SQLite(self._report_template['query'],\
        #         ic.utils.util.readAndEvalFile(ic.utils.resource.icGetTabResFileName()))

    def _getSQLQueryTable(self, report, db_url=None, sql=None):
        """
        Get query table.

        :param report: Report template data.
        :param db_url: Connection string as url.
            For example:
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: SQL query text.
        :return: Query table dictionary:
            {'__fields__': field_name_list, '__data__': table_data}
        """
        result = None

        db_connection = None
        try:
            if not db_url:
                data_source = report['data_source']

                if not data_source:
                    log_func.error(u'Report data source not defined')
                    return {'__fields__': list(), '__data__': list()}

                signature = data_source[:4].upper()
                if signature != DB_URL_SIGNATURE:
                    log_func.error('Not support DB type <%s>' % signature)
                    return result
                # DB is set using standard DB URL
                db_url = data_source[4:].lower().strip()

            log_func.info(u'DB URL <%s>' % db_url)

            db_connection = sqlalchemy.create_engine(db_url)
            log_func.info(u'SQL <%s>' % str_func.toUnicode(sql, 'utf-8'))
            sql_result = db_connection.execute(sql)
            rows = sql_result.fetchall()
            cols = rows[0].keys() if rows else []

            db_connection.dispose()
            db_connection = None

            result = {'__fields__': cols, '__data__': list(rows)}
            return result
        except:
            if db_connection:
                db_connection.dispose()

            log_func.fatal(u'Error defining SQL query table <%s>.' % sql)
        return None

    def _isQueryFunc(self, query):
        """
        Determine the submitted request as a function?

        :param query: Query text.
        :return: True/False.
        """
        return query and isinstance(query, str) and query.startswith(PY_SIGNATURE)

    def _execQueryFunc(self, query, vars=None):
        """
        Get a request from a function.

        :param query: Query text.
        :param vars: External variables.
        :return: Query in internal format.
        """
        # Clear signature
        func = query.replace(PY_SIGNATURE, '').strip()
        var_names = vars.keys() if vars else None
        log_func.debug(u'Execute function: <%s>. External variables %s' % (func, var_names))
        return exec_func.execTxtFunction(func, context=vars)

    def _isEmptyQueryTbl(self, query_tbl):
        """
        Is empty query table?.

        :param query_tbl: Query table.
        :return: True - empty query table / False - no.
        """
        if not query_tbl:
            return True
        # Exists variables?
        elif isinstance(query_tbl, dict) and '__variables__' in query_tbl and query_tbl['__variables__']:
            return False
        # Exists coordinate filling?
        elif isinstance(query_tbl, dict) and '__coord_fill__' in query_tbl and query_tbl['__coord_fill__']:
            return False
        # Exists table data?
        elif isinstance(query_tbl, dict) and '__data__' in query_tbl and query_tbl['__data__']:
            return False
        return True

    def createEmptyQueryTbl(self):
        """
        Create empty query table.

        :return: Query table dictionary:
            {'__fields__': field_name_list, '__data__': table_data}
        """
        return {'__fields__': (), '__data__': []}

    def getQueryTbl(self, report, db_url=None, sql=None, *args, **kwargs):
        """
        Get query table.

        :param report: Report template data.
        :param db_url: Connection string as url.
            For example:
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: SQL query.
            At the beginning of the SQL query should be a signature:
            <SQL:> - SQL query text
            <PY:> -  SQL query text returned Python function.
            <PRG:> - SQL query text returned Python function.
        :return: Query table dictionary:
            {'__fields__': field_name_list, '__data__': table_data}
        """
        query = None
        try:
            if sql:
                query = sql
            else:
                # Case when a query function returns a table
                if isinstance(report['query'], dict):
                    return report['query']
                elif self._isQueryFunc(report['query']):
                    variables = kwargs.get('variables', None)
                    query = self._execQueryFunc(report['query'], vars=variables)

                    if isinstance(query, dict):
                        if '__sql__' in query:
                            dataset_dict = self._getSQLQueryTable(report=report,
                                                                  db_url=db_url,
                                                                  sql=query['__sql__'])
                            if isinstance(dataset_dict, dict):
                                query.update(dataset_dict)
                        return query
                else:
                    query = report['query']
                # Query not defined
                if query is None:
                    log_func.error(u'Query not defined')
                    return None

                if query.startswith(SQL_SIGNATURE):
                    # SQL expression
                    query = query.replace(SQL_SIGNATURE, u'').strip()
                elif query.startswith(CODE_SIGNATURE):
                    # Python function
                    query = exec_func.execTxtFunction(query.replace(CODE_SIGNATURE, u'').strip())
                elif query.startswith(PY_SIGNATURE):
                    # Python
                    query = exec_func.execTxtFunction(query.replace(PY_SIGNATURE, u'').strip())
                else:
                    log_func.error(u'Not defined query signature <%s>' % query)
                    return None
                # The request can be parameterized by variables passed explicitly.
                # Therefore, it is necessary to generate
                if kwargs:
                    try:
                        # For replacements, use another generator
                        query_txt = query.replace(u'[&', u'{{ ').replace(u'&]', u' }}')
                        query = txtgen_func.generate(query_txt, kwargs)
                    except:
                        log_func.fatal(u'Error transform query\n<%s>\nfor report query table' % str(query))

            query_tbl = None
            if not self._query_table:
                # SQL expression
                query_tbl = self._getSQLQueryTable(report, db_url=db_url, sql=query)
            else:
                if isinstance(self._query_table, str):
                    if self._query_table[:4].upper() == SQL_SIGNATURE:
                        query_tbl = self._getSQLQueryTable(report, sql=self._query_table[4:].strip())
                    else:
                        log_func.error(u'Unsupported query type <%s>' % self._query_table)

                elif isinstance(self._query_table, dict):
                    query_tbl = self._query_table
                else:
                    log_func.error(u'Unsupported query type <%s>' % type(self._query_table))
            return query_tbl
        except:
            log_func.fatal(u'Error query table <%s>.' % query)
        return None

    # def RepSQLObj2SQLite(self, report, res_table):
    #     """
    #     Преобразование имен в шаблоне отчета в контексте SQLObject в имена в
    #         контексте sqlite.
    #
    #     :param report: Щаблон отчета.
    #     :param res_table: Ресурсное описание таблиц.
    #     """
    #     try:
    #         rep = report
    #         # Для корректной обработки имен полей и таблиц они д.б.
    #         # отсортированны по убыванию длин имен классов данных
    #         data_class_names = res_table.keys()
    #         data_class_names.sort()
    #         data_class_names.reverse()
    #
    #         # Обработка шаблона отчета
    #         # 1. Верхний и нижний колонтитулы
    #         # Перебор ячеек
    #         for row in rep['upper']:
    #             for cell in row:
    #                 if cell:
    #                     # Перебор классов
    #                     for data_class_name in data_class_names:
    #                         cell['value'] = ic.db.tabrestr.icNamesSQLObj2SQLite(cell['value'], data_class_name,
    #                                                                             res_table[data_class_name]['scheme'])
    #         # Перебор ячеек
    #         for row in rep['under']:
    #             for cell in row:
    #                 if cell:
    #                     # Перебор классов
    #                     for data_class_name in data_class_names:
    #                         cell['value'] = ic.db.tabrestr.icNamesSQLObj2SQLite(cell['value'], data_class_name,
    #                                                                             res_table[data_class_name]['scheme'])
    #         # 2. Лист шаблона
    #         # Перебор ячеек
    #         for row in rep['sheet']:
    #             for cell in row:
    #                 if cell:
    #                     # Перебор классов
    #                     for data_class_name in data_class_names:
    #                         cell['value'] = ic.db.tabrestr.icNamesSQLObj2SQLite(cell['value'], data_class_name,
    #                                                                             res_table[data_class_name]['scheme'])
    #         # 3. Описание групп
    #         for grp in rep['groups']:
    #             for data_class_name in data_class_names:
    #                 grp['field'] = ic.db.tabrestr.icNamesSQLObj2SQLite(grp['field'], data_class_name,
    #                                                                    res_table[data_class_name]['scheme'])
    #
    #         return rep
    #     except:
    #         return report

    def previewResult(self, report_data=None):
        """
        Preview.

        :param report_data: Generated report data.
        """
        return

    def printResult(self, report_data=None):
        """
        Print.

        :param report_data: Generated report data.
        """
        return

    def convertResult(self, report_data=None, to_filename=None):
        """
        Convert.

        :param report_data: Generated report data.
        :param to_filename: Destination report filename.
        """
        return

    def save(self, report_data=None):
        """
        Save generated report data to file.

        :param report_data: Generated report data.
        :return: Destination report data filename or None if error.
        """
        return None
