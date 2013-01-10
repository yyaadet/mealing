#!/bin/env python
# coding=utf-8
'''user related model definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.db import models
from mealing.models import Order, Department
import time
import datetime

class UserProfile(models.Model):
    """ user profile class.
    >>> from django.contrib.auth.models import User
    >>> u = User.objects.create_user("pengxt", "pengxt@funshion.com", "xiaotao")
    >>> print u.username
    pengxt
    >>> print u.get_profile().order_number
    0
    
    # test order_meal()
    >>> u.get_profile().order_meal(None)
    True
    >>> u.get_profile().order_meal(None)
    False
    
    # test has_ordered_today()
    >>> u.get_profile().has_ordered_today()
    True
    """
    user = models.OneToOneField(DjangoUser)
    order_number = models.IntegerField(default = 0, editable = False, verbose_name = u"订餐次数")
    last_order_timestamp = models.IntegerField(default = 0, editable = False)
    last_order = models.ForeignKey("Order", null = True, editable = False)
    real_name = models.CharField(max_length = 30, verbose_name = u"真实姓名")
    department = models.ForeignKey("Department", null = True, verbose_name = u"所属部门")
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"额外信息"
        
    def order_meal(self, order):
        """ order meal
        """
        if self.has_ordered_today() is True:
            return False
        self.order_number += 1
        self.last_order_timestamp = int(time.time())
        self.last_order = order
        return True
    
    def cancel_order(self):
        """ cancel meal order today
        """
        return True
        
    def has_ordered_today(self):
        """ check is ordered tody?
        """
        now = datetime.datetime(1, 1, 1).today()
        last_order_date = datetime.datetime(1, 1, 1).fromtimestamp(self.last_order_timestamp)
        if (now.year == last_order_date.year and now.month == last_order_date.month and 
               now.day == last_order_date.day):
            return True
        return False
    
    def get_last_order_time(self):
        """ get human readable last_order_timestamp
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.last_order_timestamp))
    get_last_order_time.short_description = u"最后订餐时间"