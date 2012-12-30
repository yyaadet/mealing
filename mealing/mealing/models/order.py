#!/bin/env python
# coding=utf-8
''' order related model definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.http import HttpRequest as request
from restaurant import Restaurant, Menu
import time

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
    u1, 
    """
    sponsor = models.ForeignKey(DjangoUser, blank = False, editable = False)
    restaurant = models.ForeignKey(Restaurant, blank = False, verbose_name = u"餐厅")
    owners = models.ManyToManyField(DjangoUser, blank = False, related_name="%(app_label)s_%(class)s_owners")
    menus = models.ManyToManyField(Menu, blank = False)
    price = models.IntegerField(default = 0, editable = False, verbose_name = u"总价格")
    add_timestamp = models.IntegerField(default = (lambda: int(time.time())), editable = False, verbose_name = u"下单时间")
    end_timestamp = models.IntegerField(default = 0, editable = False, verbose_name = u"下单时间")
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"订单"
        verbose_name_plural = u"订单"
        
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
            retval += "%s, " % u.username 
        return retval
    get_owners_string.short_description = u"订餐人"
    
    def get_menus_string(self):
        """get all menus string
        """
        retv = u""
        for m in self.menus.all():
            retv += u"%s, " % m.name
        return retv
    get_menus_string.short_description = u"所订菜单"