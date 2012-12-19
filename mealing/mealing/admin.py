#!/bin/env python
# coding=utf-8
'''admin model definition.

'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.contrib import admin
from mealing.models import Restaurant
import time


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "phone1", "address", "tips", "readable_add_timestamp")


admin.site.register(Restaurant, RestaurantAdmin)
