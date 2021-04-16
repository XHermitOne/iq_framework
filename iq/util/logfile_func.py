#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions for reading messages from log files.

The program message log is saved in a file  *.log
Log format:
2016-11-18 08:22:11 INFO Message
    ^         ^      ^      ^
    |         |      |      +-- Message text
    |         |      +--------- Message type
    |         +---------------- Log time
    +-------------------------- Log date
The message text can be multi-line. Mostly for critical errors.
All programs should output messages in this format.
"""

import os
import os.path
import datetime

from . import log_func
from . import global_func

__version__ = (0, 0, 0, 1)

# Log types
INFO_LOG_TYPE = 'INFO'
WARNING_LOG_TYPE = 'WARNING'
ERROR_LOG_TYPE = 'ERROR'
FATAL_LOG_TYPE = 'FATAL'
DEBUG_LOG_TYPE = 'DEBUG'
SERVICE_LOG_TYPE = 'SERVICE'
DEBUG_SERVICE_LOG_TYPE = 'DEBUG SERVICE.'

LOG_TYPES = (DEBUG_SERVICE_LOG_TYPE,    # Non-core types must be first to be discovered
             SERVICE_LOG_TYPE,
             INFO_LOG_TYPE,
             WARNING_LOG_TYPE,
             ERROR_LOG_TYPE,
             FATAL_LOG_TYPE,
             DEBUG_LOG_TYPE,
             )

AND_FILTER_LOGIC = 'AND'
OR_FILTER_LOGIC = 'OR'

MSG_LEN_LIMIT = 100

DATETIME_LOG_FMT = '%Y-%m-%d %H:%M:%S'

DEFAULT_ENCODING = global_func.getDefaultEncoding()

LINE_SEPARATOR = os.linesep


def getRecordsLogFile(log_filename, log_types=LOG_TYPES,
                      dt_start_filter=None, dt_stop_filter=None,
                      filters=(), filter_logic=AND_FILTER_LOGIC,
                      encoding=DEFAULT_ENCODING):
    """
    Read messages of the specified types from the program message log file.

    :param log_filename: Log filename.
    :param log_types: Log message types.
    :param dt_start_filter: Start datetime of the filter by time.
        If not specified, then the selection occurs from the beginning of the file.
    :param dt_stop_filter: End datetime filter by time.
        If not specified, then the selection occurs to the end of the file.
    :param filters: Tuple / list of additional filtering methods.
        Filtering methods are specified as lambda or functions that take
        dictionary entries, but return True - entry falls into the selection / False - does not.
    :param filter_logic: Command for processing additional filters
        AND - For a record to be included in the selection, all filters must be positively executed,
        OR - For the entry to be included in the selection, a positive execution of one filter is sufficient.
    :param encoding: Log file encoding.
    :return: List of format dictionaries:
        [{'dt': Log datetime as datetime.datetime,
          'type': Message type: INFO, WARNING and etc,
          'text': Message,
          'short': Short message text limited MSG_LEN_LIMIT}, ...]
    """
    if not log_filename:
        log_func.warning(u'Undefined program message log file for reading')
        return list()

    if not os.path.exists(log_filename):
        log_func.warning(u'Program message log file <%s> not found' % log_filename)
        return list()

    log_file = None
    try:
        records = list()

        record = dict()
        log_file = open(log_filename, 'r')
        for line in log_file:
            # Determine whether the current line is the beginning of a new message or a continuation of the previous one
            if isNewMsg(line):
                record = parseLogMsgRecord(line, encoding=encoding)
                if checkFilterRecord(record, log_types, dt_start_filter, dt_stop_filter, filters, filter_logic):
                    records.append(record)
            else:
                record['text'] = record.get('text', u'') + line
                record['short'] += (u'...' if not record.get('short', u'').endswith(u'...') else u'')

        log_file.close()
        return records
    except:
        if log_file:
            log_file.close()
        log_func.fatal(u'Error reading program message log entries <%s>' % log_filename)
    return list()


def isNewMsg(line):
    """
    Determine if the current line is the beginning of a new message or
    continuation of the previous

    :param line: The current line of the program message log file being processed.
    :return: True - new message / False - continuation of the previous message.
    """
    if not line or len(line) < 20:
        return False
    try:
        msg_type = line[20:][:line[20:].index(' ')]
    except ValueError:
        return False
    return msg_type in LOG_TYPES


def getMsgLogType(line):
    """
    Determine the type of message log.

    :param line: The current line of the program message log file being processed.
    :return: Message type or None if error.
    """
    for log_type in LOG_TYPES:
        if line[20:].startswith(log_type):
            return log_type
    return None


def parseLogMsgRecord(line, encoding=DEFAULT_ENCODING):
    """
    Parse the line of the program message log file.

    :param line: The current line of the program message log file being processed.
    :return: {'dt': Log datetime as datetime.datetime,
              'type': Message type INFO, WARNING and etc,
              'text': Message text,
              'short': Short message text limited MSG_LEN_LIMIT}
    """
    dt_txt = line[:20].strip()
    try:
        dt = datetime.datetime.strptime(dt_txt, DATETIME_LOG_FMT)
    except:
        log_func.fatal(u'Error parse log datetime <%s>' % dt_txt)
        raise

    msg_type = getMsgLogType(line)
    msg = line[21+len(msg_type):].strip()
    short_msg = u''
    try:
        if isinstance(msg, str):
            short_msg = msg[:MSG_LEN_LIMIT] + (u'...' if len(msg) > MSG_LEN_LIMIT else u'')
    except:
        log_func.fatal(u'Error parse message text')
    return dict(dt=dt, type=msg_type, text=msg, short=short_msg)


def checkFilterRecord(record, log_types=LOG_TYPES,
                      dt_start_filter=None, dt_stop_filter=None,
                      filters=(), filter_logic=AND_FILTER_LOGIC):
    """
    Checking the correspondence of the entry to the filters.

    :param record: Current checked record .
    :param log_types: Log message types.
    :param dt_start_filter: Start datetime of the filter by time.
        If not specified, then the selection occurs from the beginning of the file.
    :param dt_stop_filter: End datetime filter by time.
        If not specified, then the selection occurs to the end of the file.
    :param filters: Tuple / list of additional filtering methods.
        Filtering methods are specified as lambda or functions that take
        dictionary entries, but return True - entry falls into the selection / False - does not.
    :param filter_logic: Command for processing additional filters
        AND - For a record to be included in the selection, all filters must be positively executed,
        OR - For the entry to be included in the selection, a positive execution of one filter is sufficient.
    :return: True - The entry matches all filters and must be added to the selection /
        False - The entry does not match any filter.
    """
    msg_type = record.get('type', '')
    if msg_type not in log_types:
        return False

    result = True
    dt = record.get('dt', None)
    if dt_start_filter:
        if dt:
            result = result and (dt >= dt_start_filter)
        else:
            log_func.warning(u'Error parse datetime in record %s' % str(record))
            return False
    if dt_stop_filter:
        if dt:
            result = result and (dt <= dt_stop_filter)
        else:
            log_func.warning(u'Error parse datetime in record %s' % str(record))
            return False

    if filters:
        try:
            filter_result = [fltr(record) for fltr in filters]
        except:
            log_func.fatal(u'Error check filters')
            return False

        if filter_logic == AND_FILTER_LOGIC:
            result = result and all(filter_result)
        elif filter_logic == OR_FILTER_LOGIC:
            result = result and any(filter_result)

    return result
