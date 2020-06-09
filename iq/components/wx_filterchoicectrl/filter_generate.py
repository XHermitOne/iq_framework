#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter generation functions.

For example:
    createFilterGroupAND(createFilterCompareRequisite('field1', '==', 'FFF'))

A filter is a dictionary-list structure consisting of
structures of two types of objects: group and props.

Group - a structure that describes the grouping of parenthesized elements and
connected by one logical operand (AND, OR, NOT).

Group format:
{
 'name': Group name. Usually corresponds to a logical operand.
 'type': Group type. <group> string.
 'logic': Logical operand. AND/OR/NOT.
 'children': Requisite list.
}

Requisite - the structure describing the group element corresponds to
table field. In addition to specifying a field, it includes a comparison operator
and arguments to the comparison operator.

Requisite format:
{
 'requisite': Requisite name. Usually matches the table field name.
 'type': Requisite type. <compare> string.
 'arg_1': Argument 1 value.
 'arg_2': Argument 2 value.
 'get_args': An additional function to get arguments.
 'function': Compare function name.
            The comparison function is selected by name from the dictionary
            of comparison functions filter_builder_env.DEFAULT_ENV_FUNCS.
 '__sql__': Element tuple sql expressions corresponding to this attribute.
            Therefore, the WHERE generation of the SQL section is
            to correctly join the necessary rows of this key.
}
"""

import copy

__version__ = (0, 0, 0, 1)


def createFilterGroup(logic='AND', *compare_requisites):
    """
    Create filter group.

    :param logic: Logical operand.
    :param compare_requisites: Filter requisite list.
    :return: Group data:
        {
        'name': Group name. Usually corresponds to a logical operand.
        'type': Group type. <group> string.
        'logic': Logical operand. AND/OR/NOT.
        'children': Requisite list.
        }
    """
    compare_requisites = [requisite for requisite in compare_requisites if requisite]
    filter_grp = dict(name=logic, type='group',
                      logic=logic, children=compare_requisites)
    return filter_grp


def createFilterGroupAND(*compare_requisites):
    """
    Create filter group with logical operand <AND>.

    :param compare_requisites: Filter requisite list.
    :return: Group data:
        {
        'name': Group name. Usually corresponds to a logical operand.
        'type': Group type. <group> string.
        'logic': Logical operand. AND/OR/NOT.
        'children': Requisite list.
        }
    """
    return createFilterGroup('AND', *compare_requisites)


def createFilterGroupOR(*compare_requisites):
    """
    Create filter group with logical operand <OR>.

    :param compare_requisites: Filter requisite list.
    :return: Group data:
        {
        'name': Group name. Usually corresponds to a logical operand.
        'type': Group type. <group> string.
        'logic': Logical operand. AND/OR/NOT.
        'children': Requisite list.
        }
    """
    return createFilterGroup('OR', *compare_requisites)


def createFilterGroupNOT(*compare_requisites):
    """
    Create filter group with logical operand <NOT>.

    :param compare_requisites: Filter requisite list.
    :return: Group data:
        {
        'name': Group name. Usually corresponds to a logical operand.
        'type': Group type. <group> string.
        'logic': Logical operand. AND/OR/NOT.
        'children': Requisite list.
        }
    """
    return createFilterGroup('NOT', *compare_requisites)


# Compare operations analogs
EQUAL_COMPARE = '=='
NOT_EQUAL_COMPARE = '<>'
LESSER_OR_EQUAL_COMPARE = '<='
GREAT_OR_EQUAL_COMPARE = '>='
GREAT_COMPARE = '>'
LESSER_COMPARE = '<'
BETWEEN_COMPARE = '>..<'
NOT_BETWEEN_COMPARE = '.<>.'
IS_NULL_COMPARE = 'N'
STARTSWITH_COMPARE = '..)'
ENDSWITH_COMPARE = '(..'
CONTAIN_COMPARE = '(..)'

COMPARE_OPERATION_TRANSLATE = {'==': 'equal',
                               '<>': 'not_equal',
                               '<=': 'lesser_or_equal',
                               '>=': 'great_or_equal',
                               '>': 'great',
                               '<': 'lesser',
                               '>..<': 'between',
                               '.<>.': 'not_between',
                               'N': 'is_null',

                               '..)': 'startswith',
                               '(..': 'endswith',
                               '(..)': 'contain',
                               }

DEFAULT_COMPARE_OPERATE = EQUAL_COMPARE


def createFilterCompareRequisite(name, compare_operate=DEFAULT_COMPARE_OPERATE,
                                 arg_1=None, arg_2=None):
    """
    Create filter requisite.

    :param name: Requisite name. Usually matches the table field name.
    :param compare_operate: Compare operations.
    :param arg_1: Argument 1 value.
    :param arg_2: Argument 2 value.
    :return: Requisite data:
        {
        'requisite': Requisite name. Usually matches the table field name.
        'type': Requisite type. <compare> string.
        'arg_1': Argument 1 value.
        'arg_2': Argument 2 value.
        'get_args': An additional function to get arguments.
        'function': Compare function name.
                    The comparison function is selected by name from the dictionary
                    of comparison functions filter_builder_env.DEFAULT_ENV_FUNCS.
        '__sql__': Element tuple sql expressions corresponding to this attribute.
                   Therefore, the WHERE generation of the SQL section is
                   to correctly join the necessary rows of this key.
        }
    """
    compare_func = COMPARE_OPERATION_TRANSLATE.get(compare_operate, compare_operate)
    filter_compare = dict(requisite=name, type='compare',
                          arg_1=arg_1, arg_2=arg_2,
                          function=compare_func)
    return filter_compare


def addFilterCompareToGroup(filter_group, filter_compare, do_clone=False):
    """
    Add filter requisite into filter group.

    :param filter_group: Filter group data:
        {
        'name': Group name. Usually corresponds to a logical operand.
        'type': Group type. <group> string.
        'logic': Logical operand. AND/OR/NOT.
        'children': Requisite list.
        }
    :param filter_compare: Filter requisite compare data:
        {
        'requisite': Requisite name. Usually matches the table field name.
        'type': Requisite type. <compare> string.
        'arg_1': Argument 1 value.
        'arg_2': Argument 2 value.
        'get_args': An additional function to get arguments.
        'function': Compare function name.
                    The comparison function is selected by name from the dictionary
                    of comparison functions filter_builder_env.DEFAULT_ENV_FUNCS.
        '__sql__': Element tuple sql expressions corresponding to this attribute.
                   Therefore, the WHERE generation of the SQL section is
                   to correctly join the necessary rows of this key.
        }
    :param do_clone: Pre-clone source group?
    :return: Filled filter group data:
        {
        'name': Group name.
        'type': Group type. <group> string.
        'logic': Logical operand. AND/OR/NOT.
        'children': [... { Filter requisite }]
        }
    """
    if do_clone:
        filter_group = copy.deepcopy(filter_group)

    if not filter_compare:
        # We do not add empty filter details
        return filter_group

    if filter_group and isinstance(filter_group, dict):
        if ('children' not in filter_group) or (filter_group['children'] is None):
            filter_group['children'] = list()

        if isinstance(filter_group['children'], list):
            filter_group['children'].append(filter_compare)
        elif isinstance(filter_group['children'], tuple):
            filter_group['children'] = list(filter_group['children'])
            filter_group['children'].append(filter_compare)

    return filter_group
