#!/bin/env python
# coding=utf-8
'''User need to modify it. 
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from settings import *
import os
import logging


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mealing_pro',  # Or path to database file if using sqlite3.
        'USER': 'cacti',  # Not used with sqlite3.
        'PASSWORD': 'cacti',  # Not used with sqlite3.
        'HOST': '192.168.16.205',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
        'TEST_CHARSET': "utf8",
    }
}

CACHE_BACKEND = 'memcached://192.168.16.205:11211/?max_entries=2048&timeout=5&cull_percentage=10'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

#for logging
LOG_FILENAME = "mealing.debug.log"
LEVEL = logging.WARNING
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), LOG_FILENAME),
    level = LEVEL,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)
    
    
EMAIL_HOST = "mail.funshion.com"
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = "[mealing]"
EMAIL_USE_TLS = False

"""app settings
"""
APP_NAME = u"风行订餐"
APP_DEVELOPER = u"pengxt <pengxt@funshion.com>"
    
