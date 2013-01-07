#!/bin/env python
# coding=utf-8
""" home page functions.

>>> from django.test.client import Client
>>> c = Client()
>>> resp = c.get("/")
>>> print resp.status_code
200
>>> print (resp.context["settings"] != None)
True
"""

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from mealing.views.decorator import render_template


def index(request):
    """ site index
    """
    return render_template("index.html", request = request)