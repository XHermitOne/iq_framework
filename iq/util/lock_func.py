#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lock system functions.
"""

import os
import os.path
import stat

from . import log_func
from . import file_func
from . import sys_func
from . import global_func
from . import lang_func
from ..dialog import dlg_func

__version__ = (0, 0, 1, 2)

_ = lang_func.getTranslation().gettext

LOCK_FILE_EXT = '.lck'

DEFAULT_LOCK_NAME = 'default'

DEFAULT_LOCK_DIR = os.path.join(file_func.getFrameworkPath(), 'lock')

UNKNOWN_USER = u'User name not defined'
UNKNOWN_COMPUTER = u'Computer name not defined'


def lockRecord(table, record, message=None):
    """
    Lock record by table name and record index.

    :param table: Table name.
    :param record:  Record index.
    :param message: Message.
    :return: True/False.
    """
    result = True
    table = str(table)
    record = str(record)

    if isLockTable(record):
        log_func.warning(u'Record <%s : %s> is locked' % (table, record))
        return False

    table_lock_dirname = os.path.join(getLockDir(), table)
    if not os.path.isdir(table_lock_dirname):
        try:
            os.makedirs(table_lock_dirname)
        except:
            log_func.fatal(u'Error create folder <%s>' % table_lock_dirname)
            result = False

    record_lock_filename = os.path.join(table_lock_dirname, record)
    try:
        lock_file = os.open(record_lock_filename, os.O_CREAT | os.O_EXCL,
                            mode=stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except OSError:
        result = False
    else:
        if isinstance(message, str):
            os.close(lock_file)
            try:
                lock_file = os.open(record_lock_filename, os.O_WRONLY,
                                    mode=stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                os.write(lock_file, message.encode())
            except:
                log_func.fatal(u'Error save lock file <%s>' % record_lock_filename)
                result = False
        os.close(lock_file)

    return result


def unLockRecord(table, record):
    """
    Unlock record by table name and record index.

    :param table: Table name.
    :param record:  Record index.
    :return: True/False.
    """
    result = True
    table = str(table)
    record = str(record)

    table_lock_dirname = os.path.join(getLockDir(), table)
    if os.path.isdir(table_lock_dirname):

        record_lock_filename = os.path.join(table, record)
        if os.path.isfile(record_lock_filename):
            try:
                os.remove(record_lock_filename)
            except:
                log_func.fatal(u'Error remove file <%s>' % record_lock_filename)
                result = False
    else:
        result = False
    return result


def lockTable():
    pass


def unLockTable():
    pass


def isLockTable(table):
    """
    Is locked table?
    """
    table = str(table)
    path = os.path.join(getLockDir(), table + LOCK_FILE_EXT)
    return os.path.isdir(path)


def readLockMessage(table, record):
    """
    Read lock message.

    :param table: Table name.
    :param record:  Record index.
    :return: Lock message.
    """
    result = None
    lock_file = None
    if isLockRecord(table, record):
        table = str(table)
        record = str(record)

        table_lock_dirname = os.path.join(getLockDir(), table)
        record_lock_filename = os.path.join(table_lock_dirname, record)
        try:
            lock_file = os.open(record_lock_filename, os.O_RDONLY | os.O_EXCL,
                                mode=stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        except OSError:
            pass

    if lock_file:
        result = os.read(lock_file, 65535)
        os.close(lock_file)
    return result


def isLockRecord(table, record):
    """
    Is locked record?

    :param table: Table name.
    :param record:  Record index.
    :return: True/False.
    """
    result = False

    table = str(table)
    record = str(record)

    table_lock_dirname = os.path.join(getLockDir(), table)
    if os.path.isdir(table_lock_dirname):
        record_lock_filename = os.path.join(table_lock_dirname, record)
        result = os.path.exists(record_lock_filename)
    return result


def getLockDir():
    """
    Get lock directory.
    """
    prj_name = global_func.getProjectName()
    lock_dir = os.path.join(file_func.getProjectPath(), 'lock') if prj_name else DEFAULT_LOCK_DIR
    return lock_dir


def clearDirLocks(lock_id, lock_dir, lock_filenames):
    """
    Delete locks from directory.

    :param lock_id: Lock owner id.
    :param lock_dir: Lock directory.
    :param lock_filenames: Lock filename in lock_dir
    """
    try:
        lock_files = [x for x in [os.path.join(lock_dir, x) for x in lock_filenames] if os.path.isfile(x)]

        for cur_filename in lock_files:
            lock_file = None
            try:
                lock_file = open(cur_filename, 'rt')
                signature = lock_file.read()
                lock_file.close()
                try:
                    signature = eval(signature)
                    if signature['computer'] == lock_id:
                        os.remove(cur_filename)
                        log_func.info(u'Delete lock file <%s>' % cur_filename)
                except:
                    log_func.warning(u'Not valid lock signature <%s>' % signature)
            except:
                if lock_file:
                    lock_file.close()
                log_func.fatal(u'Error read lock signature file <%s>' % cur_filename)
    except:
        log_func.fatal(u'Error delete lock files from <%s>' % lock_dir)


def clearLocks(lock_id=None, lock_dir=None):
    """
    Delete locks.

    :param lock_id: Lock owner id.
    :param lock_dir: Lock directory.
    """
    if lock_dir is None:
        lock_dir = getLockDir()
    if not lock_id:
        lock_id = sys_func.getComputerName()
    return os.path.walk(lock_dir, clearDirLocks, lock_id)


def lockFile(filename, lock_record=None):
    """
    Lock file.

    :param filename: Lock filename.
    :param lock_record: Lock record.
    :return: Tuple:
        (True/False, Lock record).
    """
    lock_file_flag = False
    lock_rec = lock_record

    lock_filename = os.path.splitext(filename)[0] + LOCK_FILE_EXT

    if not os.path.isfile(lock_filename):
        lock_dir = os.path.dirname(lock_filename)
        if not os.path.isdir(lock_dir):
            try:
                os.makedirs(lock_dir)
            except:
                log_func.fatal(u'Error create folder <%s>' % lock_dir)

        lock_file = None
        try:
            lock_file = os.open(lock_filename, os.O_CREAT | os.O_EXCL,
                                mode=stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        except OSError:
            lock_file_flag = True
            if lock_file:
                os.close(lock_file)
            lock_rec = readLockRecord(lock_filename)
        else:
            if lock_record is not None:
                os.close(lock_file)
                lock_file = os.open(lock_filename, os.O_WRONLY,
                                    mode=stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                if isinstance(lock_record, str):
                    str_lock_rec = lock_record
                else:
                    str_lock_rec = str(lock_record)
                os.write(lock_file, str_lock_rec.encode())
            os.close(lock_file)
    else:
        lock_file_flag = True
        lock_rec = readLockRecord(lock_filename)

    return not lock_file_flag, lock_rec


def readLockRecord(lock_filename):
    """
    Read lock file.

    :param lock_filename: Lock filename.
    :return: Lock record if None if error.
    """
    lock_file = None
    try:
        lock_filename = os.path.splitext(lock_filename)[0] + LOCK_FILE_EXT

        if not os.path.exists(lock_filename):
            return None

        lock_file = os.open(lock_filename, os.O_RDONLY,
                            mode=stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        lock_rec = os.read(lock_file, 65535)
        os.close(lock_file)
        try:
            return eval(lock_rec)
        except:
            log_func.warning(u'Error lock record format <%s>' % lock_rec)
            return lock_rec
    except:
        if lock_file:
            os.close(lock_file)
        log_func.fatal(u'Error read lock record <%s>' % lock_filename)
    return None


def isLockFile(filename):
    """
    Is locked file?

    :param filename: Filename.
    :return: True/False.
    """
    lock_filename = os.path.splitext(filename)[0] + LOCK_FILE_EXT
    return os.path.isfile(lock_filename)


def unLockFile(filename, **unlock_condition):
    """
    Unlock file.

    :param filename: Filename.
    :param unlock_condition: Unlock check condition.
        Lock record attribute name = value.
        If attribute name not exists in lock record,
        then it value is None.
    :return: True/False.
    """
    lock_filename = os.path.splitext(filename)[0] + LOCK_FILE_EXT
    log_func.info(u'Unlock. Lock file <%s> (%s). Condition %s' % (lock_filename,
                                                                  os.path.exists(lock_filename), unlock_condition))
    if os.path.exists(lock_filename):
        if unlock_condition:
            lck_rec = readLockRecord(lock_filename)

            can_unlock = bool(len([key for key in unlock_condition.keys() if lck_rec.setdefault(key, None) == unlock_condition[key]]) == len(unlock_condition))
            log_func.info(u'Lock record %s (%s)' % (lck_rec, can_unlock))
            if can_unlock:
                os.remove(lock_filename)
            else:
                return False
        else:
            os.remove(lock_filename)
    log_func.info(u'Unlock file <%s>' % lock_filename)
    return True


def _unLockFileWalk(args, cur_dir, cur_names):
    """
    Unlock file by computer name.
    Use in os.path.walk().

    :param args: Tuple (Computer name, User name).
    :param cur_dir: Current folder path.
    :param cur_names: Sub folder names.
    """
    computer_name = args[0]
    user_name = args[1]

    lock_files = [x for x in [os.path.join(cur_dir, x) for x in cur_names] if os.path.isfile(x) and os.path.splitext(x)[1] == LOCK_FILE_EXT]

    for cur_file in lock_files:
        lock_record = readLockRecord(cur_file)

        if isinstance(lock_record, str) and not lock_record.strip():
            os.remove(cur_file)
            log_func.warning(u'Remove lock file <%s>. Invalid lock record <%s>' % (cur_file, lock_record))
        else:
            if not user_name:
                if lock_record['computer'] == computer_name:
                    os.remove(cur_file)
                    log_func.info(u'Remove lock file <%s>' % cur_file)
            else:
                if lock_record['computer'] == computer_name and lock_record['user'] == user_name:
                    os.remove(cur_file)
                    log_func.info(u'Remove lock file <%s>' % cur_file)


def unLockFiles(lock_dir, computer_name=None, user_name=None):
    """
    Unnlock files if directory.

    :param lock_dir: Lock directory.
    :param computer_name: Computer name.
    :return: True/False.
    """
    if not computer_name:
        computer_name = sys_func.getComputerName()
    if not user_name:
        user_name = global_func.getUsername()
    if lock_dir:
        return os.walk(lock_dir, _unLockFileWalk, (computer_name, user_name))


def getLockUsername(lock_filename):
    """
    Get lock owner user name.

    :param lock_filename: Lock filename.
    """
    if isLockFile(lock_filename):
        lock_rec = readLockRecord(lock_filename)
        return lock_rec.get('user', UNKNOWN_USER) if isinstance(lock_rec, dict) else UNKNOWN_USER
    return UNKNOWN_USER


def getLockComputer(lock_filename):
    """
    Get lock owner computer name.

    :param lock_filename: Lock filename.
    """
    if isLockFile(lock_filename):
        lock_rec = readLockRecord(lock_filename)
        return lock_rec.get('computer', UNKNOWN_COMPUTER) if isinstance(lock_rec, dict) else UNKNOWN_COMPUTER
    return UNKNOWN_COMPUTER


def getLockFilename(lock_name):
    """
    Get lock filename by lock name.

    :param lock_name: Lock name.
    :return: Full lock filename.
    """
    return os.path.join(getLockDir(), lock_name + LOCK_FILE_EXT)


def lockObj(lock_name):
    """
    Lock object by name.

    :param lock_name: Lock name.
    :return:
    """
    username = global_func.getUsername()
    computer = sys_func.getComputerName()
    return lockFile(getLockFilename(lock_name=lock_name),
                    lock_record=dict(user=username, computer=computer))


def unLockObj(lock_name, *args, **kwargs):
    """
    Unlock object by name.

    :param lock_name: Lock name.
    :return:
    """
    return unLockFile(getLockFilename(lock_name=lock_name), *args, **kwargs)


def isLockObj(lock_name):
    """
    Is locked object?

    :param lock_name: Lock name.
    :return: True/False.
    """
    is_lock_file = isLockFile(getLockFilename(lock_name=lock_name))
    if is_lock_file:
        username = global_func.getUsername()
        computer = sys_func.getComputerName()
        return (username != getLockUsernameObj(lock_name)) or (computer != getLockComputerObj(lock_name))
    return is_lock_file


def getLockUsernameObj(lock_name):
    """
    Get lock owner user name.

    :param lock_name: Lock name.
    :return:
    """
    return getLockUsername(getLockFilename(lock_name=lock_name))


def getLockComputerObj(lock_name):
    """
    Get lock owner computer name.

    :param lock_name: Lock name.
    :return:
    """
    return getLockComputer(getLockFilename(lock_name=lock_name))


def openStdWarningBoxIfLocked(lock_name, lock_msg=None):
    """
    Open standart warning box if resource is locked.

    :param lock_name: Lock name.
    :param lock_msg: Lock message.
    :return: True - resource is locked/False - not locked.
    """
    if isLockObj(lock_name):
        lock_computer = getLockComputerObj(lock_name)
        lock_username = getLockUsernameObj(lock_name)
        if lock_msg is None:
            lock_msg = _('Editing locked by user ') + lock_username + _(' Computer ') + lock_computer
        dlg_func.openWarningBox(_('ATTENTION'), lock_msg)
        return True
    return False
