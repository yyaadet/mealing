#!/bin/env python
# coding=utf-8
'''User need to modify it. 
'''

__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


import os
import logging

from settings import *

STATUS = "dev"  # test, dev, pro

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mealing',  # Or path to database file if using sqlite3.
        'USER': 'cacti',  # Not used with sqlite3.
        'PASSWORD': 'cacti',  # Not used with sqlite3.
        'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

CACHE_BACKEND = 'memcached://192.168.16.205:11212/?max_entries=2048&timeout=5&cull_percentage=10'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

#for logging
LOG_FILENAME = "mealing.debug.log"
LEVEL = logging.DEBUG
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), LOG_FILENAME),
    level = LEVEL,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)


if STATUS == "dev" :
    DATABASES = {
       'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mealing',  # Or path to database file if using sqlite3.
            'USER': 'cacti',  # Not used with sqlite3.
            'PASSWORD': 'cacti',  # Not used with sqlite3.
            'HOST': '192.168.16.205',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',  # Set to empty string for default. Not used with sqlite3.
            'TEST_CHARSET': "utf8",
        }
    }
elif STATUS == "test":
    DATABASES = {
       'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mealing',  # Or path to database file if using sqlite3.
            'USER': 'cacti',  # Not used with sqlite3.
            'PASSWORD': 'cacti',  # Not used with sqlite3.
            'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',  # Set to empty string for default. Not used with sqlite3.
            'TEST_CHARSET': "utf8",
        }
    }
    CACHE_BACKEND = 'memcached://localhost:11211/?max_entries=2048&timeout=5&cull_percentage=10'
    
    
EMAIL_HOST = "mail.funshion.com"
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = "[mealing]"
EMAIL_USE_TLS = False
EMAIL_FROM = "mealing@funshion.com"

"""app settings
"""
APP_NAME = u"风行订餐"
APP_DEVELOPER = u"pengxt <pengxt@funshion.com>"
RANK_TOP = 50    
