#!/bin/env python
# coding=utf-8
'''admin model definition.

>>> from mealing.models import Restaurant, Menu
>>> from django.contrib import admin
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.contrib import admin
from mealing.models import Restaurant, Menu, MenuPrice
import time


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "phone1", "get_menu_num", "address", "tips", "readable_add_timestamp",)
    search_fields = ["name"]
    
    
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "get_restaurant", "price", "readable_add_timestamp",)
    search_fields = ["name"]
    
    
class MenuPriceAdmin(admin.ModelAdmin):
    list_display = ("get_menu_name", "price", "readable_add_timestamp")
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
    
    
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuPrice, MenuPriceAdmin)