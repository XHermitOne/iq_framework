#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
*.DBF file manager.
"""

import os
import os.path
import copy
import time

from ...util import log_func

# Error codes:
NOT_ERROR = 0       # Not error
NOT_OPEN = 1        # Error open file
NOT_GET = 2         # Error read byte from file
NOT_PUT = 3         # Error write byte to file
NOT_SEEK = 4        # Error set position in file
NOT_TELL = 5        # Error get position in file
NOT_FIELD = 6       # Error find field name
NOT_TYPE = 7        # Error type field
NOT_MEMORY = 8      # Memory error
NOT_ALLOC = 9       # Memory allocation error
NOT_LIBRARY = 10    # Dynamic library error
NOT_DEL = 11        # Error delete file
NOT_RENAME = 12     # Error rename template file

# Error text
ERROR_TXT = {NOT_ERROR: u'Not error',
             NOT_OPEN: u'Error open file',
             NOT_GET: u'Error read byte from file',
             NOT_PUT: u'Error write byte to file',
             NOT_SEEK: u'Error set position in file',
             NOT_TELL: u'Error get position in file',
             NOT_FIELD: u'Error find field name',
             NOT_TYPE: u'Error type field',
             NOT_MEMORY: u'Memory error',
             NOT_ALLOC: u'Memory allocation error',
             NOT_LIBRARY: u'Dynamic library error',
             NOT_DEL: u'Error delete file',
             NOT_RENAME: u'Error rename template file',
             }

# DBF file field specification
SPC_DBF_FIELD = {'name': 'field1',      # Field name
                 'type': 'C',           # Field type
                 'len': 10,             # Field length
                 'decimal': 0,          # Decimal point
                 }

DEL_REC_FLAG = 1        # Delete record flag
UNDEL_REC_FLAG = 0      # Undelete record flag
IS_DEL_REC_FLAG = 99    # Is deleted record flag

# End of file
DBF_FILE_EOF_CHAR = 0x1A

# Alignment (default right alignment)
LEFT_ALIGN = 1
RIGHT_ALIGN = 0

DEFAULT_DBF_ENCODING = 'cp866'

__version__ = (0, 0, 0, 1)


class iqDBFFileProto(object):
    """
    *.DBF file manager class .
    """
    def __init__(self, dbf_filename=None):
        """
        Constructor.

        :param dbf_filename: DBF filename.
        """
        self._dbf_file_name = dbf_filename

    def getDBFFileName(self):
        return self._dbf_file_name

    def __del__(self):
        """
        Destructor.
        """
        self.closeDBF()

    def createDBF(self, dbf_struct=(), dbf_filename=None, recreate=True):
        """
        Create DBF file.

        :param dbf_struct: DBF file struct in format:
            ({'name': field1 name,
             'type': field1 type('C', 'N' and etc),
             'len': field1 length,
             'decimal': field1 decimal point},
             ...).
        :param dbf_filename: DBF filename.
        :param recreate: Recreate file if exists?
        """
        assert 0, u'Empty method'

    def openDBF(self, dbf_filename=None):
        """
        Open DBF file.

        :param dbf_filename: DBF filename.
        """
        assert 0, u'Empty method'

    def closeDBF(self):
        """
        Close DBF file.
        """
        assert 0, u'Empty method'

    def getFieldCount(self):
        """
        Get field number.
        """
        assert 0, u'Empty method'

    def getFieldByNum(self, n_field):
        """
        Get field value by index.

        :param n_field: Field index.
        """
        assert 0, u'Empty method'

    def getFieldByName(self, field_name):
        """
        Get field value by name.

        :param field_name: Field name.
        """
        assert 0, u'Empty method'

    def setFieldByNum(self, n_field, field_value, align=None):
        """
        Set field value by index.

        :param n_field: Field index.
        :param field_value: Vield value.
        :param align: Alignment.
        """
        assert 0, u'Empty method'

    def setFieldByName(self, field_name, field_value, align=None):
        """
        Set field value by name.

        :param field_name: Field name.
        :param field_value: Field value.
        :param align: Alignment.
        """
        assert 0, u'Empty method'

    def setDateFieldByNum(self, n_field, datetime_tuple):
        """
        Set date field by index.

        :param n_field: Field index.
        :param datetime_tuple: Date field value as tuple.
        """
        assert 0, u'Empty method'
        
    def setDateFieldByName(self, field_name, datetime_tuple):
        """
        Set date field by name.

        :param field_name: Field name.
        :param datetime_tuple: Date field value as tuple.
        """
        assert 0, u'Empty method'

    def setDateFieldFmtByNum(self, n_field, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Set date field value in format by index.

        :param n_field: Field index.
        :param datetime_value: Date field value as string in format datetime_fmt.
        :param datetime_fmt: Date value format.
        """
        assert 0, u'Empty method'
        
    def setDateFieldFmtByName(self, field_name, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Set date field value in format by name.

        :param field_name: Field name.
        :param datetime_value: Date field value as string in format datetime_fmt.
        :param datetime_fmt: Date value format.
        """
        assert 0, u'Empty method'

    def getDateFieldFmtByNum(self, n_field, datetime_fmt='%d/%m/%Y'):
        """
        Get date field value in format by index.

        :param n_field: Field index.
        :param datetime_fmt: Date value format.
        """
        assert 0, u'Empty method'
        
    def getDateFieldFmtByName(self, field_name, datetime_fmt='%d/%m/%Y'):
        """
        Get date field value in format by name.

        :param field_name: Field name.
        :param datetime_fmt: Date value format.
        """
        assert 0, u'Empty method'
            
    def skipDBF(self, step=1):
        """
        Skip in table.

        :param step: Step. If <0 then to begin, and if >0 then to end.
        """
        assert 0, u'Empty method'

    def nextDBF(self):
        """
        Move to next record.
        """
        assert 0, u'Empty method'

    def prevDBF(self):
        """
        Move to prev record.
        """
        assert 0, u'Empty method'

    def gotoDBF(self, rec_no=0):
        """
        Go to record.

        :param rec_no: Record index.
        """
        assert 0, u'Empty method'

    def firstDBF(self):
        """
        Go to first record.
        """
        assert 0, u'Empty method'

    def lastDBF(self):
        """
        Go to last record.
        """
        assert 0, u'Empty method'

    def isEOF(self):
        """
        Is end of file?
        """
        assert 0, u'Empty method'

    def isBOF(self):
        """
        Is begin of file?
        """
        assert 0, u'Empty method'

    def delRec(self):
        """
        Mark deleted record.
        """
        assert 0, u'Empty method'

    def unDelRec(self):
        """
        Unmark deleted record.
        """
        assert 0, u'Empty method'

    def isDelRec(self):
        """
        Is mark deleted record?
        """
        assert 0, u'Empty method'

    def delRecord(self, del_flag):
        """
        Delete records.

        :param del_flag: Delete flag.
        """
        assert 0, u'Empty method'

    def setDel(self):
        """
        Set delete records.
        """
        assert 0, u'Empty method'

    def appendRecord(self, *rec_num, **rec_name):
        """
        Append empty record to table end.

        :param rec_num: Record by index.
        :param rec_name: Record by names.
        """
        assert 0, u'Empty method'

    def getRecDict(self):
        """
        Get current record as dictionary.
        """
        assert 0, u'Empty method'
        
    def getErrorCode(self):
        """
        Get error code.
        """
        assert 0, u'Empty method'

    def getRecCount(self):
        """
        Get record number.
        """
        assert 0, u'Empty method'

    def getFieldNum(self, field_name):
        """
        Get field index by name.

        :param field_name: Field name.
        """
        assert 0, u'Empty method'

    def findSort(self, field_name, find_text):
        """
        Find text in field value.

        :param field_name: Field name.
        :param find_text: Find text.
        """
        assert 0, u'Empty method'

    def filterRecsByField(self, field_name, value):
        """
        Filter records by field value.

        :param field_name: Field name.
        :param value: Field value.
        :return: Filtered record list.
        """
        assert 0, u'Empty method'

    def getRecNo(self):
        """
        Get current record index.
        """
        assert 0, u'Empty method'

    def isUsed(self):
        """
        Is used?
        """
        assert 0, u'Empty method'

    def zap(self):
        """
        Zap DBF.
        """
        assert 0, u'Empty method'

    def pack(self):
        """
        Pack DBF.
        """
        assert 0, u'Empty method'

    def getFieldName(self, n_field):
        """
        Get field name by index.

        :param n_field: Field index.
        """
        assert 0, u'Empty method'

    def getFieldType(self, n_field):
        """
        Get field type by index.

        :param n_field: Field index.
        """
        assert 0, u'Empty method'

    def getFieldLen(self, n_field):
        """
        Get field length by index.

        :param n_field: Field index.
        """
        assert 0, u'Empty method'

    def getFieldDecimal(self, n_field):
        """
        Get field decimal point by index.

        :param n_field: Field index.
        """
        assert 0, u'Empty method'

    def _delLastEOFChar(self, dbf_filename):
        """
        Delete last symbol if it is EOF.

        :param dbf_filename: *.DBF filename.
        """
        dbf_file = None
        if os.path.isfile(dbf_filename):
            try:
                dbf_file = open(dbf_filename, 'r+')
                dbf_file.seek(0, 2)
                dbf_file_size = dbf_file.tell()
                last_char = dbf_file.read(1)
                if last_char and ord(last_char) == DBF_FILE_EOF_CHAR:
                    dbf_file.trancate(dbf_file_size-2)
                dbf_file.close()
            except:
                log_func.fatal(u'Error delete last EOF symbol')
                if dbf_file:
                    dbf_file.close()
                return False
            return True
        return False

    def _alignValueByName(self, field_name, field_value, align=RIGHT_ALIGN):
        """
        Align value.

        :param field_name: Field name.
        :param field_value: Field value.
        :param align: Alignment.
        :return: Aligned value string.
        """
        if field_value is None:
            field_value = ''

        field_len = self.getFieldLen(self.getFieldNum(str(field_name).upper()))
        field_val = str(field_value)[:field_len]
        if align == LEFT_ALIGN:
            align_fmt = '%-'+str(field_len)+'s'
            field_val = align_fmt % field_val
        elif align == RIGHT_ALIGN:
            # Default right alignment
            pass
        return field_val

    def _alignValueByNum(self, n_field, field_value, align=RIGHT_ALIGN):
        """
        Align value.

        :param n_field: Field index.
        :param field_value: Field value.
        :param align: Alignment.
        :return: Aligned value string.
        """
        if field_value is None:
            field_value = ''

        field_len = self.getFieldLen(n_field)
        field_val = str(field_value)[:field_len]
        if align == LEFT_ALIGN:
            align_fmt = '%-'+str(field_len)+'s'
            field_val = align_fmt % field_val
        elif align == RIGHT_ALIGN:
            # Default right alignment
            pass
        return field_val


class iqDBFPYFile(iqDBFFileProto):
    """
    *.DBF file manager class.
    """
    def __init__(self, dbf_filename=None):
        """
        Constructor.

        :param dbf_filename: DBF filename.
        """
        iqDBFFileProto.__init__(self, dbf_filename)
        # Auto alignment
        self.AutoAlign = RIGHT_ALIGN
        
        self._dbf = None        # DBF object
        self._cur_rec_no = -1   # Cur record index
        self._rec_count = -1    # Record number

    def createDBF(self, dbf_struct=(), dbf_filename=None, recreate=True):
        """
        Create DBF file.

        :param dbf_struct: DBF file struct in format:
            ({'name': field1 name,
             'type': field1 type('C', 'N' and etc),
             'len': field1 length,
             'decimal': field1 decimal point},
             ...).
        :param dbf_filename: DBF filename.
        :param recreate: Recreate file if exists?
        """
        if dbf_filename:
            self._dbf_file_name = dbf_filename
        if self._dbf_file_name:
            try:
                import dbfpy3.dbf
            except ImportError:
                log_func.error(u'Error import dbfpy3.dbf')
                return False

            self._dbf = dbfpy3.dbf.Dbf(dbf_filename, new=recreate)
            # Add fields
            fields = [(fld['name'].upper(), fld['type'], fld['len'], fld['decimal']) for fld in dbf_struct]
            self._dbf.addField(*fields)

            # Create file
            self._dbf.flush()
            self._dbf.close()
            return True
        return False

    def openDBF(self, dbf_filename=None):
        """
        Open DBF file.

        :param dbf_filename: DBF filename.
        """
        if dbf_filename:
            self._dbf_file_name = dbf_filename
        if self._dbf_file_name:
            try:
                import dbfpy3.dbf
            except ImportError:
                log_func.error(u'Error import dbfpy3.dbf')
                return False

            self._dbf = dbfpy3.dbf.Dbf(self._dbf_file_name)
            self._cur_rec_no = 0
            return True
        return False

    def closeDBF(self):
        """
        Close DBF file.
        """
        if self._dbf:
            self._cur_rec_no = -1
            return self._dbf.close()
        return False

    def getFieldCount(self):
        """
        Get field number.
        """
        if self._dbf:
            return len(self._dbf.fieldDefs)
        return -1

    def getFieldByNum(self, n_field):
        """
        Get field value by index.

        :param n_field: Field index.
        """
        if self._dbf:
            cur_record = self._getCurrentRecord()
            return cur_record.asList()[int(n_field)]
        return None

    def getFieldByName(self, field_name):
        """
        Get field value by name.

        :param field_name: Field name.
        """
        if self._dbf:
            cur_record = self._getCurrentRecord()
            return cur_record[str(field_name).upper()]
        return None

    def setFieldByNum(self, n_field, field_value, align=None):
        """
        Set field value by  index.

        :param n_field: Field index.
        :param field_value: Field value.
        :param align: Alignment.
        """
        field_name = self.getFieldName(n_field)
        return self.setFieldByName(field_name, field_value, align)

    def setFieldByName(self, field_name, field_value, align=None):
        """
        Set field value by name.

        :param field_name: Field name.
        :param field_value: Field value.
        :param align: Alignment.
        """
        if align is None:
            align = self.AutoAlign
        field_name = str(field_name).upper()
        
        if self._dbf:
            cur_record = self._getCurrentRecord()
            cur_record[field_name] = self._alignValueByName(field_name, field_value, align)
            cur_record.store()
            return True
        return False

    def setDateFieldByNum(self, n_field, datetime_tuple):
        """
        Set date field value by index.

        :param n_field: Field index.
        :param datetime_tuple: Datetime value as tuple.
        """
        pass
        
    def setDateFieldByName(self, field_name, datetime_tuple):
        """
        Set date field value by name.

        :param field_name: Field name.
        :param datetime_tuple: Datetime value as tuple.
        """
        pass

    def setDateFieldFmtByNum(self, n_field, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Set date field value in format by index.

        :param n_field: Field index.
        :param datetime_value: Date field value as string in format datetime_fmt.
        :param datetime_fmt: Date value format.
        """
        pass
        
    def setDateFieldFmtByName(self, field_name, datetime_value, datetime_fmt='%d/%m/%Y'):
        """
        Set date field value in format by name.

        :param field_name: Field name.
        :param datetime_value: Date field value as string in format datetime_fmt.
        :param datetime_fmt: Date value format.
        """
        pass

    def getDateFieldFmtByNum(self, n_field, datetime_fmt='%d/%m/%Y'):
        """
        Get date field value in format by index.

        :param n_field: Field index.
        :param datetime_fmt: Date value format.
        """
        pass
        
    def getDateFieldFmtByName(self, field_name, datetime_fmt='%d/%m/%Y'):
        """
        Get date field value in format by name.

        :param field_name: Field name.
        :param datetime_fmt: Date value format.
        """
        pass
            
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
        return self.gotoDBF(self.getRecCount()-1)

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
        Get current record object.
        """
        if 0 <= self._cur_rec_no < self.getRecCount():
            try:
                return self._dbf[self._cur_rec_no]
            except:
                log_func.fatal(u'Error get record [%d] in DBF file <%s>' % (self._cur_rec_no,
                                                                            self.getDBFFileName()))
        return None
        
    def delRec(self):
        """
        Mark deleted record.
        """
        cur_record = self._getCurrentRecord()
        if cur_record:
            cur_record.delete()
            self._rec_count -= 1
            return True
        return False            

    def unDelRec(self):
        """
        Unmark deleted record.
        """
        pass

    def isDelRec(self):
        """
        Is mark deleted record?
        """
        cur_record = self._getCurrentRecord()
        if cur_record:
            return cur_record.deleted
        return False            

    def delRecord(self, del_flag):
        """
        Delete records.

        :param del_flag: Delete flag.
        """
        pass

    def setDel(self):
        """
        Set delete records.
        """
        pass

    def appendRecord(self, *rec_num, **rec_name):
        """
        Append empty record to table end.

        :param rec_num: Record by index.
        :param rec_name: Record by names.
        """
        ok = False
        if self._dbf:
            rec = self._dbf.newRecord()
            if rec_num:
                for i_field in range(len(rec_num)):
                    self.setFieldByNum(i_field, rec_num[i_field])
            if rec_name:
                for field_name in rec_name.keys():
                    self.setFieldByName(field_name, rec_name[field_name])
            rec.store()
            self._rec_count += 1
        return ok

    def getRecDict(self):
        """
        Get current record as dictionary.
        """
        cur_record = self._getCurrentRecord()
        if cur_record is None:
            log_func.warning(u'DBF file current record not defined')
            return None
        if cur_record.deleted:
            log_func.warning(u'Get marked delete DBF record')
            return None

        if cur_record:
            return cur_record.asDict()
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
            return self._dbf.indexOfFieldName(str(field_name).upper())
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

            record = self.getRecDict()
            while not self.isEOF():
                if field_name in record:
                    field_value = record[field_name]
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
            log_func.fatal(u'Error filter DBF file <%s> records by field <%s> value <%s>' % (self.getDBFFileName(),
                                                                                             field_name, value))
        return list()

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

    def zap(self):
        """
        Zap DBF.
        """
        pass

    def pack(self):
        """
        Pack DBF.
        """
        pass

    def getFieldName(self, n_field):
        """
        Get field name by index.

        :param n_field: Field index.
        """
        if self._dbf:
            field_name = self._dbf.fieldNames[int(n_field)]
            return str(field_name).upper()
        return None

    def getFieldType(self, n_field):
        """
        Get field type by index.

        :param n_field: Field index.
        """
        if self._dbf:
            field = self._dbf.fieldDefs[int(n_field)]
            return field.typeCode
        return None

    def getFieldLen(self, n_field):
        """
        Get field length by index.

        :param n_field: Field index.
        """
        if self._dbf:
            field = self._dbf.fieldDefs[int(n_field)]
            return field.length
        return None

    def getFieldDecimal(self, n_field):
        """
        Get field decimal point by index.

        :param n_field: Field index.
        """
        if self._dbf:
            field = self._dbf.fieldDefs[int(n_field)]
            return field.decimalCount
        return None
