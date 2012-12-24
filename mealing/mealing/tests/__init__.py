#!/bin/env python
# coding=utf-8
'''test definition.

'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

import doctest
from django.test import TestCase
from mealing.models import restaurant
from mealing import models
from mealing import admin

"""
__test__ = {
            "Doctest":  restaurant,
        }

"""

class ModelsTest(TestCase):
    def test_models(self):
        doctest.testmod(restaurant)
        doctest.testmod(models)
        doctest.testmod(admin)