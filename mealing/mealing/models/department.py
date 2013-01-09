#!/bin/env python
# coding=utf-8
''' department related model definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.db import models
import time

class Department(models.Model):
    """ user's department.
    """
    name = models.CharField(max_length = 30, verbose_name = u"名称")
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"部门"
        verbose_name_plural = u"部门"
        
    def __unicode__(self):
        return u"%s" % (self.name)
    
    def __str__(self):
        return self.name
    
    