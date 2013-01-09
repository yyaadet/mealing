#!/bin/env python
# coding=utf-8
''' order is kernel functioin. we need test more carefully.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.utils import unittest
from django.test.client import Client
from mealing.models import Config


class OrderExamineTest(unittest.TestCase):
    """ examine order logic
    """
    url = "/order/ready/"
    
    def setUp(self):
        """ first init test instance
        """
        pass
    
    def test_when_order_shutdown(self):
        """ when order is shutdowned, order is denied.
        """
        
    