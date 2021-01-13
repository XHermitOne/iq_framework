#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции получения/определения иконок маркеров.
"""

import os.path
from ...util import log_func

__version__ = (0, 1, 1, 1)

ICON_FILENAME_EXT = '.png'

# Последовательность имет цветов маркеров по умолчанию
DEFAULT_COLOR_NAMES_SEQUENCE = ('blue', 'green', 'yellow', 'red', 'cyan', 'magenta', 'gray')


def get_marker_icon_filename(icon_name):
    """
    Получить полное имя файла иконки маркера.
    :param icon_name: Имя иконки.
        Может задаваться как имя (например marker) или базовое имя файла (например marker.png).
    :return: Полное имя файла или None в случае ошибки.
    """
    if not isinstance(icon_name, str):
        log_func.warning(u'Не корректный тип <%s> имени иконки' % icon_name.__class__.__name__)
        return None

    if not icon_name.endswith(ICON_FILENAME_EXT):
        icon_name += ICON_FILENAME_EXT

    filename = os.path.join(os.path.dirname(__file__), 'img', icon_name)
    return filename

