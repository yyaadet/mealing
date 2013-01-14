#!/bin/env python
# coding=utf-8
''' all rank view here.

>>> from django.test.client import Client

########### test pop_menu()
>>> c = Client()
>>> resp = c.get("/rank/pop_menu/")
>>> print resp.status_code
200
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from mealing.views.decorator import render_template
from mealing.models import PopMenuRank
from django.conf import settings


def pop_menu(request):
    """ to render pop menu rank
    """
    ranks = PopMenuRank.objects.all()[:settings.RANK_TOP]
    return render_template("rank_pop_menu.html", {"ranks": ranks}, request)