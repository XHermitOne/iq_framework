#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python analog compare functions.
"""

__version__ = (0, 0, 0, 1)


# NUMERIC
def pyLesser(val, cmp, *arg):
    return val < cmp


def pyLesserOrEqual(val, cmp, *arg):
    return val <= cmp


def pyGreat(val, cmp, *arg):
    return val > cmp


def pyGreatOrEqual(val, cmp, *arg):
    return val >= cmp


def pyBetween(val, cmp1, cmp2, *arg):
    return cmp1 <= val <= cmp2


def pyNotBetween(val, cmp1, cmp2, *arg):
    return not (cmp1 <= val <= cmp2)


# STRING
def pyEqual(val, cmp, *arg):
    return val == cmp


def pyNotEqual(val, cmp, *arg):
    return val != cmp


def pyContain(val, cmp, *arg):
    return cmp in val


def pyNotContain(val, cmp, *arg):
    return not (cmp in val)


def pyInto(val, cmp, *arg):
    return val in cmp


def pyNotInto(val, cmp, *arg):
    return not (val in cmp)


def pyStartsWith(val, cmp, *arg):
    return val.startswith(cmp)


def pyEndsWith(val, cmp, *arg):
    return val.endswith(cmp)


def pyMask(val, cmp, *arg):
    return True


def pyNotMask(val, cmp, *arg):
    return True


def pyIsNull(val, cmp, *arg):
    return not bool(val)


def pyNotNull(val, cmp, *arg):
    return bool(val)


# DATETIME
def pyDateTimeEqual(val, cmp, *arg):
    return val == cmp


def pyDateTimeNotEqual(val, cmp, *arg):
    return val != cmp


def pyDateTimeInto(val, cmp, *arg):
    return val in cmp


def pyDateTimeNotInto(val, cmp, *arg):
    return not (val in cmp)


def pyDateTimeIsNull(val, cmp, *arg):
    return val is None


def pyDateTimeNotNull(val, cmp, *arg):
    return val is not None


def pyDateTimeLesser(val, cmp, *arg):
    return val < cmp


def pyDateTimeLesserOrEqual(val, cmp, *arg):
    return val <= cmp


def pyDateTimeGreat(val, cmp, *arg):
    return val > cmp


def pyDateTimeGreatOrEqual(val, cmp, *arg):
    return val >= cmp


def pyDateTimeBetween(val, cmp1, cmp2, *arg):
    return cmp1 <= val <= cmp2


def pyDateTimeNotBetween(val, cmp1, cmp2, *arg):
    return not (cmp1 <= val <= cmp2)
