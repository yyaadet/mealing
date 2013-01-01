#!/bin/env python
# coding=utf-8
'''test definition.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

import doctest
from django.test import TestCase
from mealing.models import restaurant
from mealing.models import order
from mealing.models import user
from mealing.models import config
# models
from mealing import models
# admin
from mealing import admin
# views
from mealing.views import index
from mealing.views import user as userview
# forms
from mealing.forms import user as userform

class ModelsTest(TestCase):
    def test_models(self):
        doctest.testmod(restaurant)
        doctest.testmod(order)
        doctest.testmod(user)
        doctest.testmod(models)
        doctest.testmod(admin)
        doctest.testmod(index)
        doctest.testmod(userview)
        doctest.testmod(config)
        doctest.testmod(userform)