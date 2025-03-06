#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Internationalization functions.
"""

import gettext
import locale
import os.path

from . import log_func
from . import sys_func

__version__ = (0, 1, 2, 1)

TEXT_DOMAIN = 'iq'
DEFAULT_LOCALE_DIR = 'locale'
DEFAULT_LOCALE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   DEFAULT_LOCALE_DIR)

DEFAULT_LOCALE = 'en_US'
RUSSIAN_LOCALE = 'ru_RU'

ENGLISH_LANGUAGE = 'en'
RUSSIAN_LANGUAGE = 'ru'

TRANSLATIONS = dict()

WINDOWS2UNIX_LANGUAGE = {
    'Russian_Russia': RUSSIAN_LOCALE,
}


def getDefaultLocaleLanguage():
    """
    Get default locale language.

    :return: Locale language as string.
        For Unix and Windows should be the same.
    """
    # Setup textdomain
    try:
        locale.bindtextdomain(TEXT_DOMAIN, DEFAULT_LOCALE_PATH)
    except AttributeError:
        log_func.warning(u'Locale module not support text domain')

    language = locale.getlocale()[0]

    if sys_func.isWindowsPlatform():
        if language in WINDOWS2UNIX_LANGUAGE:
            language = WINDOWS2UNIX_LANGUAGE.get(language, DEFAULT_LOCALE)
        else:
            try:
                item1, item2 = language.split('_')
                language = '_'.join((item1[:2].lower(), item2[:2].upper()))
            except:
                log_func.fatal(u'Error get language')
                language = DEFAULT_LOCALE
    return language


def getTranslation(language=None):
    """
    Get translation object.

    :param language: Language (For example 'ru', 'en' and etc).
    :return: Translation object.
    """
    global TRANSLATIONS

    if language is None:
        language = getDefaultLocaleLanguage()

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


def isNotEnglishText(text):
    """
    Is this not an English text?
    """
    if isinstance(text, str):
        not_english = any([ord(c) > 128 for c in text])
        return not_english
    # Not string
    return False
