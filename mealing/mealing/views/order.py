#!/bin/env python
# coding=utf-8
""" order routines

>>> from django.test.client import Client
>>> from django.utils import simplejson
>>> from mealing.models import Restaurant, Menu
>>> from django.contrib.auth.models import User as DjUser

# test ready()
>>> c = Client()
>>> u = DjUser.objects.create_user("test_order", "test_order@funshion.com", "test_order")
>>> c.login(username = "test_order", password = "test_order")
True
>>> resp = c.get("/order/ready/")
>>> print resp.status_code
200
>>> rest = Restaurant.objects.create(name = "test_order_rest")
>>> menu = Menu.objects.create(name = "test_order_menu", restaurant = rest, price = 10)
>>> resp = c.get("/menu/check/%d/" % menu.id) # check menu
>>> resp = c.post("/order/ready/", {"receivers": "test_order"})
>>> print resp.status_code
302
>>> print u.get_profile().last_order != None
True
>>> print c.session["menus"]
set([])

# test info()
>>> resp = c.get("/order/%d/" % u.get_profile().last_order.id)
>>> print resp.status_code
200
"""


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.contrib.auth.models import User as DjangoUser
from django.http import Http404
from mealing.views.decorator import render_json, render_template
from mealing.models import Menu, Config, Order
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
    # sum total price
    total_price = 0
    if menus:
        restaurant = menus[0].restaurant
        for menu in menus:
            total_price += menu.price
    # init and check form
    if request.method == "POST":
        form = CommitOrderForm(request.POST)
        if form.is_valid():
            receivers = []
            receiver_names = form.cleaned_data["receivers"].split(" ")
            # check fee is validate
            per_capita_fee = Config.get_default().per_capita_fee
            if len(receiver_names) * per_capita_fee < total_price:
                form.set_custom_error(u"费用不足，人均预算是 %d" % per_capita_fee)
                return render_template("order_ready.html", 
                           {"menus_page": menus_page, "restaurant": restaurant, 
                            "total_price": total_price, "form": form}, 
                           request = request)
            # begin to order now    
            order = Order(sponsor = request.user, restaurant = restaurant, price = total_price)
            order.save()
            for name in receiver_names:
                user = DjangoUser.objects.filter(username = name)[0]
                user.get_profile().order_meal(order)
                user.get_profile().save()
                receivers.append(user)
            order.owners = receivers
            order.menus = menus
            order.save()
            # clear session
            request.session["menus"] = set()
            return redirect("/")       
    else:
        form = CommitOrderForm()
    return render_template("order_ready.html", 
                           {"menus_page": menus_page, "restaurant": restaurant, 
                            "total_price": total_price, "form": form}, 
                           request = request)

def info(request, order_id = 0):
    """ order information
    """
    order = Order.objects.get(pk = order_id)
    if not order:
        raise Http404
    return render_template("order_info.html", {"order": order}, request)