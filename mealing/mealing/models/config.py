#!/bin/env python
# coding=utf-8
''' site config definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.db import models

class Config(models.Model):
    """ site config.
    >>> c = Config.objects.create()
    >>> print c.is_shutdown_order
    False
    >>> d = Config.get_default()
    >>> print d.per_capita_fee
    30
    """
    per_capita_fee = models.IntegerField(default = 30, verbose_name = u"人均费用")
    is_shutdown_order = models.BooleanField(default = False, verbose_name = u"是否永久关闭订餐")
    shutdown_order_reason = models.TextField(verbose_name = u"订餐关闭原因")
    shutdown_order_hour = models.IntegerField(default = 17, verbose_name = u"关闭订餐时刻", help_text = u"范围： 0-23")
    shutdown_order_minu = models.IntegerField(default = 0, verbose_name = u"关闭订餐分钟", help_text = u"范围： 0-59")
    
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"全局设置"
        verbose_name_plural = u"全局设置"
    
    @classmethod
    def get_default(cls):
        """ get default config. only one.
        """
        obj = cls.objects.get(pk = 1)
        if not obj:
            return None
        return obj
    
    def __unicode__(self):
        return u"全局设置项"
    
    def __str__(self):
        return u"默认设置"