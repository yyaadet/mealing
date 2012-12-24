#!/bin/env python
# coding=utf-8
'''test definition.

'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'

from mealing.models import restaurant
from django.test import TestCase
import doctest


"""
__test__ = {
            "Doctest":  restaurant.Restaurant,
        }
"""

class ModelTest(TestCase):
    
  def test_models(self):
    doctest.testmod(restaurant)