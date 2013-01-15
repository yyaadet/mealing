#!/bin/env python
# coding=utf-8
''' computer ranks

>>> from mealing.models import Restaurant, Menu, PopMenuRank

############### test _rank_pop_menu()
>>> r = Restaurant.objects.create(name = "rest")
>>> menu1 = Menu.objects.create(name = "menu1", restaurant = r, order_number = 100)
>>> menu2 = Menu.objects.create(name = "menu2", restaurant = r, order_number = 10)
>>> _rank_pop_menu()
>>> ranks = PopMenuRank.objects.all()
>>> print len(ranks) > 2
True
>>> print ranks[0].score > ranks[1].score
True



############# test _rank_newly_menu()
>>> _rank_newly_menu()
>>> newly_ranks = NewlyMenuRank.objects.all()
>>> print len(newly_ranks) > 2
True
>>> print newly_ranks[0].menu.add_timestamp >= newly_ranks[1].menu.add_timestamp
True
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from mealing.ranks import Temperature
from mealing.models import Menu, PopMenuRank, NewlyMenuRank
from mealing.utils import datetime_to_timestamp
import logging
import bisect
import datetime
import time


STEP = 1000

def _rank_pop_menu():
    offset = 0
    menus = Menu.objects.all()[:offset + STEP]
    today = datetime.datetime(1, 1, 1).today()
    sorted_menus = []
    while len(menus) > 0:
        for menu in menus:
            if menu.last_order_datetime is None:
                day_distance = today.date() - datetime.datetime(1, 1, 1).fromtimestamp(0).date()
            else:
                day_distance = today.date() - menu.last_order_datetime.date()
            logging.debug("day distance %d" % day_distance.days)
            score = Temperature(menu.order_number, day_distance.days, gravityth_power = 1.2).score
            pos = bisect.bisect(sorted_menus, (score, menu))
            sorted_menus.insert(pos, (score, menu))
            if len(sorted_menus) > settings.RANK_TOP:
                sorted_menus.pop(0)
        offset += STEP
        menus = Menu.objects.all()[offset:offset + STEP]
    #insert to db
    total_menus = len(sorted_menus)
    index = total_menus
    for score, menu in sorted_menus:
        rank = PopMenuRank(id = index, menu = menu, score = score)
        rank.save()
        logging.debug("rank %d, score %f" % (index, score))
        index -= 1
        if index <= 0:
            break


def _rank_newly_menu():
    offset = 0
    menus = Menu.objects.all()[:offset + STEP]
    today = int(time.time())
    sorted_menus = []
    while len(menus) > 0:
        for menu in menus:
            time_distance = today - menu.add_timestamp
            score = Temperature(1000, time_distance, gravityth_power = 1.2).score
            pos = bisect.bisect(sorted_menus, (score, menu))
            sorted_menus.insert(pos, (score, menu))
            if len(sorted_menus) > settings.RANK_TOP:
                sorted_menus.pop(0)
        offset += STEP
        menus = Menu.objects.all()[offset:offset + STEP]
    #insert to db
    total_menus = len(sorted_menus)
    index = total_menus
    for score, menu in sorted_menus:
        rank = NewlyMenuRank(id = index, menu = menu, score = score)
        rank.save()
        logging.debug("rank %d, score %f" % (index, score))
        index -= 1
        if index <= 0:
            break


class Command(BaseCommand):
    args = ""
    help = "Computer all ranks."
    
    def handle(self, *args, **options):
        logging.debug("rank start")
        _rank_pop_menu()
        _rank_newly_menu()
        logging.debug("rank end")
        