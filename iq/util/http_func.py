#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP send get/post request functions.
"""

import os
import time
import json

from . import log_func
from . import file_func

try:
    import urllib3
except ImportError:
    log_func.error(u'Import error urllib3')

__version__ = (0, 1, 2, 2)


def getHTTP3(url, headers=None, **kwargs):
    """
    GET request HTTP. urllib3 version.

    :param url: URL.
    :param headers: Request headers.
    :return: HTTP response content or None if error.
    """
    if not url:
        log_func.warning(u'Not define URL for GET request')
        return None

    try:
        http = urllib3.PoolManager()
        response = http.request('GET', url, headers=headers, **kwargs)
        response_content = response.data.decode('utf-8')
        return response_content
    except:
        log_func.fatal(u'Error GET request by URL <%s> by urllib3' % url)
    return None


def getHTTPSaveFile3(url, dst_filename=None, as_text=False, headers=None, **kwargs):
    """
    GET request HTTP and save to file. urllib3 version.

    :param url: URL.
    :param dst_filename: Destination file name.
        If not defined then generate template filename.
    :param as_text: Write data as text?
    :param headers: Request headers.
    :return: Result filename or None if error.
    """
    if not url:
        log_func.warning(u'Not define URL for GET request')
        return None

    if dst_filename is None:
        dst_filename = file_func.getTempFilename()

    try:
        log_func.info(u'Get <%s> file by URL <%s>...' % (dst_filename, url))
        start_time = time.time()

        http = urllib3.PoolManager()
        response = http.request('GET', url, headers=headers, **kwargs)
        response_content = response.data.decode('utf-8') if as_text else response.data

        file_obj = None
        try:
            file_obj = open(dst_filename, 'wt' if as_text else 'wb')
            file_obj.write(response_content)
            file_obj.close()
        except:
            if file_obj is not None:
                file_obj.close()
            log_func.fatal(u'Error save file <%s>' % dst_filename)

        stop_time = time.time()
        log_func.info(u'... Total time: %s seconds' % (stop_time - start_time))

        if os.path.exists(dst_filename):
            return dst_filename
        else:
            log_func.warning(u'Error save file <%s> by URL <%s>' % (dst_filename, url))
    except:
        log_func.fatal(u'Error GET request by URL <%s> by urllib3' % url)
    return None


def postHTTP3(url, headers=None, body=None, **kwargs):
    """
    POST request HTTP. urllib3 version.

    :param url: URL.
    :param headers: Request headers.
    :param body: Request body.
    :return: HTTP response content or None if error.
    """
    if not url:
        log_func.warning(u'Not define URL for POST request')
        return None

    try:
        encoded_body = json.dumps(body)
        http = urllib3.PoolManager()
        response = http.request('POST', url, headers=headers, body=encoded_body, **kwargs)
        response_content = response.data.decode('utf-8')
        return response_content
    except:
        log_func.fatal(u'Error POST request by URL <%s> by urllib3' % url)
    return None


def deleteHTTP3(url, headers=None, **kwargs):
    """
    DELETE request HTTP. urllib3 version.

    :param url: URL.
    :param headers: Request headers.
    :return: HTTP response code or None if error.
    """
    if not url:
        log_func.warning(u'Not define URL for DELETE request')
        return None

    try:
        http = urllib3.PoolManager()
        response = http.request('DELETE', url, headers=headers, **kwargs)
        response_code = response.status
        return response_code
    except:
        log_func.fatal(u'Error DELETE request by URL <%s> by urllib3' % url)
    return None


def putHTTP3(url, headers=None, fields=None, **kwargs):
    """
    PUT request HTTP. urllib3 version.

    :param url: URL.
    :param fields: Request fields.
    :param headers: Request headers.
    :return: HTTP response code or None if error.
    """
    if not url:
        log_func.warning(u'Not define URL for PUT request')
        return None

    try:
        http = urllib3.PoolManager()
        response = http.request('PUT', url, fields=fields, headers=headers, **kwargs)
        response_code = response.status
        return response_code
    except:
        log_func.fatal(u'Error PUT request by URL <%s> by urllib3' % url)
    return None
