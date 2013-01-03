#!/bin/env python
# coding=utf-8
''' restaurant routines.

# test all()
>>> from django.test.client import Client
>>> c = Client()
>>> resp = c.get("/restaurant/")
>>> print resp.status_code
200
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.core.paginator import Paginator
from mealing.views.decorator import render_template
from mealing.models import Restaurant


def all(request):
    """ show all restaurant
    """
    restaurants = Restaurant.objects.all()
    return render_template("restaurant.html")