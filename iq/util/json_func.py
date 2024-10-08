#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JSON convert functions.
"""

import json
import os
import os.path

from . import log_func
from . import file_func

try:
    import urllib.request
except ImportError:
    log_func.error(u'Import error urllib')

try:
    import urllib3
except ImportError:
    log_func.error(u'Import error urllib3')


__version__ = (0, 0, 1, 4)


def dict2JSON(data_dict):
    """
    Python dictionary convert to JSON.

    :param data_dict: Puthon dictionary.
    :return: JSON structure.
    """
    return json.dumps(data_dict)


def JSON2dict(data_json):
    """
    JSON structure convert to Python dictionary.

    :param data_json: JSON structure.
    :return: Python dictionary.
    """
    return json.loads(data_json)


def saveDictAsJSON(json_filename, data_dict, rewrite=True):
    """
    Save JSON to file.

    :param json_filename: JSON filename.
    :param data_dict: Python dictionary.
    :param rewrite: Overwrite file if already exists?
    :return: True/False.
    """
    if rewrite and os.path.exists(json_filename):
        try:
            os.remove(json_filename)
        except:
            log_func.fatal(u'Error delete JSON file <%s>' % json_filename)
            return False

    write_file = None
    try:
        # Check json dir name
        json_dirname = os.path.dirname(json_filename)
        if not os.path.exists(json_dirname):
            file_func.createDir(json_dirname)

        write_file = open(json_filename, 'w')
        json.dump(data_dict, write_file, indent=4)
        write_file.close()
        return True
    except:
        if write_file:
            write_file.close()
        log_func.fatal(u'Error save JSON file <%s>' % json_filename)
    return False


def getJSONAsDictByURL(url, *args, **kwargs):
    """
    Get JSON data as python dictionary by URL.

    :param url: URL.
    :return: JSON python dictionary or None if error.
    """
    if not url:
        log_func.warning(u'Not define URL for get JSON data')
        return None

    try:
        response = urllib.request.urlopen(url, *args, **kwargs)
        json_content = response.read()
        json_dict = json.loads(json_content)
        return json_dict
    except:
        log_func.fatal(u'Error get JSON data by URL <%s>' % url)
    return None


def getJSONAsDictByURL3(url, headers=None, *args, **kwargs):
    """
    Get JSON data as python dictionary by URL. urllib3 version.

    :param url: URL.
    :param headers: Request headers.
    :return: JSON python dictionary or None if error.
    """
    if not url:
        log_func.warning(u'Not define URL for get JSON data')
        return None

    json_content = None
    try:
        http = urllib3.PoolManager()
        response = http.request('GET', url, headers=headers)
        json_content = response.data.decode('utf-8')
        json_dict = json.loads(json_content)
        return json_dict
    except:
        log_func.fatal(u'Error get JSON data by URL <%s> by urllib3' % url)
        if json_content:
            log_func.error(u'JSON content:')
            log_func.error(json_content)
        else:
            log_func.error(u'JSON content: <%s>' % str(json_content))
    return None
