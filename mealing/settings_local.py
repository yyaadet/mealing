#!/bin/env python
# coding=utf-8
'''User need to modify it. 

'''

__author__ = 'pengxt <pengxt@funshion.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


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

CACHE_BACKEND = 'memcached://192.168.16.205:11211/?max_entries=2048&timeout=5&cull_percentage=10'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

if STATUS == "dev" :
    DATABASES = {
       'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mealing',  # Or path to database file if using sqlite3.
            'USER': 'cacti',  # Not used with sqlite3.
            'PASSWORD': 'cacti',  # Not used with sqlite3.
            'HOST': '192.168.16.205',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',  # Set to empty string for default. Not used with sqlite3.
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
        }
    }
    
    