#!/bin/env python
# coding=utf-8
''' date util definition.
>>> import datetime
>>> now = datetime.datetime(1, 1, 1)
>>> other = datetime.datetime(1, 2, 1)
>>> print is_same_day(now, other)
False
>>> other1 = datetime.datetime(1, 1, 1)
>>> print is_same_day(now, other1)
True
'''


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


import datetime

def is_same_day(date1, date2):
    """ date1 and date2 is datetime object
    """
    if date1.year == date2.year and date1.month == date2.month and date1.day == date2.day:
        return True
    return False

def is_today(date):
    """ date is datetime object
    """
    now = datetime.datetime(1, 1, 1).today()
    if now.year == date.year and now.month == date.month and now.day == date.day:
        return True
    return False