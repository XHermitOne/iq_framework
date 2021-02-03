#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JSON RPC client functions.
"""

import jsonrpclib

from . import log_func

__version__ = (0, 0, 0, 1)

HTTP_URL_FMT = 'http://%s:%s'
# Error message signature
TASK_ERROR_SIGNATURE = u'ERROR: '


def createJSONRPCServerUrl(host=None, port=None):
    """
    Create JSON RCP server connection url.

    :param host: JSON RCP server host.
    :param port: JSON RCP server port.
    :return: Url string or None if error.
    """
    if not host:
        log_func.warning(u'Not define JSON RPC server host')
        return None

    if not port:
        log_func.warning(u'Not define JSON RPC server port')
        return None

    url = HTTP_URL_FMT % (str(host), str(port))
    log_func.info(u'Create JSON RPC server url <%s>' % url)
    return url


def createJSONRPCServerConnection(url):
    """
    Create JSON RCP server connection.

    :param url: JSON RCP server connection url.
    :return: Connection object or None if error.
    """
    try:
        connection = jsonrpclib.Server(url)
        return connection
    except:
        log_func.fatal(u'Error create JSON RCP server connection <%s>' % str(url))
    return None


def validJSONRPCServerConnection(url):
    """
    Check connection with JSON RCP server.

    :param url: JSON RCP server connection url.
    :return: True - connected. False - not connected.
    """
    try:
        connection = jsonrpclib.Server(url)
        result = connection.validConnection()
        log_func.info(u'Check JSON RPC server <%s> connection [%s]' % (url, '+' if result else '-'))
        return result
    except ConnectionRefusedError:
        log_func.warning(u'Check JSON RPC server <%s> connection [-]' % url)
    return False


def loginJSONRPCServerTask(connection, username, password=None):
    """
    Login to JSON RPC tasks server.

    :param connection: Connection object.
    :param username: Username.
    :param password: User password.
    :return: True/False.
    """
    if not connection:
        log_func.warning(u'Login. Not define JSON RPC server connection')
        return False

    if not username:
        log_func.warning(u'Login. Not define JSON RPC server username')
        return False

    try:
        return connection.login(username, password)
    except:
        log_func.fatal(u'Error login to JSON RPC tasks server')
    return False


def logoutJSONRPCServerTask(connection, username, password=None):
    """
    Logout from JSON RPC tasks server.

    :param connection: Connection object.
    :param username: Username.
    :param password: User password.
    :return: True/False.
    """
    if not connection:
        log_func.warning(u'Logout. Not define JSON RPC server connection')
        return False

    if not username:
        log_func.warning(u'Logout. Not define JSON RPC server username')
        return False

    try:
        return connection.logout(username, password)
    except:
        log_func.fatal(u'Error logout from JSON RPC tasks server')
    return False


def isTaskErrorText(text):
    """
    Is error text?

    :param text: Text
    :return: True - error text / False - not.
    """
    return text.startswith(TASK_ERROR_SIGNATURE) if isinstance(text, str) else False


def executeJSONRPCServerTask(connection, username, task_name, *args, **kwargs):
    """
    Execute remote task JSON RPC server.

    :param connection: Connection object.
    :param username: Username.
    :param task_name: Task name.
    :param args: Task arguments.
    :param kwargs: Task named arguments.
    :return: Task result or None if error.
    """
    if not connection:
        msg = u'Execute task <%s>. Not define JSON RPC server connection' % task_name
        log_func.warning(msg)
        return None

    if not username:
        msg = u'Execute task <%s>. Not define JSON RPC server username' % task_name
        log_func.warning(msg)
        return None

    try:
        result = connection.execute(username, task_name, *args, **kwargs)
        if isTaskErrorText(result):
            msg = result.lstrip(TASK_ERROR_SIGNATURE)
            log_func.error(u'Error execute task <%s>: %s' % (task_name, msg))
            return None
        return result
    except:
        log_func.fatal(u'Error execute JSON RPC tasks server task <%s>' % task_name)
    return None
