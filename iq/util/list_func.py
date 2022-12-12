#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Additional list processing functions.
"""

import operator
import functools

__version__ = (0, 0, 0, 1)


def sortMultiKey(items, keys):
    """
    Sophisticated sorting of a dictionary list.
    Source: https://wiki.python.org/moin/SortingListsOfDictionaries
    For example:
        result = sortMultiKey(undecorated, ['key1', 'key2', 'key3'])
        result = sortMultiKey(undecorated, ['-key1', '-key2', '-key3'])

    :param items: List of dictionaries.
    :param keys: Key sorting order.
    :return: Sorted list.
    """
    comparers = [((operator.itemgetter(key[1:].strip()), -1) if key.startswith('-') else (operator.itemgetter(key.strip()), 1)) for key in
                 keys]

    def comparer(left, right):
        """
        Compare function.

        :param left: Value on the left for comparison.
        :param right: Value on the right for comparison.
        :return:
        """
        for fn, mult in comparers:
            fn_left = fn(left)
            fn_right = fn(right)
            # This is an expression to replace cmp function from Python2
            #                        V
            result = (fn_left > fn_right) - (fn_left < fn_right)

            if result:
                return mult * result
        else:
            return 0

    return sorted(items, key=functools.cmp_to_key(comparer))


AND_COMPARE_SIGNATURE = 'AND'
OR_COMPARE_SIGNATURE = 'OR'


def filterMultiKey(items, finds, compare=AND_COMPARE_SIGNATURE):
    """
    Filtering the list of dictionaries by the values of several keys.

    :param items: List of dictionaries.
    :param finds: Key values dictionary.
    :param compare: Comparison method AND or OR.
    :return: List of filtered dictionaries.
    """
    result = list()
    if compare == AND_COMPARE_SIGNATURE:
        result = [item for item in items if all([item.get(key, None) == value for key, value in finds.items()])]
    elif compare == OR_COMPARE_SIGNATURE:
        result = [item for item in items if any([item.get(key, None) == value for key, value in finds.items()])]
    else:
        pass
    return result


def findMultiKey(items, find_keys, compare=AND_COMPARE_SIGNATURE):
    """
    Find the list of dictionaries for the values of several keys.

    :param items: List of dictionaries.
    :param find_keys: Key values dictionary.
    :param compare: Comparison method AND or OR.
    :return: Dictionary found or None if nothing is found.
    """
    filter_items = filterMultiKey(items, find_keys, compare)
    return filter_items[0] if filter_items else None


def findMultiKeyIdx(items, find_keys, compare=AND_COMPARE_SIGNATURE):
    """
    Find index the list of dictionaries for the values of several keys.

    :param items: List of dictionaries.
    :param find_keys: Key values dictionary.
    :param compare: Comparison method AND or OR.
    :return: Index or -1 if nothing is found.
    """
    filter_items = filterMultiKey(items, find_keys, compare)
    find_dict = filter_items[0] if filter_items else None
    if find_dict:
        return items.index(find_dict)
    return -1


def findTextRowIdx(items, find_text, start_row=0, compare_contain=True):
    """
    Find row index the list of dictionaries row.

    :param items: List of dictionaries.
    :param find_text: Find text.
    :param start_row: Start row.
    :param compare_contain: Comparison on the content of the text?
    :return: Index or -1 if nothing is found.
    """
    for i_row, row in enumerate(items):
        if i_row >= start_row:
            for value in row.values():
                find = (find_text in str(value)) if compare_contain else (find_text == str(value))
                if find:
                    return i_row
    return -1


def findTextInListIdx(items, find_text, compare_contain=True):
    """
    Find index in the list.

    :param items: List of strings.
    :param find_text: Find text
    :param compare_contain: Comparison on the content of the text?
    :return: Index or -1 if nothing is found.
    """
    for i, value in enumerate(items):
        find = (find_text in str(value)) if compare_contain else (find_text == str(value))
        if find:
            return i
    return -1


def dataset2queryTable(dataset):
    """
    Convert dataset format data to query table format data.

    :param dataset: Dataset format data:
        [
        {'column1 name': value1, 'column2 name': value1, ...},
        ...
        ]
    :return: Query table format data:
        {
        '__fields__': ('column1 name', 'column2 name', ...),
        '__data__': [
            (value1, value2, ...),
            ...
            ]
        }
    """
    assert isinstance(dataset, (list, tuple)), u'Dataset type error'

    query_table = dict()
    query_table['__fields__'] = tuple(dataset[0].keys()) if dataset else tuple()
    query_table['__data__'] = [tuple(record.values()) for record in dataset] if dataset else list()
    return query_table


def queryTable2dataset(query_table):
    """
    Convert query table format data to dataset format data.

    :param query_table: Query table format data:
        {
        '__fields__': ('column1 name', 'column2 name', ...),
        '__data__': [
            (value1, value2, ...),
            ...
            ]
        }
    :return: Dataset format data:
        [
        {'column1 name': value1, 'column2 name': value1, ...},
        ...
        ]
    """
    assert isinstance(query_table, dict), u'Query table type error'

    dataset = [{col_name: row[i] for i, col_name in enumerate(query_table.get('__fields__', list()))} for row in query_table.get('__data__', list())]
    return dataset
