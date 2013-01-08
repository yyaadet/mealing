#!/usr/bin/env python
# coding=utf-8
''' manage utility.
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
