#!/bin/env python
# coding=utf-8
''' order related model definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.http import HttpRequest as request
from mealing.models.restaurant import Restaurant, Menu
from mealing.utils import is_today
import time
import datetime

class Order(models.Model):
    """ user order. don't allow order multiple restaurants.
    >>> u = DjangoUser.objects.create_user("u1", "u1@funshion.com", "1111")
    >>> r = Restaurant.objects.create(name = "res1")
    >>> m = Menu.objects.create(restaurant = r, name = "menu", price = 10)
    >>> o = Order.objects.create(sponsor = u, restaurant = r)
    >>> print o.sponsor
    u1
    >>> o.menus = [m]
    >>> o.save()
    >>> print o.menus.all()
    [<Menu: menu>]
    >>> print o.__unicode__()
    u1: res1
    >>> print o.sum_price()
    10
    >>> print o.price
    10
    >>> o.owners = [u]
    >>> print o.owners.all()
    [<User: u1>]
    >>> print o.get_owners_string()
    , 
    >>> print o.is_end()
    False
    
    ######### test get_today_restaurants()
    >>> restaurants = Order.get_today_restaurants()
    >>> print restaurants[0].name == r.name
    True
    
    ######### test delete()
    >>> o.delete()
    >>> user = DjangoUser.objects.get(pk = u.id)
    >>> print user.get_profile().last_order
    None
    >>> print user.get_profile().last_order_timestamp
    0
    >>> print o.get_status() != ""
    True
    
    
    
    
    """
    sponsor = models.ForeignKey(DjangoUser, blank = False, editable = False, verbose_name = u"订餐人")
    restaurant = models.ForeignKey(Restaurant, blank = False, verbose_name = u"餐厅")
    owners = models.ManyToManyField(DjangoUser, blank = False, related_name="%(app_label)s_%(class)s_owners", verbose_name = u"领餐人")
    menus = models.ManyToManyField(Menu, blank = False, verbose_name = u"菜品")
    price = models.IntegerField(default = 0, editable = False, verbose_name = u"总价格")
    add_timestamp = models.IntegerField(default = (lambda: int(time.time())), editable = False, verbose_name = u"下单时间")
    end_timestamp = models.IntegerField(default = 0, editable = False, verbose_name = u"结束订单时间")
    notify_number = models.IntegerField(default = 0, editable = False)
    last_notify_datetime = models.DateTimeField(auto_now = True, editable = False)
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"订单"
        verbose_name_plural = u"订单"
        ordering = ["restaurant", "add_timestamp"]
        
    def __unicode__(self):
        return u"%s: %s" % (self.sponsor.username, self.restaurant.name)
    
    def sum_price(self):
        """ recalculation all menu price, then save to db
        """
        price = 0
        for menu in self.menus.all():
            price += menu.price
        if price != self.price:
            self.price = price
            self.save()
        return price
    
    def get_owners_string(self):
        """ get all owners
        """
        retval = u""
        for u in self.owners.all():
            retval += "%s, " % (u.get_profile().real_name) 
        return retval
    get_owners_string.short_description = u"领餐人"
    
    def get_menus_string(self):
        """get all menus string
        """
        retv = u""
        for m in self.menus.all():
            retv += u"%s, " % m.name
        return retv
    get_menus_string.short_description = u"所订菜单"
    
    def is_end(self):
        """ is order end?
        """
        if self.end_timestamp == 0:
            return False
        if int(time.time()) > self.end_timestamp:
            return True
        return False
    
    def get_add_time(self):
        """ readable add_timestamp
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.add_timestamp))
    get_add_time.short_description = u"订餐时间"
    
    def get_end_time(self):
        """ readable end_timestamp
        """
        if self.end_timestamp == 0:
            return u"none"
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.end_timestamp))
    get_end_time.short_description = u"到餐时间"
    
    def delete(self, *args, **kwargs):
        """ to override builtin delete method
        """
        # update owners last order information
        for user in self.owners.all():
            profile = user.get_profile()
            profile.last_order_timestamp = 0
            profile.last_order = None
            profile.save()
        super(Order, self).delete(*args, **kwargs)
    
    def get_status(self):
        """ to get readable status
        """
        if is_today(datetime.datetime(1, 1, 1).fromtimestamp(self.add_timestamp)) is False:
            return u"已过期"
        elif self.notify_number > 0:
            return u"餐已经到了"
        else:
            return u"未到"
    get_status.short_description = u"订餐状态"
    
    @classmethod
    def get_today_restaurants(cls):
        """ get all restaurants of today
        """
        today = datetime.datetime(1, 1, 1).today().replace(hour = 0, minute = 0, second = 0)
        today_timestamp = time.mktime(today.timetuple())
        orders = cls.objects.filter(add_timestamp__gt = today_timestamp)
        restaurants = [order.restaurant for order in orders]
        return list(set(restaurants))