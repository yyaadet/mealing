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

# test all_menu()
>>> import urllib
>>> restaurant = Restaurant.objects.create(name = "rest1")
>>> menu = Menu.objects.create(restaurant_id = restaurant.id, name = "menu1")
>>> resp = c.get("/restaurant/menu/%d/%s/" % (restaurant.id, urllib.quote(restaurant.name)))
>>> print resp.status_code
200
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.utils.encoding import smart_str
from mealing.views.decorator import render_template
from mealing.models import Restaurant, Menu
import logging
import urllib
import types


def all(request, page = 1):
    """ show all restaurant
    """
    all_restaurants = Restaurant.objects.all()
    paginator = Paginator(all_restaurants, 8)
    try:
        restaurants_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        restaurants_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        restaurants_page = paginator.page(paginator.num_pages)
    logging.debug("restaurant page: %d ~ %d index" % (restaurants_page.start_index(), restaurants_page.end_index()))
    return render_template("restaurant.html", {"restaurants_page": restaurants_page}, request)

def all_menu(request, restaurant_id = 0, restaurant_name = "", page = 1):
    """ get all menus of restaurant by name or id
    """
    if type(restaurant_id) != types.IntType:
        restaurant_id = int(restaurant_id)
    if restaurant_id <= 0:
        raise Http404
    menus = Menu.objects.filter(restaurant_id = restaurant_id)
    if menus == []:
        raise Http404
    paginator = Paginator(menus, 20)
    try:
        menus_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        menus_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        menus_page = paginator.page(paginator.num_pages)
    logging.debug("restaurant id type: %s, value %s" % (type(restaurant_id), restaurant_id))
    prefix = "/restaurant/menu/%d/%s" % (restaurant_id, urllib.quote(smart_str(restaurant_name)))
    return render_template("restaurant_all_menu.html", 
                           {"menus_page": menus_page, "prefix": prefix, "restaurant_name": restaurant_name}, 
                           request)