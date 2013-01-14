#!/bin/env python
# coding=utf-8
'''restaurant model definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.db import models
from mealing.utils import is_today
import time
import datetime


class Restaurant(models.Model):
    """ A Restaurant object
    
    #create some restaurants
    >>> r1 = Restaurant(name = u"test1", phone1 = u"12222", address = u"good", tips = u"test")
    >>> r1.save()
    >>> print r1
    test1
    >>> r1.add_timestamp = 0
    >>> print r1.readable_add_timestamp()
    1970-01-01 08:00:00
    >>> print r1.get_menu_num()
    0
    >>> r1.add_order_number(10)
    >>> r1.save()
    >>> print r1.order_number
    10
    >>> print r1.get_avg_price()
    0
    >>> menu = Menu.objects.create(name = "menu1", price = 20, restaurant = r1)
    >>> print r1.get_avg_price()
    20
    """
    name = models.CharField(blank = False, max_length = 60, verbose_name = u"名称")
    phone1 = models.CharField(blank = False, max_length = 60, verbose_name = u"电话1")
    phone2 = models.CharField(blank = True, null = True, max_length = 60, verbose_name = u"电话2")
    phone3 = models.CharField(blank = True, null = True, max_length = 60, verbose_name = u"电话3")
    address = models.CharField(blank = False, max_length = 300, verbose_name = u"联系地址")
    tips = models.TextField(blank = False, max_length = 1024, verbose_name = u"友情提示")
    add_timestamp  = models.IntegerField(default = (lambda: int(time.time())), editable = False)
    order_number = models.IntegerField(default = 0, editable = False, verbose_name = u"被订次数")
    max_person_everyday = models.IntegerField(default = 0, verbose_name = u"最多可订餐人数")
    last_order_timestamp = models.IntegerField(default = 0, editable = False)
    order_number_today= models.IntegerField(default = 0, editable = False, verbose_name = u"今日订餐人数")
    
    
    class Meta:
        """ meta class
        """
        app_label = "mealing"
        verbose_name = u"餐厅"
        verbose_name_plural = u"餐厅"
        
    def __unicode__(self):
        return self.name
    
    def readable_add_timestamp(self):
        """ readable timestamp string
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.add_timestamp))
    readable_add_timestamp.short_description = u"添加时间"
    
    def get_menu_num(self):
        """ get menu number
        """
        return Menu.objects.filter(restaurant = self.id).count()
    get_menu_num.short_description = u"菜单数"
    
    def add_order_number(self, number = 1):
        """ add order number
        """
        last_order_date = datetime.datetime(1, 1, 1).fromtimestamp(self.last_order_timestamp)
        if is_today(last_order_date):
            self.order_number += number
            self.order_number_today += number
            self.last_order_timestamp = int(time.time())
        else:
            self.order_number += number
            self.order_number_today = number
            self.last_order_timestamp = int(time.time())
            
    def get_avg_price(self):
        """ get avg price of all menus 
        """
        menus = Menu.objects.filter(restaurant = self)
        if len(menus) is 0:
            return 0
        total_price = 0
        for menu in menus:
            total_price += menu.price
        return total_price / len(menus)
    get_avg_price.short_description= u"平均价格"
    
class Menu(models.Model):
    """ menu of restaurant
    >>> r = Restaurant(name = "rest")
    >>> r.save()
    >>> m = Menu(name = "aa", restaurant = r)
    >>> m.save()
    >>> print m
    aa
    >>> print len(m.get_history_price())
    0
    >>> m.price = 10
    >>> m.save()
    >>> print len(m.get_history_price())
    1
    >>> print m.price
    10
    """
    #restaurant_id = models.IntegerField(blank = False, verbose_name = u"餐厅id")
    restaurant = models.ForeignKey("Restaurant", db_index = False, verbose_name = u"餐厅")
    name = models.CharField(blank = False, max_length = 60, verbose_name = u"菜名")
    price = models.IntegerField(default = 0, verbose_name = u"价格")
    add_timestamp = models.IntegerField(default = (lambda: int(time.time())), editable = False)
    order_number = models.IntegerField(default = 0, editable = False, verbose_name = u"被订次数")
    last_order_datetime = models.DateTimeField(auto_now = True, editable = False)
    
    class Meta:
        """ meta class
        """
        app_label = "mealing"
        verbose_name = u"菜单"
        verbose_name_plural = u"菜单"
    
    def readable_add_timestamp(self):
        """ readable timestamp string
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.add_timestamp))
    readable_add_timestamp.short_description = u"添加时间"
    
    def get_restaurant(self):
        """ get restaurant object
        
        >>> r = Restaurant(name = "midl")
        >>> r.save()
        >>> m = Menu(restaurant = r, name = "hanberge", price = 5)
        >>> print m.price
        5
        >>> print m.get_restaurant()
        midl
        """
        return self.restaurant.name
    get_restaurant.short_description = u"餐厅"
    
    def get_history_price(self):
        return MenuPrice.objects.filter(menu = self.id)
    
    def save(self, force_insert=False, force_update=False, using=None):
        """ save to db
        """
        super(Menu, self).save(force_insert, force_update, using)
        if self.price > 0:
            MenuPrice.objects.create(menu = self, price = self.price)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
class MenuPrice(models.Model):
    """ menu history price list
    >>> r = Restaurant.objects.create(name = "rest")
    >>> m = Menu.objects.create(name = "menu", restaurant = r)
    >>> m.price = 100
    >>> m.save()
    >>> mp = m.get_history_price()[0]
    >>> print mp
    menu: 100
    """
    menu = models.ForeignKey("Menu", db_index = False, editable = False)
    price = models.IntegerField(default = 0, editable = False)
    add_timestamp = models.IntegerField(default = (lambda: int(time.time())), editable = False)
    
    class Meta:
        """ meta class
        """
        app_label = "mealing"
        verbose_name = u"菜单历史价格"
        verbose_name_plural = u"菜单历史价格"
        
    def get_menu_name(self):
        return self.menu.name
    get_menu_name.short_description = u"菜名"
    
    def readable_add_timestamp(self):
        """ readable timestamp string
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.add_timestamp))
    readable_add_timestamp.short_description = u"变更时间"
    
    def __unicode__(self):
        return self.menu.name
    
    def __str__(self):
        return "%s: %d" % (self.menu.name, self.price)
    
    