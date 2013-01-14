#!/bin/env python
# coding=utf-8
''' all rank models.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.db import models


class PopMenuRank(models.Model):
    """ use id as rank. use last order time and order number as params, ranked by temperature algorithm.
    >>> from mealing.models import Menu, Restaurant
    >>> res = Restaurant.objects.create(name = "rest1")
    >>> menu1 = Menu.objects.create(restaurant = res, name = "menu1")
    >>> rank1 = PopMenuRank.objects.create(menu = menu1, score = 1.7)
    >>> print rank1.score
    1.7
    """
    menu = models.ForeignKey("Menu")
    score = models.FloatField(default = 0.0)
    
    class Meta:
        app_label = "mealing"
        
class NewlyMenuRank(models.Model):
    """ use id as rank. use add time as key params, ranked by temperature algorithm.
    """
    menu = models.ForeignKey("Menu")
    score = models.FloatField(default = 0.0)
    
    class Meta:
        app_label = "mealing"