#!/bin/env python
# coding=utf-8
""" order routines

>>> from django.test.client import Client
>>> from django.utils import simplejson
>>> from mealing.models import Restaurant, Menu
>>> from django.contrib.auth.models import User as DjUser

# test check()
>>> c = Client()
>>> resp = c.get("/order/ready")
>>> print resp.status_code
200
"""


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from mealing.views.decorator import render_json
from mealing.models import Menu
import logging
import types


def ready(request):
    pass