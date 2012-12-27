#!/bin/env python
# coding=utf-8
''' models definition.

>>> from restaurant import Restaurant, Menu


'''

from restaurant import Restaurant, Menu, MenuPrice
from order import Order
from user import UserProfile

from django.contrib.auth.models import User
from django.db.models.signals import post_save

# definition of UserProfile from above
# ...

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
