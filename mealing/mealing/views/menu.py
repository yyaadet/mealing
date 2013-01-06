#!/bin/env python
# coding=utf-8
""" menu routines

>>> from django.test.client import Client
>>> from django.utils import simplejson
>>> from mealing.models import Restaurant, Menu
>>> from django.contrib.auth.models import User as DjUser

# test check()
>>> c = Client()
>>> restaurant = Restaurant.objects.create(name = "restxxxxx")
>>> menu = Menu.objects.create(restaurant = restaurant, name = "menu")
>>> resp = c.get("/menu/check/%d/" % menu.id)
>>> resp_obj = simplejson.loads(resp.content)
>>> print resp_obj["is_ok"]
False
>>> u = DjUser.objects.create_user("user_001", "user1@funshion.com", "user")
>>> c.login(username = "user_001", password = "user")
True
>>> resp = c.get("/menu/check/%d/" % menu.id)
>>> resp_obj = simplejson.loads(resp.content)
>>> print resp_obj["is_ok"]
True
>>> print c.session["menus"].get(menu.id)
True
"""


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from mealing.views.decorator import render_json
from mealing.models import Menu
import logging
import types


@render_json
def check(request, menu_id = 0):
    """ order meal, user check menu.
    """
    if type(menu_id) != types.IntType:
        menu_id = int(menu_id)
    if request.user.is_authenticated() == False:
        logging.debug("please login")
        return {"is_ok": False, "reason": u"请先登录"}
    menu = Menu.objects.get(id = menu_id)
    if menu == None:
        logging.debug("not found menu")
        return {"is_ok": False, "reason": u"无效菜单id"}
    # menus store as {"menu_id": True|False}, True|False is checked.
    menus = request.session.get("menus", {})
    if menu_id not in menus:
        menus[menu_id] = True
    else:
        menus[menu_id] = (not menus[menu_id])
    if menus[menu_id] == False:
        menus.pop(menu_id)
    # reset session["menu"]
    request.session["menus"] = menus
    return {"is_ok": True, "is_checked": menus[menu_id]}