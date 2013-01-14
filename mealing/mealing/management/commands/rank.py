#!/bin/env python
# coding=utf-8
''' computer ranks
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.core.management.base import BaseCommand, CommandError
from mealing.ranks import Temperature
from mealing.models import Menu
import logging
import bisect
import datetime


STEP = 1000

def _rank_pop_menu():
    offset = 0
    menus = Menu.objects.all()[:offset + STEP]
    today = datetime.datetime(1, 1, 1).today()
    sorted_menus = []
    while len(menus) > 0:
        for menu in menus:
            datetime_distance = today - menu.last_order_datetime
            score = Temperature(menu.order_number, datetime_distance.day).score
            pos = bisect.bisect(sorted_menus, (score, menu))
            sorted_menus.insert(pos, (score, menu))
        offset += STEP
        menus = Menu.objects.all()[offset:offset + STEP]
    #insert to db
    index = 1
    for score, menu in sorted_menus:
        rank = PopMenuRank(pk = index, menu = menu, score = score)
        rank.save()


class Command(BaseCommand):
    args = ""
    help = "Computer all ranks."
    
    def handle(self, *args, **options):
        logging.debug("rank start")
        _rank_pop_menu()
        logging.debug("rank end")
        