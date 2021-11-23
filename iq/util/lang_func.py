#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Internationalization functions.
"""

import gettext
import locale

from . import log_func

__version__ = (0, 0, 1, 1)

TEXT_DOMAIN = 'iq'
DEFAULT_LOCALE_DIR = 'locale'

RUSSIAN_LOCALE = 'ru_RU'

TRANSLATIONS = dict()


def getTranslation(language=None):
    """
    Get translation object.

    :param language: Language (For example 'ru', 'en' and etc).
    :return: Translation object.
    """
    global TRANSLATIONS

    if language is None:
        language = locale.getlocale()[0]

    if language in TRANSLATIONS:
        return TRANSLATIONS[language]
    elif gettext.find(TEXT_DOMAIN, localedir=DEFAULT_LOCALE_DIR, languages=[language]):
        translation = gettext.translation(TEXT_DOMAIN,
                                          localedir=DEFAULT_LOCALE_DIR,
                                          languages=[language])
        translation.install()
        log_func.info(u'GETTEXT. Install traslation for language <%s>' % language)
        TRANSLATIONS[language] = translation
        return translation
    else:
        log_func.warning(u'GETTEXT. Language <%s> not found' % language)
    return gettext
