#!/bin/env python
# coding=utf-8
'''restaurant model definition.

'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.db import models
import time


class Restaurant(models.Model):
    """ A Restaurant object
    >>> from mealing.models.restaurant import Restaurant
    
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
    """
    name = models.CharField(blank = False, max_length = 60, verbose_name = u"名称")
    phone1 = models.CharField(blank = False, max_length = 60, verbose_name = u"电话")
    phone2 = models.CharField(blank = True, null = True, max_length = 60, verbose_name = u"电话")
    phone3 = models.CharField(blank = True, null = True, max_length = 60, verbose_name = u"电话")
    address = models.CharField(blank = False, max_length = 300, verbose_name = u"联系地址")
    tips = models.TextField(blank = False, max_length = 1024, verbose_name = u"友情提示")
    add_timestamp  = models.IntegerField(default = (lambda: int(time.time())), editable = False)
    
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
    
    