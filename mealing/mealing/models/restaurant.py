#!/bin/env python
# coding=utf-8
'''restaurant model definition.

'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.db import models

class Restaurant(models.Model):
    name = models.CharField(blank = False, max_length = 60)
    phone1 = models.CharField(blank = False, max_length = 60)
    phone2 = models.CharField(blank = True, null = True, max_length = 60)
    phone3 = models.CharField(blank = True, null = True, max_length = 60)
    address = models.CharField(blank = False, max_length = 300)
    tips = models.CharField(blank = False, max_length = 1024)
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"餐厅"
        verbose_name_plural = u"餐厅"
        
    def __unicode__(self):
        return self.name