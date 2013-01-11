#!/bin/env python
# coding=utf-8
'''admin model definition.

>>> from mealing.models import Restaurant, Menu
>>> from django.contrib import admin
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User as DjangoUser
from mealing.models import Restaurant, Menu, MenuPrice
from mealing.models import UserProfile
from mealing.models import Order
from mealing.models import Config
from mealing.models import Department
import time


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "phone1", "get_menu_num", "address", "tips", "readable_add_timestamp",)
    search_fields = ["name"]
    
    
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "get_restaurant", "price", "readable_add_timestamp",)
    search_fields = ["name", ]
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ("sponsor", "restaurant", "get_menus_string", "get_owners_string", "get_add_time", "get_end_time", )
    search_fields = ["sponsor", ]
    
    def has_add_permission(self, request):
        return False
    
    
class ConfigAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False
    
    
class MenuPriceAdmin(admin.ModelAdmin):
    list_display = ("get_menu_name", "price", "readable_add_timestamp", )
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
    
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", )

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(DjangoUserAdmin):
    inlines = (UserProfileInline, )
    
    
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuPrice, MenuPriceAdmin)
admin.site.register(Department, DepartmentAdmin)
# Re-register UserAdmin
admin.site.unregister(DjangoUser)
admin.site.register(DjangoUser, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Config, ConfigAdmin)