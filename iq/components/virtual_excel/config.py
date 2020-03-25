#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import datetime

# Режим отладки
DEBUG_MODE = True

# Режим журналирования
LOG_MODE = True

# Кодировка консоли по умолчанию
DEFAULT_ENCODING = 'utf-8'

# Имя папки профиля программы
PROFILE_DIRNAME = '.icreport'
# Путь до папки профиля
PROFILE_PATH = os.path.join(os.environ.get('HOME', os.path.dirname(__file__)),
                            PROFILE_DIRNAME)

LOG_FILENAME = os.path.join(PROFILE_PATH,
                            'virtual_excel_%s.log' % datetime.date.today().isoformat())


# Определять адресацию внутри объединенной ячейки как ошибку
DETECT_MERGE_CELL_ERROR = False


def get_cfg_var(name):
    """
    Прочитать значение переменной конфига.

    :type name: C{string}
    :param name: Имя переменной.
    """
    return globals()[name]


def set_cfg_var(name, value):
    """
    Установить значение переменной конфига.

    :type name: C{string}
    :param name: Имя переменной.
    :param value: Значение переменной.
    """
    globals()[name] = value
