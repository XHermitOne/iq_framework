#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Formation of the environment for the work of the editor
of selection criteria for collections.

Filter editor environment.
Format:
{
    'requisites': List of details available for selection,
    'logic': Standard logical operations,
    'funcs': Standart functions,
}

Requisite.
Format:
{
    'name': Requisite name,
    'description': Requisite description,
    'field': Requisite storage field name,
    'type': Requisite type,
    'funcs': Function list,
}

Requisite types:
REQUISITE_TYPE_STR='str' - String
REQUISITE_TYPE_INT='int' - Integer
REQUISITE_TYPE_FLOAT='float' - Float
REQUISITE_TYPE_NUM='number' - Number
REQUISITE_TYPE_DATETIME='datetime' - Datetime
REQUISITE_TYPE_REF='REF' - Reference object

Functions:
    All functions must return a tuple of validation elements 
    in SQL terms
    For example: ('cost','>=','2300.00') or
              ('name','ILIKE(%s)','\'%Company name%\'')

Function registration:
1. Reg function in DEFAULT_ENV_..._FUNCS.
    For example: DEFAULT_ENV_REF_FUNCS
2. Reg function name in DEFAULT_..._FUNCS.
    For example: DEFAULT_REF_FUNCS
3. Reg python function analog in PY_..._FUNCS.
    For example: PY_REF_FUNCS
"""

import wx.adv

from ...util import log_func
from ...util import lang_func
from ...engine.wx import wxbitmap_func

from . import filter_py_funcs
from . import filter_ext_funcs
from . import filter_builder_ctrl

try:
    from ..wx_refobjtreecomboctrl.component import iqWxRefObjTreeComboCtrl
except ImportError:
    log_func.error(u'Reference object choice component not found in filter constructor')
    iqWxRefObjTreeComboCtrl = None

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

REQUISITE_TYPE_STR = 'str'
REQUISITE_TYPE_INT = 'int'
REQUISITE_TYPE_FLOAT = 'float'
REQUISITE_TYPE_NUM = 'number'
REQUISITE_TYPE_D = 'd_text'  # Date as string
REQUISITE_TYPE_DATETIME = 'datetime'
REQUISITE_TYPE_REF = 'REF'  # Ref object

# Dictionary for converting database field types
# to attribute value types
DB_FLD_TYPE2REQUISITE_TYPE = {'Text': REQUISITE_TYPE_STR,
                              'Int': REQUISITE_TYPE_INT,
                              'Float': REQUISITE_TYPE_FLOAT,
                              'Date': REQUISITE_TYPE_D,
                              'DateTime': REQUISITE_TYPE_DATETIME,
                              'REF': REQUISITE_TYPE_REF,
                              }
    
DEFAULT_DATETIME_FORMAT = '%Y.%m.%d %H:%M:%S'


def _getRequisiteField(requisite):
    """
    Define the attribute storage field.
    """
    if ('field' not in requisite) or (not requisite['field']):
        if ('name' not in requisite) or (not requisite['name']):
            log_func.error(u'The attribute storage field is not defined <%s>' % requisite)
            return None
        field = requisite['name'].lower()
    else:
        field = requisite['field']
    return field


def getNumEqual(requisite, value):
    """
    The function of comparing the value of a numerical attribute with a value.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '=', value


def getStrEqual(requisite, value):
    """
    The function of comparing the value of a string attribute with a value.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '=', u'\''+value+u'\''


def getDateTimeEqual(requisite, value):
    """
    The function of comparing the value of a datetime attribute with a value.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '=', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def getEqual(requisite, value):
    """
    The function of comparing the value of props with the specified value.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return getNumEqual(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrEqual(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return getDateTimeEqual(requisite, value)

    # Compare strings by default
    return getStrEqual(requisite, value)


def getNumNotEqual(requisite, value):
    """
    The function of comparing the value of the numerical
    attribute with the specified value for inequality.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '<>', value


def getStrNotEqual(requisite, value):
    """
    The function of comparing the value of the string attribute 
    with the specified value for inequality.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '<>', u'\''+value+u'\''


def getDateTimeNotEqual(requisite, value):
    """
    The function of comparing the datetime attribute
    value with the specified value for inequality.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '<>', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def getNotEqual(requisite, value):
    """
    The function of comparing the value of props
    with the specified value for inequality.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return getNumNotEqual(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrNotEqual(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return getDateTimeNotEqual(requisite, value)

    # Compare strings by default
    return getStrNotEqual(requisite, value)


def getNumGreat(requisite, value):
    """
    The function of comparing the numerical requisite value to > (great).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '>', value


def getStrGreat(requisite, value):
    """
    The function of comparing the string requisite value to > (great).
    
    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '>', u'\''+value+u'\''


def getDateTimeGreat(requisite, value):
    """
    The function of comparing the datetime requisite value to > (great).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '>', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def getGreat(requisite, value):
    """
    The function of comparing the requisite value to > (great).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return getNumGreat(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrGreat(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return getDateTimeGreat(requisite, value)

    # Compare string by default
    return getNumGreat(requisite, value)


def getNumGreatOrEqual(requisite, value):
    """
    The function of comparing the numerical requisite value to >= (great or equal).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '>=', value


def getStrGreatOrEqual(requisite, value):
    """
    The function of comparing the string requisite value to >= (great or equal).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '>=', u'\''+value+u'\''


def getDateTimeGreatOrEqual(requisite, value):
    """
    The function of comparing the datetime requisite value to >= (great or equal).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '>=', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def getGreatOrEqual(requisite, value):
    """
    The function of comparing the requisite value to >= (great or equal).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return getNumGreatOrEqual(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrGreatOrEqual(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return getDateTimeGreatOrEqual(requisite, value)

    # Compare numerical by default
    return getNumGreatOrEqual(requisite, value)


def getNumLesser(requisite, value):
    """
    The function of comparing the numerical requisite value to < (lesser).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '<', value


def getStrLesser(requisite, value):
    """
    The function of comparing the string requisite value to < (lesser).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '<', u'\''+value+u'\''


def getDateTimeLesser(requisite, value):
    """
    The function of comparing the datetime requisite value to < (lesser).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '<', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def getLesser(requisite, value):
    """
    The function of comparing the requisite value to < (lesser).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return getNumLesser(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrLesser(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return getDateTimeLesser(requisite, value)

    # Compare numerical by default
    return getNumLesser(requisite, value)


def getNumLesserOrEqual(requisite, value):
    """
    The function of comparing the numerical requisite value to <= (lesser or equal).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '<=', value


def getStrLesserOrEqual(requisite, value):
    """
    The function of comparing the string requisite value to <= (lesser or equal).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '<=', u'\''+value+u'\''


def getDateTimeLesserOrEqual(requisite, value):
    """
    The function of comparing the datetime requisite value to <= (lesser or equal).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, '<=', '\'%s\'' % value.strftime(DEFAULT_DATETIME_FORMAT)


def getLesserOrEqual(requisite, value):
    """
    The function of comparing the requisite value to <= (lesser or equal).

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return getNumLesserOrEqual(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrLesserOrEqual(requisite, value)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return getDateTimeLesserOrEqual(requisite, value)

    # Compare numerical by default
    return getNumLesserOrEqual(requisite, value)


def getNumBetween(requisite, minimum, maximum):
    """
    The function of comparing the numerical requisite value to BETWEEN.

    :param requisite: Requisite data from the environment.
    :param minimum: Minimum value.
    :param maximum: Maximum value.
    """
    field = _getRequisiteField(requisite)
    return field, 'BETWEEN ', minimum, ' AND ', maximum


def getStrBetween(requisite, minimum, maximum):
    """
    The function of comparing the string requisite value to BETWEEN.

    :param requisite: Requisite data from the environment.
    :param minimum: Minimum value.
    :param maximum: Maximum value.
    """
    field = _getRequisiteField(requisite)
    return field, 'BETWEEN ', u'\''+minimum+u'\'', ' AND ', u'\''+maximum+u'\''


def getDateTimeBetween(requisite, minimum, maximum):
    """
    The function of comparing the datetime requisite value to BETWEEN.

    :param requisite: Requisite data from the environment.
    :param minimum: Minimum value.
    :param maximum: Maximum value.
    """
    field = _getRequisiteField(requisite)
    return field, 'BETWEEN ', \
                  '\'%s\'' % minimum.strftime(DEFAULT_DATETIME_FORMAT), ' AND ', \
                  '\'%s\'' % maximum.strftime(DEFAULT_DATETIME_FORMAT)


def getBetween(requisite, minimum, maximum):
    """
    The function of comparing the requisite value to BETWEEN.

    :param requisite: Requisite data from the environment.
    :param minimum: Minimum value.
    :param maximum: Maximum value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return getNumBetween(requisite, minimum, maximum)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrBetween(requisite, minimum, maximum)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return getDateTimeBetween(requisite, minimum, maximum)

    # Compare string by default
    return getStrBetween(requisite, minimum, maximum)


def getNumNotBetween(requisite, minimum, maximum):
    """
    The function of comparing the numerical requisite value to NOT BETWEEN.

    :param requisite: Requisite data from the environment.
    :param minimum: Minimum value.
    :param maximum: Maximum value.
    """
    field = _getRequisiteField(requisite)
    return 'NOT (', field, 'BETWEEN ', minimum, ' AND ', maximum, ')'


def getStrNotBetween(requisite, minimum, maximum):
    """
    The function of comparing the string requisite value to NOT BETWEEN.

    :param requisite: Requisite data from the environment.
    :param minimum: Minimum value.
    :param maximum: Maximum value.
    """
    field = _getRequisiteField(requisite)
    return 'NOT (', field, 'BETWEEN ', u'\''+minimum+u'\'', ' AND ', u'\''+maximum+u'\'', ')'


def getDateTimeNotBetween(requisite, minimum, maximum):
    """
    The function of comparing the datetime requisite value to NOT BETWEEN.

    :param requisite: Requisite data from the environment.
    :param minimum: Minimum value.
    :param maximum: Maximum value.
    """
    field = _getRequisiteField(requisite)
    return 'NOT (', field, 'BETWEEN ', \
           '\'%s\'' % minimum.strftime(DEFAULT_DATETIME_FORMAT), ' AND ', \
           '\'%s\'' % maximum.strftime(DEFAULT_DATETIME_FORMAT), ')'


def getNotBetween(requisite, minimum, maximum):
    """
    The function of comparing the requisite value to NOT BETWEEN.

    :param requisite: Requisite data from the environment.
    :param minimum: Minimum value.
    :param maximum: Maximum value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return getNumNotBetween(requisite, minimum, maximum)
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrNotBetween(requisite, minimum, maximum)
        elif requisite['type'] == REQUISITE_TYPE_DATETIME:
            return getDateTimeNotBetween(requisite, minimum, maximum)

    # Compare string by default
    return getStrNotBetween(requisite, minimum, maximum)


def getStrContain(requisite, value):
    """
    The function of comparing the string requisite value to CONTAIN.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, 'ILIKE(', '\'%'+value+'%\'', ')'


def getContain(requisite, value):
    """
    The function of comparing the requisite value to CONTAIN.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrContain(requisite, value)
        
    # Compare string by default
    return getStrContain(requisite, value)


def getStrNotContain(requisite, value):
    """ 
    The function of comparing the string requisite value to NOT CONTAIN.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return 'NOT (', field, 'ILIKE(', '\'%'+value+'%\'', '))'


def getNotContain(requisite, value):
    """ 
    The function of comparing the requisite value to NOT CONTAIN.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrNotContain(requisite, value)
        
    # Compare string by default
    return getStrNotContain(requisite, value)


def getStrStartsWith(requisite, value):
    """ 
    The function of comparing the string requisite value to STARTSWITH.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, 'ILIKE(', '\''+value+'%\'', ')'


def getStartsWith(requisite, value):
    """ 
    The function of comparing the requisite value to STARTSWITH.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrStartsWith(requisite, value)
        
    return getStrStartsWith(requisite, value)


def getStrEndsWith(requisite, value):
    """ 
    The function of comparing the string requisite value to ENDSWITH.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, 'ILIKE(', '\'%'+value+'\'', ')'


def getEndsWith(requisite, value):
    """
    The function of comparing the requisite value to ENDSWITH.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrEndsWith(requisite, value)
        
    return getStrEndsWith(requisite, value)


def getStrMask(requisite, value):
    """
    The function of comparing the string requisite value to MASK.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return field, 'ILIKE(', '\''+value+'\'', ')'


def getMask(requisite, value):
    """
    The function of comparing the requisite value to MASK.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrMask(requisite, value)
        
    return getStrMask(requisite, value)


def getStrNotMask(requisite, value):
    """
    The function of comparing the string requisite value to NOT MASK.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    field = _getRequisiteField(requisite)
    return 'NOT (', field, 'ILIKE(', '\''+value+'\'', '))'


def getNotMask(requisite, value):
    """
    The function of comparing the requisite value to MASK.

    :param requisite: Requisite data from the environment.
    :param value: Comparable value.
    """
    if 'type' in requisite and requisite['type']:
        if requisite['type'] in (REQUISITE_TYPE_INT, REQUISITE_TYPE_FLOAT, REQUISITE_TYPE_NUM):
            return None
        elif requisite['type'] == REQUISITE_TYPE_STR:
            return getStrNotMask(requisite, value)
        
    return getStrNotMask(requisite, value)


def getIsNull(requisite):
    """
    The function of comparing the requisite value to NULL.

    :param requisite: Requisite data from the environment.
    """
    field = _getRequisiteField(requisite)
    return field, ' IS NULL'


def getIsNotNull(requisite):
    """
    The function of comparing the requisite value to NOT NULL.

    :param requisite: Requisite data from the environment.
    """
    field = _getRequisiteField(requisite)
    return field, ' IS NOT NULL'


def getInto(requisite, values):
    """
    The function of comparing the requisite value to INTO.

    :param requisite: Requisite data from the environment.
    :param values: Value list.
    """
    field = _getRequisiteField(requisite)
    return field, ' IN ', tuple(values)


def getNotInto(requisite, values):
    """
    The function of comparing the requisite value to NOT INTO.

    :param requisite: Requisite data from the environment.
    :param values: Value list.
    """
    field = _getRequisiteField(requisite)
    return 'NOT (', field, ' IN ', tuple(values), ')'


# Logic operation
LOGIC_OPERATION = {'name': 'AND',
                   'description': _(u'AND'),
                   }

# Filter function in the collection selection editor
FILTER_FUNC = {'function': None,     # Function object
               'description': None,
               'args': list(),       # Function argument list
               }

# Function argument in the collection selection editor
FILTER_ARG = {'name': None,         # Argument name
              'description': None,  # Description
              'ext_edit': None,     # Class advanced argument value editor
              'ext_args': None,     # Advanced editor class constructor arguments
              'ext_kwargs': None,   # Advanced editor class constructor arguments
              }
    
# Requisite in the collection selection editor
FILTER_REQUISITE = {'name': None,         # Requisite name
                    'description': None,  # Description
                    'field': None,        # Requisite store field
                    'type': None,         # Requisite type
                    'funcs': [],          # Function list
                    }

# Standart logic operations
DEFAULT_ENV_LOGIC_OPERATIONS = [
    {'name': 'AND', 'description': _(u'AND'), 'img': wxbitmap_func.createIconBitmap('logic_and')},
    {'name': 'OR', 'description': _(u'OR'), 'img': wxbitmap_func.createIconBitmap('logic_or')},
    {'name': 'NOT', 'description': _(u'NOT'), 'img': wxbitmap_func.createIconBitmap('logic_not_and')},
    {'name': 'NOT OR', 'description': _(u'NOT OR'), 'img': wxbitmap_func.createIconBitmap('logic_not_or')},
    ]
    
# Standart functions
DEFAULT_ENV_FUNCS = {
    'equal': {
        'name': 'equal',
        'function': getEqual,
        'description': _(u'Equal'),
        'args': [
                {'name': 'value',
                 'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },
        
    'not_equal': {
        'name': 'not_equal',
        'function': getNotEqual,
        'description': _(u'Not equal'),
        'args': [
                 {'name': 'value',
                  'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_not_equal'),
        },
        
    'great': {
        'name': 'great',
        'function': getGreat,
        'description': _(u'Great'),
        'args': [
            {'name': 'value',
             'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_great'),
        },
        
    'great_or_equal': {
        'name': 'great_or_equal',
        'function': getGreatOrEqual,
        'description': _(u'Great or equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_great_or_equal'),
        },
        
    'lesser': {
        'name': 'lesser',
        'function': getLesser,
        'description': _(u'Lesser'),
        'args': [
            {'name': 'value',
             'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_lesser'),
        },
        
    'lesser_or_equal': {
        'name': 'lesser_or_equal',
        'function': getLesserOrEqual,
        'description': _(u'Lesser or equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_lesser_or_equal'),
        },
        
    'between': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Between'),
        'args': [
            {'name': 'minimum',
             'description': _(u'Minimum value')},
            {'name': 'maximum',
             'description': _(u'Maximum value')},
            ],
        'img': wxbitmap_func.createIconBitmap('logic_between'),
        },
    
    'not_between': {
        'name': 'not_between',
        'function': getNotBetween,
        'description': _(u'Not between'),
        'args': [
            {'name': 'minimum',
             'description': _(u'Minimum value')},
            {'name': 'maximum',
             'description': _(u'Maximum value')},
            ],
        'img': wxbitmap_func.createIconBitmap('logic_not_between'),
        },
        
    'contain': {
        'name': 'contain',
        'function': getContain,
        'description': _(u'Contain'),
        'args': [
            {'name': 'value',
             'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_contain'),
        },

    'not_contain': {
        'name': 'not_contain',
        'function': getNotContain,
        'description': _(u'Not contain'),
        'args': [
            {'name': 'value',
             'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_not_contain'),
        },
        
    'startswith': {
        'name': 'startswith',
        'function': getStartsWith,
        'description': _(u'Starts with'),
        'args': [
            {'name': 'value',
             'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_left_equal'),
        },

    'endswith': {
        'name': 'endswith',
        'function': getEndsWith,
        'description': _(u'Ends with'),
        'args': [
            {'name': 'value',
             'description': _(u'Value')}],
        'img': wxbitmap_func.createIconBitmap('logic_right_equal'),
        },

    'mask': {
        'name': 'mask',
        'function': getMask,
        'description': _(u'Matches the mask'),
        'args': [
            {'name': 'value',
             'description': _(u'Mask')}],
        'img': wxbitmap_func.createIconBitmap('logic_mask'),
        },
        
    'not_mask': {
        'name': 'not_mask',
        'function': getNotMask,
        'description': _(u'Does not match the mask'),
        'args': [
            {'name': 'value',
             'description': _(u'Mask')}],
        'img': wxbitmap_func.createIconBitmap('logic_not_mask'),
        },
        
    'is_null': {
        'name': 'is_null',
        'function': getIsNull,
        'description': _(u'Is NULL'),
        'args': [],
        'img': wxbitmap_func.createIconBitmap('logic_is_null'),
        },
        
    'is_not_null': {
        'name': 'is_not_null',
        'function': getIsNotNull,
        'description': _(u'Is not NULL'),
        'args': [],
        'img': wxbitmap_func.createIconBitmap('logic_is_not_null'),
        },
        
    'into': {
        'name': 'into',
        'function': getInto,
        'description': _(u'Any of'),
        'args': [
            {'name': 'values',
             'description': _(u'Value list')}],
        'img': wxbitmap_func.createIconBitmap('logic_into'),
        },
        
    'not_into': {
        'name': 'not_into',
        'function': getNotInto,
        'description': _(u'Not one of'),
        'args': [
            {'name': 'values',
             'description': _(u'Value list')}],
        'img': wxbitmap_func.createIconBitmap('logic_not_into'),
        },
        
    }
    
DEFAULT_STRING_FUNCS = ('equal', 'not_equal', 
                        'contain', 'not_contain',
                        'startswith', 'endswith',
                        # 'mask','not_mask',
                        'is_null', 'is_not_null', 
                        'into', 'not_into')
    
PY_STRING_FUNCS = {
    'equal': filter_py_funcs.pyEqual,
    'not_equal': filter_py_funcs.pyNotEqual,
    'contain': filter_py_funcs.pyContain,
    'not_contain': filter_py_funcs.pyNotContain,
    'startswith': filter_py_funcs.pyStartsWith,
    'endswith': filter_py_funcs.pyEndsWith,
    'mask': filter_py_funcs.pyMask,
    'not_mask': filter_py_funcs.pyNotMask,
    'is_null': filter_py_funcs.pyIsNull,
    'is_not_null': filter_py_funcs.pyNotNull,
    'into': filter_py_funcs.pyInto,
    'not_into': filter_py_funcs.pyNotInto,
}
    
DEFAULT_NUMBER_FUNCS = ('equal', 'not_equal', 'lesser', 'lesser_or_equal',
                        'great', 'great_or_equal', 
                        'between', 'not_between',
                        'is_null', 'is_not_null')

PY_NUMBER_FUNCS = {
    'equal': filter_py_funcs.pyEqual,
    'not_equal': filter_py_funcs.pyNotEqual,
    'lesser': filter_py_funcs.pyLesser,
    'lesser_or_equal': filter_py_funcs.pyLesserOrEqual,
    'great': filter_py_funcs.pyGreat,
    'great_or_equal': filter_py_funcs.pyGreatOrEqual,
    'between': filter_py_funcs.pyBetween,
    'not_between': filter_py_funcs.pyNotBetween,
    'is_null': filter_py_funcs.pyIsNull,
    'is_not_null': filter_py_funcs.pyNotNull,
    }


DEFAULT_DATE_FUNCS = ('date_equal', 'date_not_equal', 'date_lesser', 'date_lesser_or_equal',
                      'date_great', 'date_great_or_equal', 'date_between', 'date_not_between',
                      'is_null', 'is_not_null',
                      # Additional functions
                      'sys_date',   # System day
                      'sys_month',  # System month
                      'sys_year',   # System year
                      'choice_date',    # Date
                      'choice_month',   # Month
                      'choice_year',    # Year
                      'choice_date_range',    # Date range
                      'choice_month_range',   # Month range
                      )

PY_DATE_FUNCS = {
    'equal': filter_py_funcs.pyEqual,
    'not_equal': filter_py_funcs.pyNotEqual,
    'lesser': filter_py_funcs.pyLesser,
    'lesser_or_equal': filter_py_funcs.pyLesserOrEqual,
    'great': filter_py_funcs.pyGreat,
    'great_or_equal': filter_py_funcs.pyGreatOrEqual,
    'between': filter_py_funcs.pyBetween,
    'not_between': filter_py_funcs.pyNotBetween,
    'startswith': filter_py_funcs.pyStartsWith,
    'endswith': filter_py_funcs.pyEndsWith,
    'is_null': filter_py_funcs.pyIsNull,
    'is_not_null': filter_py_funcs.pyNotNull,
    }


DEFAULT_DATETIME_FUNCS = ('datetime_equal', 'datetime_not_equal', 
                          'datetime_lesser', 'datetime_lesser_or_equal',
                          'datetime_great', 'datetime_great_or_equal', 
                          'datetime_between', 'datetime_not_between',
                          'is_null', 'is_not_null',
                          # Additional functions
                          'datetime_sys_date',   # System day
                          'datetime_yesterday',   # Yesterday
                          'datetime_two_days_ago',   # Two days ago
                          'datetime_sys_month',  # System month
                          'datetime_sys_year',   # System year
                          'datetime_oper_year',   # Operational year
                          'datetime_choice_date',    # Date
                          'datetime_choice_month',   # Month
                          'datetime_choice_year',    # Year
                          'datetime_choice_date_range',    # Date range
                          'datetime_choice_month_range',   # Month range
                          )

PY_DATETIME_FUNCS = {
    'equal': filter_py_funcs.pyDateTimeEqual,
    'not_equal': filter_py_funcs.pyDateTimeNotEqual,
    'lesser': filter_py_funcs.pyDateTimeLesser,
    'lesser_or_equal': filter_py_funcs.pyDateTimeLesserOrEqual,
    'great': filter_py_funcs.pyDateTimeGreat,
    'great_or_equal': filter_py_funcs.pyDateTimeGreatOrEqual,
    'between': filter_py_funcs.pyDateTimeBetween,
    'not_between': filter_py_funcs.pyDateTimeNotBetween,
    'is_null': filter_py_funcs.pyDateTimeIsNull,
    'is_not_null': filter_py_funcs.pyDateTimeNotNull,
    }


DEFAULT_REF_FUNCS = ('nsi_equal', 'nsi_not_equal', 'nsi_left_equal',)


PY_NSI_FUNCS = {
    'nsi_equal': filter_py_funcs.pyEqual,
    'nsi_not_equal': filter_py_funcs.pyNotEqual,
    'nsi_left_equal': filter_py_funcs.pyStartsWith,
    }


PY_FUNCS = {
    REQUISITE_TYPE_STR: PY_STRING_FUNCS,
    REQUISITE_TYPE_INT: PY_NUMBER_FUNCS,
    REQUISITE_TYPE_FLOAT: PY_NUMBER_FUNCS,
    REQUISITE_TYPE_NUM: PY_NUMBER_FUNCS,
    REQUISITE_TYPE_D: PY_DATE_FUNCS,
    REQUISITE_TYPE_DATETIME: PY_DATETIME_FUNCS,
    REQUISITE_TYPE_REF: PY_NSI_FUNCS,
}
    
   
# Environment of collection selection criteria editor
FILTER_ENVIRONMENT = {
    'requisites': [],  # Requisite list
    'logic': DEFAULT_ENV_LOGIC_OPERATIONS,  # Standart logic operations
    'funcs': DEFAULT_ENV_FUNCS,  # Standart functions
    }


# Standard functions used for date details
DEFAULT_ENV_DATE_FUNCS = {
    'date_equal': {
        'name': 'equal',
        'function': getEqual,
        'description': _(u'Equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },
        
    'date_not_equal': {
        'name': 'not_equal',
        'function': getNotEqual,
        'description': _(u'Not equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_not_equal'),
        },
        
    'date_great': {
        'name': 'great',
        'function': getGreat,
        'description': _(u'Great'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_great'),
        },
        
    'date_great_or_equal': {
        'name': 'great_or_equal',
        'function': getGreatOrEqual,
        'description': _(u'Great or equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_great_or_equal'),
        },
        
    'date_lesser': {
        'name': 'lesser',
        'function': getLesser,
        'description': _(u'Lesser'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_lesser'),
        },
        
    'date_lesser_or_equal': {
        'name': 'lesser_or_equal',
        'function': getLesserOrEqual,
        'description': _(u'Lesser or equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_lesser_or_equal'),
        },
        
    'date_between': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Between'),
        'args': [
            {'name': 'minimum',
             'description': _(u'Minimum value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             },
            {'name': 'maximum',
             'description': _(u'Maximum value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             },
            ],
        'img': wxbitmap_func.createIconBitmap('logic_between'),
        },
    
    'date_not_between': {
        'name': 'not_between',
        'function': getNotBetween,
        'description': _(u'Not between'),
        'args': [
            {'name': 'minimum',
             'description': _(u'Minimum value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             },
            {'name': 'maximum',
             'description': _(u'Maximum value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             },
            ],
        'img': wxbitmap_func.createIconBitmap('logic_not_between'),
        },

    # --- Additional functions ---

    'sys_date': {
        'name': 'equal',
        'function': getEqual,
        'description': _(u'System data'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsSysDate,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },

    'sys_month': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'System month'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsSysMonth,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },

    'sys_year': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'System year'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsSysYear,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },

    'choice_date': {
        'name': 'equal',
        'function': getEqual,
        'description': _(u'Date'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceDate,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },

    'choice_month': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Month'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceMonth,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },

    'choice_year': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Year'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceYear,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },

    'choice_date_range': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Date range'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceDateRange,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },

    'choice_month_range': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Month range'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceMonthRange,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },

    }

DEFAULT_ENV_FUNCS.update(DEFAULT_ENV_DATE_FUNCS)

# Standard functions used for datetime details
DEFAULT_ENV_DATETIME_FUNCS = {
    'datetime_equal': {
        'name': 'equal',
        'function': getEqual,
        'description': _(u'Equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_not_equal': {
        'name': 'not_equal',
        'function': getNotEqual,
        'description': _(u'Not equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_not_equal'),
    },

    'datetime_great': {
        'name': 'great',
        'function': getGreat,
        'description': _(u'Great'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_great'),
    },

    'datetime_great_or_equal': {
        'name': 'great_or_equal',
        'function': getGreatOrEqual,
        'description': _(u'Great or equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_great_or_equal'),
    },

    'datetime_lesser': {
        'name': 'lesser',
        'function': getLesser,
        'description': _(u'Lesser'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_lesser'),
    },

    'datetime_lesser_or_equal': {
        'name': 'lesser_or_equal',
        'function': getLesserOrEqual,
        'description': _(u'Lesser or equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_lesser_or_equal'),
    },

    'datetime_between': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Between'),
        'args': [
            {'name': 'minimum',
             'description': _(u'Minimum value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             },
            {'name': 'maximum',
             'description': _(u'Maximum value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             },
        ],
        'img': wxbitmap_func.createIconBitmap('logic_between'),
    },

    'datetime_not_between': {
        'name': 'not_between',
        'function': getNotBetween,
        'description': _(u'Not between'),
        'args': [
            {'name': 'minimum',
             'description': _(u'Minimum value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             },
            {'name': 'maximum',
             'description': _(u'Maximum value'),
             'ext_edit': filter_builder_ctrl.iqDateArgExtEdit,
             'ext_kwargs': {'component': {'style': wx.adv.DP_DROPDOWN}}
             },
        ],
        'img': wxbitmap_func.createIconBitmap('logic_not_between'),
    },

    # --- Additional functions ---

    'datetime_sys_date': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'System date'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsSysDateDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_yesterday': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Yesterday'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsYesterdayDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_two_days_ago': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Two days ago'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsTwoDaysAgoDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_sys_month': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'System month'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsSysMonthDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_sys_year': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'System year'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsSysYearDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_oper_year': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Operational year'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsOperYearDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_choice_date': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Date'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceDateDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_choice_month': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Month'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceMonthDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_choice_year': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Year'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceYearDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_choice_date_range': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Date range'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceDateRangeDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

    'datetime_choice_month_range': {
        'name': 'between',
        'function': getBetween,
        'description': _(u'Month range'),
        'args': [],
        'get_args': filter_ext_funcs.getArgsChoiceMonthRangeDatetime,
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
    },

}

DEFAULT_ENV_FUNCS.update(DEFAULT_ENV_DATETIME_FUNCS)

DEFAULT_ENV_REF_FUNCS = {
    'nsi_equal': {
        'name': 'equal',
        'function': getEqual,
        'description': _(u'Equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': iqWxRefObjTreeComboCtrl,
             'ext_kwargs': {'component': {}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_equal'),
        },
        
    'nsi_not_equal': {
        'name': 'not_equal',
        'function': getNotEqual,
        'description': _(u'Not equal'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': iqWxRefObjTreeComboCtrl,
             'ext_kwargs': {'component': {}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_not_equal'),
        },

    'nsi_left_equal': {
        'name': 'startswith',
        'function': getStartsWith,
        'description': _(u'Group'),
        'args': [
            {'name': 'value',
             'description': _(u'Value'),
             'ext_edit': iqWxRefObjTreeComboCtrl,
             'ext_kwargs': {'component': {}}
             }],
        'img': wxbitmap_func.createIconBitmap('logic_left_equal'),
        },
    }

DEFAULT_ENV_FUNCS.update(DEFAULT_ENV_REF_FUNCS)

DEFAULT_FUNCS = {
    REQUISITE_TYPE_STR: DEFAULT_STRING_FUNCS,
    REQUISITE_TYPE_INT: DEFAULT_NUMBER_FUNCS,
    REQUISITE_TYPE_FLOAT: DEFAULT_NUMBER_FUNCS,
    REQUISITE_TYPE_NUM: DEFAULT_NUMBER_FUNCS,
    REQUISITE_TYPE_D: DEFAULT_DATE_FUNCS,
    REQUISITE_TYPE_DATETIME: DEFAULT_DATETIME_FUNCS,
    REQUISITE_TYPE_REF: DEFAULT_REF_FUNCS,
}

DEFAULT_ALL_FUNCS = tuple(DEFAULT_ENV_FUNCS.keys())
