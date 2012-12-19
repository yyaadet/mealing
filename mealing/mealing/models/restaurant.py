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
    
    >>> Restaurant.objects.all()
    
    #create some restaurants
    #>>> r1 = Restaurant(name = u"test1", phone1 = u"12222", address = u"good", tips = u"test")
    #>>> r1.save()
    #>>> print r1
    #'test1'
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