#!/bin/env python
# coding=utf-8
''' models definition.
>>> from restaurant import Restaurant, Menu
'''


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from restaurant import Restaurant, Menu, MenuPrice
from department import Department
from order import Order
from user import UserProfile
from config import Config
import datetime

# definition of UserProfile from above
# ...

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)