#!/bin/env python
# coding=utf-8
'''user related model definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.db import models
import time

class UserProfile(models.Model):
    """ user profile class.
    >>> from django.contrib.auth.models import User
    >>> u = User.objects.create_user("pengxt", "pengxt@funshion.com", "xiaotao")
    >>> print u.username
    pengxt
    >>> print u.get_profile().order_num
    0
    """
    user = models.OneToOneField(DjangoUser)
    order_num = models.IntegerField(default = 0, editable = False, verbose_name = u"订餐次数")
    
    class Meta:
        app_label = "mealing"
        verbose_name = u"额外信息"