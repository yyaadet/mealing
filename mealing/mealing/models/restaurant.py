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
    """
    name = models.CharField(blank = False, max_length = 60, verbose_name = u"名称")
    phone1 = models.CharField(blank = False, max_length = 60, verbose_name = u"电话")
    phone2 = models.CharField(blank = True, null = True, max_length = 60, verbose_name = u"电话")
    phone3 = models.CharField(blank = True, null = True, max_length = 60, verbose_name = u"电话")
    address = models.CharField(blank = False, max_length = 300, verbose_name = u"联系地址")
    tips = models.TextField(blank = False, max_length = 1024, verbose_name = u"友情提示")
    add_timestamp  = models.IntegerField(default = (lambda: int(time.time())), editable = False)
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"餐厅"
        verbose_name_plural = u"餐厅"
        
    def __unicode__(self):
        return self.name
    
    def readable_add_timestamp(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.add_timestamp))
    readable_add_timestamp.short_description = u"添加时间"
    
class Menu(models.Model):
    """ menu of restaurant
    
    >>> m = Menu(name = "aa", restaurant_id = 1)
    >>> m.save()
    >>> print m
    aa
    """
    restaurant_id = models.IntegerField(blank = False, verbose_name = u"餐厅id")
    name = models.CharField(blank = False, max_length = 60, verbose_name = u"菜名")
    price = models.IntegerField(default = 0, verbose_name = u"价格")
    add_timestamp = models.IntegerField(default = (lambda: int(time.time())), editable = False)
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"菜单"
        verbose_name_plural = u"菜单"
    
    def readable_add_timestamp(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.add_timestamp))
    readable_add_timestamp.short_description = u"添加时间"
    
    def get_restaurant(self):
        """ get restaurant object
        
        >>> r = Restaurant(name = "midl")
        >>> r.save()
        >>> m = Menu(restaurant_id = r.id, name = "hanberge", price = 5)
        >>> print m.price
        5
        """
        return Restaurant.objects.get(id = self.restaurant_id)
    
    def __str__(self):
        return self.name
    
class MenuPrice(models.Model):
    """ menu history price list
    """
    menu_id = models.IntegerField(blank = False)
    price = models.IntegerField(default = 0)
    add_timestamp = models.IntegerField(default = (lambda: int(time.time())), editable = False)
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"菜单历史价格"
        verbose_name_plural = u"菜单历史价格"
    
    
    