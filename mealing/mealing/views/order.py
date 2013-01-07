#!/bin/env python
# coding=utf-8
""" order routines

>>> from django.test.client import Client
>>> from django.utils import simplejson
>>> from mealing.models import Restaurant, Menu
>>> from django.contrib.auth.models import User as DjUser

# test check()
>>> c = Client()
>>> u =DjUser.objects.create_user("test_order", "test_order@funshion.com", "test_order")
>>> c.login(username = "test_order", password = "test_order")
True
>>> resp = c.get("/order/ready/")
>>> print resp.status_code
200
"""


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from mealing.views.decorator import render_json, render_template
from mealing.models import Menu
from mealing.forms import CommitOrderForm
import logging
import types


def ready(request, page = 1):
    """ ready to complete order
    """
    if request.user.is_authenticated() is False:
        return redirect("/login/")
    menus = Menu.objects.filter(id__in = request.session.get("menus", []))
    paginator = Paginator(menus, 20)
    try:
        menus_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        menus_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        menus_page = paginator.page(paginator.num_pages)
    restaurant = None
    total_price = 0
    if menus:
        restaurant = menus[0].restaurant
        for menu in menus:
            total_price += menu.price
    # init and check form
    if request.method == "POST":
        form = CommitOrderForm(request.POST)
        if form.is_valid():
            # check user
            receivers = []
            receiver_names = form.cleaned_data["receivers"].split(" ")
            for name in receiver_names:
                u = DjangoUser.objects.get(username = name)
                if not u :
                    form.set_custom_error(u"%s 是一个无效的用户名" % name)
                    return render_template("order_ready.html", 
                           {"menus_page": menus_page, "restaurant": restaurant, 
                            "total_price": total_price, "form": form}, 
                           request = request)
                receivers.append(u)
            
                
    else:
        form = CommitOrderForm()
    return render_template("order_ready.html", 
                           {"menus_page": menus_page, "restaurant": restaurant, 
                            "total_price": total_price, "form": form}, 
                           request = request)