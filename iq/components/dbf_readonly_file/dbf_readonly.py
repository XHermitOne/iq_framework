#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DBF readonly file manager.
"""

import os.path

from ..dbf_file import dbf

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqDBFReadOnlyFile(dbf.iqDBFFileProto):
    """
    *.DBF readonly file class.
    Requirement <dbfread> library. [https://github.com/olemb/dbfread/]
    """
    def __init__(self, dbf_filename=None, encoding=dbf.DEFAULT_DBF_ENCODING):
        """
        Constructor.

        :param dbf_filename: DBF filename.
        :param encoding: DBF file code page.
        """
        dbf.iqDBFFileProto.__init__(self, dbf_filename)

        self.encoding = encoding

        self._dbf = None        # DBF object
        self._cur_rec_no = -1   # Current record number
        self._rec_count = -1    # Record number

    def openDBF(self, dbf_filename=None, encoding=dbf.DEFAULT_DBF_ENCODING):
        """
        Open DBF file.

        :param dbf_filename: DBF filename.
        """
        if dbf_filename:
            self._dbf_file_name = dbf_filename

        if encoding:
            self.encoding = encoding

        if self._dbf_file_name and os.path.exists(self._dbf_file_name):
            try:
                import dbfread
            except ImportError:
                log_func.error(u'Error import <dbfread> [https://github.com/olemb/dbfread/]')
                return False
            self._dbf = dbfread.DBF(self._dbf_file_name, load=True, encoding=self.encoding)
            self._cur_rec_no = 0
            return True
        return False

    def closeDBF(self):
        """
        Close DBF file.
        """
        if self._dbf:
            self._cur_rec_no = -1
            self._dbf = None
            return True
        return False

    def getFieldCount(self):
        """
        Get field number.
        """
        if self._dbf:
            return len(self._dbf.fields)
        return -1

    def getFieldByNum(self, n_field):
        """
        Get field value by index.

        :param n_field: Field index.
        """
        if self._dbf:
            cur_record = self._getCurrentRecord()
            return list(cur_record.values())[int(n_field)]
        return None

    def getFieldByName(self, field_name):
        """
        Get field value by name.

        :param field_name: Field name.
        """
        if self._dbf:
            cur_record = self._getCurrentRecord()
            return dict(cur_record)[str(field_name).upper()]
        return None

    def getDateFieldFmtByNum(self, n_field, datetime_fmt='%d/%m/%Y'):
        """
        Get date field value in format by index.

        :param n_field: Field index.
        :param datetime_fmt: Date value format.
        """
        dt_value = self.getFieldByNum(n_field)
        if dt_value:
            return dt_value.strftime(datetime_fmt)
        return None

    def getDateFieldFmtByName(self, field_name, datetime_fmt='%d/%m/%Y'):
        """
        Get date field value in format by name.

        :param field_name: Field name.
        :param datetime_fmt: Date value format.
        """
        dt_value = self.getFieldByName(field_name)
        if dt_value:
            return dt_value.strftime(datetime_fmt)
        return None

    def skipDBF(self, step=1):
        """
        Skip in table.

        :param step: Step. If <0 then to begin, and if >0 then to end.
        """
        self._cur_rec_no += step
        self._cur_rec_no = max(0, self._cur_rec_no)
        self._cur_rec_no = min(self.getRecCount(), self._cur_rec_no)
        return self._cur_rec_no

    def nextDBF(self):
        """
        Move to next record.
        """
        return self.skipDBF(1)

    def prevDBF(self):
        """
        Move to prev record.
        """
        return self.skipDBF(-1)

    def gotoDBF(self, rec_no=0):
        """
        Go to record.

        :param rec_no: Record index.
        """
        self._cur_rec_no = rec_no
        self._cur_rec_no = max(0, self._cur_rec_no)
        self._cur_rec_no = min(self.getRecCount(), self._cur_rec_no)
        return self._cur_rec_no

    def firstDBF(self):
        """
        Go to first record.
        """
        return self.gotoDBF(0)

    def lastDBF(self):
        """
        Go to last record.
        """
        return self.gotoDBF(self.getRecCount() - 1)

    def isEOF(self):
        """
        Is end of file?
        """
        return bool(self._cur_rec_no >= self.getRecCount())

    def isBOF(self):
        """
        Is begin of file?
        """
        return bool(self._cur_rec_no <= 0)

    def _getCurrentRecord(self):
        """
        Get current record.
        """
        if 0 <= self._cur_rec_no < self.getRecCount():
            try:
                return self._dbf.records[self._cur_rec_no]
            except:
                log_func.fatal(u'Error get record [%d] in DBF file <%s>' % (self._cur_rec_no,
                                                                            self.getDBFFileName()))
        return None

    def isDelRec(self):
        """
        Is mark deleted record?
        """
        # cur_record = self._getCurrentRecord()
        # if cur_record:
        #     return cur_record.deleted
        return False

    def getRecDict(self):
        """
        Get current record as dictionary.
        """
        cur_record = self._getCurrentRecord()

        if self.isDelRec():
            log_func.warning(u'Get marked delete DBF record')
            return None

        if cur_record:
            return dict(cur_record)
        return None

    def getErrorCode(self):
        """
        Get error code.
        """
        pass

    def getRecCount(self):
        """
        Get record number.
        """
        if self._dbf:
            if self._rec_count < 0:
                self._rec_count = len(self._dbf)
        else:
            self._rec_count = -1
        return self._rec_count

    def getFieldNum(self, field_name):
        """
        Get field index by name.

        :param field_name: Field name.
        """
        if self._dbf:
            field_names = [field.name for field in self._dbf.fields]
            return field_names.index(str(field_name).upper())
        return -1

    def findSort(self, field_name, find_text):
        """
        Find text in field value.

        :param field_name: Field name.
        :param find_text: Find text.
        """
        pass

    def filterRecsByField(self, field_name, value):
        """
        Filter records by field value.

        :param field_name: Field name.
        :param value: Field value.
        :return: Filtered record list.
        """
        try:
            records = list()
            open_ok = self.openDBF()
            if not open_ok:
                log_func.error(u'Error open DBF file <%s>' % self.getDBFFileName())
                return list()

            value = value.strip()
            record = self.getRecDict()
            while not self.isEOF():
                if field_name in record:
                    field_value = record[field_name].strip()
                    if field_value == value:
                        records.append(record)
                else:
                    log_func.error(u'Field <%s> not found in record %s' % (field_name, record.keys()))
                self.nextDBF()
                record = self.getRecDict()
            self.closeDBF()

            return records
        except:
            self.closeDBF()
            log_func.fatal(u'Error filter records DBF file <%s> by field <%s> value <%s>' % (self.getDBFFileName(),
                                                                                             field_name, value))
        return list()

    def getIndexRecsByField(self, field_name):
        """
        Filter records by field.

        :param field_name: Field name.
        :return: Dictionary:
            {
                field1 value :  filtered record list,
                ...
            }
            if empty dictionary if error.
        """
        try:
            index_records = dict()
            open_ok = self.openDBF()
            if not open_ok:
                log_func.error(u'Error open DBF file <%s>' % self.getDBFFileName())
                return dict()

            record = self.getRecDict()
            while not self.isEOF():
                if field_name in record:
                    field_value = record[field_name].strip()
                    if field_value in index_records:
                        index_records[field_value].append(record)
                    else:
                        index_records[field_value] = [record]
                else:
                    log_func.error(u'Field <%s> not found in record %s' % (field_name, record.keys()))
                self.nextDBF()
                record = self.getRecDict()
            self.closeDBF()

            return index_records
        except:
            self.closeDBF()
            log_func.fatal(u'Error filter records DBF file <%s> by field <%s>' % (self.getDBFFileName(),
                                                                                  field_name))
        return dict()

    def getRecNo(self):
        """
        Get current record index.
        """
        return self._cur_rec_no

    def isUsed(self):
        """
        Is used?
        """
        pass

    def getFieldName(self, n_field):
        """
        Get field name by index.

        :param n_field: Field index.
        """
        if self._dbf:
            field_names = [field.name for field in self._dbf.fields]
            return str(field_names[n_field]).upper()
        return None

    def getFieldType(self, n_field):
        """
        Get field type by index.

        :param n_field: Field index.
        """
        if self._dbf:
            field_types = [field.type for field in self._dbf.fields]
            return field_types[n_field]
        return None

    def getFieldLen(self, n_field):
        """
        Get field length by index.

        :param n_field: Field index.
        """
        if self._dbf:
            field_lengths = [field.length for field in self._dbf.fields]
            return field_lengths[n_field]
        return None

    def getFieldDecimal(self, n_field):
        """
        Get field decimal point by index.

        :param n_field: Field index.
        """
        if self._dbf:
            field_decimals = [field.decimal_count for field in self._dbf.fields]
            return field_decimals[n_field]
        return None
