#!/bin/env python
# coding=utf-8
''' util definition.
'''


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from mealing.utils.date import is_same_day, is_today, datetime_to_timestamp, get_today_start_timestamp
from mealing.utils.email import send_mail