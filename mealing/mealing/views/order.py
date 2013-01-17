#!/bin/env python
# coding=utf-8
""" order routines

>>> from django.test.client import Client
>>> from django.utils import simplejson
>>> from mealing.models import Restaurant, Menu, Config
>>> from mealing.utils import is_today
>>> from django.contrib.auth.models import User as DjUser
>>> import datetime
>>> config = Config.get_default()
>>> now = datetime.datetime(1, 1, 1).today()

################# test ready()
>>> c = Client()
>>> u = DjUser.objects.create_user("test_order", "test_order@funshion.com", "test_order")
>>> c.login(username = "test_order", password = "test_order")
True
>>> resp = c.get("/order/ready/")
>>> print resp.status_code
200
>>> config.shutdown_order_hour = now.hour + 1
>>> config.save()
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
>>> restaurant = Restaurant.objects.get(pk = rest.id)
>>> print restaurant.order_number
1
>>> print restaurant.order_number_today
1
>>> menu = Menu.objects.get(pk = menu.id)
>>> print menu.order_number
1
>>> print is_today(menu.last_order_datetime)
True

# test info()
>>> resp = c.get("/order/%d/" % u.get_profile().last_order.id)
>>> print resp.status_code
200

######## test today() 
>>> resp = c.get("/order/today/")
>>> print resp.status_code
200
>>> resp = c.get("/order/today/%d/" % restaurant.id)
>>> print resp.status_code
200


########## test notify()
>>> order = Order.objects.get(pk = u.get_profile().last_order.id)
>>> resp = c.get("/order/notify/%d/" % order.id)
>>> print simplejson.loads(resp.content)["ok"]
False

>>> user = DjangoUser.objects.get(pk = u.id)
>>> user.is_superuser = True
>>> user.save()
>>> user = DjangoUser.objects.get(id = user.id)
>>> print user.is_superuser
True
>>> c.logout()
>>> c.login(username = user.username, password = user.username)
True
>>> resp = c.get("/order/notify/%d/" % order.id)
>>> print simplejson.loads(resp.content)["ok"]
True


########## notify_restaurant()
>>> c.logout()
>>> resp = c.get("/order/notify/restaurant/%d/" % order.restaurant.id)
>>> print simplejson.loads(resp.content)["ok"]
False

>>> c.login(username = user.username, password = user.username)
True
>>> resp = c.get("/order/notify/restaurant/%d/" % order.restaurant.id)
>>> print simplejson.loads(resp.content)["ok"]
True



############## test export_today_orders()
>>> resp = c.get("/order/export_today/")
>>> print resp.status_code
200


######## test delete()
>>> order = Order.objects.get(pk = u.get_profile().last_order.id)
>>> order.add_timestamp -= 60*60*24
>>> order.save()
>>> resp = c.get("/order/del/%d/" % order.id)
>>> user = DjangoUser.objects.get(pk = u.id)
>>> print user.get_profile().last_order != None
True
>>> order.add_timestamp += 60*60*24
>>> order.save()
>>> resp = c.get("/order/del/%d/" % order.id)
>>> user = DjangoUser.objects.get(pk = u.id)
>>> print user.get_profile().last_order
None

"""


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.contrib.auth.models import User as DjangoUser
from django.http import Http404
from django.contrib import messages
from mealing.views.decorator import render_json, render_template, render_csv
from mealing.models import Menu, Config, Order, Restaurant
from mealing.utils import is_same_day, is_today, send_mail, get_today_start_timestamp
from mealing.forms import CommitOrderForm
import logging
import types
import datetime
import time



def _is_fee_sufficient(request, config, receiver_number, total_price):
    """ judge fee by receiver number and current total price
    """
    per_capita_fee = config.per_capita_fee
    if receiver_number * per_capita_fee < total_price:
        logging.debug("fee is not sufficient")
        messages.warning(request, u"您的费用不足，每人费用为 %d" % per_capita_fee)
        return False
    return True

def _is_order_shutdown(request, config):
    """ is order system shutdown now ?
    """
    if config.is_shutdown_order == True:
        logging.debug("order is shutdown")
        messages.warning(request, u"订餐系统已经关闭：%s" % config.shutdown_order_reason)
        return True
    now = datetime.datetime(1, 1, 1).today()
    shutdown_datetime = datetime.datetime(now.year, now.month, now.day, 
                                          config.shutdown_order_hour, config.shutdown_order_minu)
    if now > shutdown_datetime:
        logging.debug("order time is pass")
        messages.warning(request, u"订餐时间已过，请于 %02d:%02d 前完成订餐" % 
                         (config.shutdown_order_hour, config.shutdown_order_minu))
        return True
    return False
    
def _is_restaurant_full(request, restaurant, receiver_number):
    """ restaurant only fullfil some people, not all.
    """
    if restaurant is None:
        return True
    if restaurant.max_person_everyday == 0:
        return False
    now = datetime.datetime(1, 1, 1).today()
    last_order_date = datetime.datetime(1, 1, 1).fromtimestamp(restaurant.last_order_timestamp)
    if is_same_day(now, last_order_date):
        if receiver_number + restaurant.order_number_today > restaurant.max_person_everyday:
            messages.warning(request, u"剩余可订餐人数为 %d，请更换其他餐厅。" % 
                             (restaurant.max_person_everyday - restaurant.order_number_today))
            return True
    else:
        if restaurant.max_person_everyday <= restaurant.order_number_today:
            messages.warning(request, u"本餐厅最大订餐人数为 %d" % restaurant.max_person_everyday)
            return True
    return False

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
            config = Config.get_default()
            # check fee is validate
            if _is_fee_sufficient(request, config, len(receiver_names), total_price) is False:
                return render_template("order_ready.html", 
                           {"menus_page": menus_page, "restaurant": restaurant, 
                            "total_price": total_price, "form": form}, 
                           request = request)
            if  _is_order_shutdown(request, config) is True:
                return render_template("order_ready.html", 
                           {"menus_page": menus_page, "restaurant": restaurant, 
                            "total_price": total_price, "form": form}, 
                           request = request)
            if _is_restaurant_full(request, restaurant, len(receiver_names)) is True:
                form.set_custom_error(u"餐厅已满")
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
            # update restaurant infomation
            restaurant.add_order_number(len(receiver_names))
            restaurant.save()
            # update menu information
            for menu in menus:
                menu.order_number += len(receiver_names)
                menu.last_order_datetime = datetime.datetime(1, 1, 1).today()
                menu.save()
            # clear session
            request.session["menus"] = set()
            return redirect("/order/%d/" % order.id)       
    else:
        form = CommitOrderForm({"receivers": request.user.username})
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

def today(request, restaurant_id = 0, page = 1):
    """ get today's order
    """
    today_timestamp = get_today_start_timestamp()
    restaurants = Order.get_today_restaurants()
    try:
        restaurant = Restaurant.objects.get(id = restaurant_id)        
    except Exception, e:
        logging.warn("restaurant %d not exist" % restaurant_id)
        restaurant = None

    if not restaurant:
        orders = Order.objects.filter(add_timestamp__gt = today_timestamp)
        prefix = "/order/today"
    else:
        orders = Order.objects.filter(add_timestamp__gt = today_timestamp, restaurant = restaurant)
        prefix = "/order/today/%d" % restaurant.id 
    total_price = 0
    for order in orders:
        total_price += order.price
    paginator = Paginator(orders, 50)
    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders_page = paginator.page(paginator.num_pages)
        
    return render_template("order_today.html", 
                           {"orders_page": orders_page, "today": today, 
                            "total_price": total_price, "restaurant": restaurant, 
                            "restaurants": restaurants, "prefix": prefix}, 
                           request)

    
def delete(request, order_id = 0):
    """ to delete order by self, who is sponsor
    """
    order = Order.objects.get(pk = order_id)
    if not order:
        raise Http404
    if order.sponsor != request.user:
        messages.warning(request, u"订单不是你发起的，无权删除")
        return redirect("/user/")
    config = Config.get_default()
    if _is_order_shutdown(request, config) is True:
        messages.warning(request, u"订餐系统关闭中，暂时不能删除")
        return redirect("/user/")
    if is_today(datetime.datetime(1, 1, 1).fromtimestamp(order.add_timestamp)) is False:
        logging.debug("order %d is out of time" % order.id)
        messages.warning(request, u"订单已经过期，不允许删除，请联系管理员")
        return redirect("/user/")
    order.delete()
    return redirect("/user/")


def _notify_order(order):
    """ to notify order owners
    """
    if not order:
        return False
    order.notify_number += 1
    order.last_notify_datetime = datetime.datetime(1, 1, 1).today()
    order.save()
    # send email
    to = [order.sponsor.email]
    cc = [user.email for user in order.owners.all()]
    if order.sponsor.email in cc:
        cc.remove(order.sponsor.email)
    subject = u"您的订餐 #%d 已到" % order.today_id
    msg = u"%s 编号为%d" % (order.restaurant.name, order.today_id)
    send_mail(subject, msg, to, cc)
    return True

@render_json
def notify(request, order_id = 0):
    """ to notify user, to get meal now
    """
    if request.user.is_superuser is False:
        return {"ok": False, "reason": u"只有管理员有权限通知"}
    try:
        order = Order.objects.get(id = order_id)
    except Exception, e:
        logging.warn("some exception: %s" % e)
        return {"ok": False, "reason": u"订餐不存在了"}
    _notify_order(order)
    return {"ok": True, "notify_number": order.notify_number}

@render_json
def notify_restaurant(request, restaurant_id = 0):
    """ notify all orders of restaurant
    """
    if request.user.is_superuser is False:
        return {"ok": False, "reason": u"只有管理员有权限通知"}
    try:
       restaurant = Restaurant.objects.get(id = restaurant_id)
    except Exception, e:
        logging.debug("some exception: %s" % e)
        return {"ok": False, "reason": u"餐厅不存在"}
    today_timestamp = get_today_start_timestamp()
    orders = Order.objects.filter(restaurant = restaurant, add_timestamp__gt = today_timestamp)
    if not orders:
        return {"ok": False, "reason": u"订餐不存在了"}
    for order in orders:
        _notify_order(order)
    return {"ok": True}


@render_csv
def export_today_orders(request):
    """ export orders of today
    """
    today = datetime.datetime(1, 1, 1).today().strftime("%Y%m%d")
    orders = Order.get_today_orders()
    retv = []
    retv.append([])
    retv.append([u"日期", u"编号", u"餐厅", u"部门", u"订餐人", u"菜品", u"价格"])
    total_price = 0
    for order in orders:
        retv.append([today, order.today_id, order.restaurant.name, order.get_department(), 
                     order.get_owners_string(), order.get_menus_string(), order.price])
    retv.insert(0, [u"总费用", total_price])
    return "%s.csv" % today, retv