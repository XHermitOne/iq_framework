#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube aggregation.
"""

__version__ = (0, 0, 0, 1)


# Aggregation functions
AGGREGATE_FUNCTIONS = (None, 'sum', 'count', 'min_value', 'max_value', 'avg',
                       'count_nonempty', 'count_distinct',
                       'stddev', 'variance')


class iqCubeAggregateProto(object):
    """
    OLAP Cube aggregation prototype class.
    """
    def getFunctionName(self):
        """
        Get aggregation function name.
        """
        return None

    def getMeasureName(self):
        """
        Measure/Fact that is aggregated.
        """
        return None

    def getExpressionCode(self):
        """
        Aggregation expression body.
        """
        return None

    def getLabel(self):
        """
        Aggregation label.
        """
        return u''
