#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Additional functions. Functions taken from the folium project.
"""

import math
import numpy
import pandas

__version__ = (0, 0, 0, 1)


def validate_location(location):
    """
    Validate a single lat/lon coordinate pair and convert to a list

    Validate that location:
    * is a sized variable
    * with size 2
    * allows indexing (i.e. has an ordering)
    * where both values are floats (or convertible to float)
    * and both values are not NaN

    :return: list[float, float]
    """
    if isinstance(location, numpy.ndarray) \
            or (pandas is not None and isinstance(location, pandas.DataFrame)):
        location = numpy.squeeze(location).tolist()
    if not hasattr(location, '__len__'):
        raise TypeError('Location should be a sized variable, '
                        'for example a list or a tuple, instead got '
                        '{!r} of type {}.'.format(location, type(location)))
    if len(location) != 2:
        raise ValueError('Expected two (lat, lon) values for location, '
                         'instead got: {!r}.'.format(location))
    try:
        coords = (location[0], location[1])
    except (TypeError, KeyError):
        raise TypeError('Location should support indexing, like a list or '
                        'a tuple does, instead got {!r} of type {}.'
                        .format(location, type(location)))
    for coord in coords:
        try:
            float(coord)
        except (TypeError, ValueError):
            raise ValueError('Location should consist of two numerical values, '
                             'but {!r} of type {} is not convertible to float.'
                             .format(coord, type(coord)))
        if math.isnan(float(coord)):
            raise ValueError('Location values cannot contain NaNs.')
    return [float(x) for x in coords]


def validate_locations(locations):
    """
    Validate an iterable with multiple lat/lon coordinate pairs.
    :return: list[list[float, float]] or list[list[list[float, float]]]
    """
    locations = if_pandas_df_convert_to_numpy(locations)
    try:
        iter(locations)
    except TypeError:
        raise TypeError('Locations should be an iterable with coordinate pairs,'
                        ' but instead got {!r}.'.format(locations))
    try:
        next(iter(locations))
    except StopIteration:
        raise ValueError('Locations is empty.')
    try:
        float(next(iter(next(iter(next(iter(locations)))))))
    except (TypeError, StopIteration):
        # locations is a list of coordinate pairs
        return [validate_location(coord_pair) for coord_pair in locations]
    else:
        # locations is a list of a list of coordinate pairs, recurse
        return [validate_locations(lst) for lst in locations]


def if_pandas_df_convert_to_numpy(obj):
    """
    Return a Numpy array from a Pandas dataframe.

    Iterating over a DataFrame has weird side effects, such as the first
    row being the column names. Converting to Numpy is more safe.
    """
    if pandas is not None and isinstance(obj, pandas.DataFrame):
        return obj.values
    else:
        return obj


def parse_size(value):
    try:
        if isinstance(value, str) and value.endswith('px'):
            value_type = 'px'
            value = int(value.strip('px'))
            assert value > 0
        elif isinstance(value, (int, float)):
            value_type = 'px'
            value = int(value)
            assert value > 0
        else:
            value_type = '%'
            value = int(value.strip('%'))
            assert 0 <= value <= 100
    except Exception:
        msg = 'Cannot parse value {!r} as {!r}'.format
        raise ValueError(msg(value, value_type))
    return value, value_type
