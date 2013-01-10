#!/bin/env python
# coding=utf-8
''' url route definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mealing.views.home.index', name='home'),
    url(r"^login/$", "mealing.views.user.login", name = "login"),
    url(r"^logout/$", "mealing.views.user.logout", name = "logout"),
    url(r"^register/$", "mealing.views.user.register", name = "register"),
    url(r"^change_password/$", "mealing.views.user.change_password", name = "change_password"),
    url(r"^get_usernames/(?P<username>\w+)/$", "mealing.views.user.get_usernames"),
    url(r"^get_usernames/$", "mealing.views.user.get_usernames"),
    url(r"^change_info/$", "mealing.views.user.change_info", name = "change_info"),
    url(r"^user/$", "mealing.views.user.home", name = "user_home"),
    
    url(r"^restaurant/all/(?P<page>\d+)/$", "mealing.views.restaurant.all", name = "restaurant_all"),
    url(r"^restaurant/all/$", "mealing.views.restaurant.all"),
    url(r"^restaurant/menu/(?P<restaurant_id>\d+)/(?P<restaurant_name>\w+)/(?P<page>\d+)/$", "mealing.views.restaurant.all_menu", 
        name = "restaurant_all_menu"),
    url(r"^restaurant/menu/(?P<restaurant_id>\d+)/(?P<restaurant_name>\w+)/$", "mealing.views.restaurant.all_menu"),
    
    url(r"^menu/check/(?P<menu_id>\d+)/$", "mealing.views.menu.check", name = "menu_check"),
    
    url(r"^order/ready/$", "mealing.views.order.ready", name = "order_ready"),
    url(r"^order/(?P<order_id>\d+)/$", "mealing.views.order.info", name = "order_info"),
    url(r"^order/today/$", "mealing.views.order.today"),
    url(r"^order/today/(?P<page>\d+)/$", "mealing.views.order.today", name = "order_today"),
    # url(r'^mealing/', include('mealing.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^admin/', include(admin.site.urls), name = "admin"),
)


