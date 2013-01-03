#!/bin/env python
# coding=utf-8
''' restaurant routines.

# test all()
>>> from django.test.client import Client
>>> c = Client()
>>> resp = c.get("/restaurant/all/1/")
>>> print resp.status_code
200
>>> resp = c.get("/restaurant/all/999999/")
>>> print resp.status_code
200
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mealing.views.decorator import render_template
from mealing.models import Restaurant
import logging


def all(request, page = 1):
    """ show all restaurant
    """
    all_restaurants = Restaurant.objects.all()
    paginator = Paginator(all_restaurants, 20)
    try:
        restaurants_page = paginator.page(page)
        cur_page = page
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        restaurants_page = paginator.page(1)
        cur_page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        restaurants_page = paginator.page(paginator.num_pages)
        cur_page = paginator.num_pages
    logging.debug("restaurant page: %d ~ %d index" % (restaurants_page.start_index(), restaurants_page.end_index()))
    return render_template("restaurant.html", {"restaurants_page": restaurants_page})