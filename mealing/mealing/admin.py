#!/bin/env python
# coding=utf-8
'''admin model definition.

>>> from mealing.models import Restaurant, Menu
>>> from django.contrib import admin
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.contrib import admin
from mealing.models import Restaurant, Menu
import time


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "phone1", "address", "tips", "readable_add_timestamp",)
    
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "readable_add_timestamp",)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
