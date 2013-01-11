#!/bin/env python
# coding=utf-8
''' email utility.
use 'python -m smtpd -n -c DebuggingServer localhost:1025' to start smtpd

######### test send_mail()
>>> send_mail("hello world", "Good", ["pengxt@funshion.com"], [])
'''


__author__ = 'pengxt <164504252@qq.com>'
__status__ = 'Product'  # can be 'Product', 'Development', 'Prototype'


from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.conf import settings
import threading

def send_mail(subject, msg, to, cc):
    """ to send text email
    """
    thread = threading.Thread(target = _send_mail_thread, args = (subject, msg, to , cc))
    thread.start()
    thread.run()
    
    
def _send_mail_thread(subject, msg, to, cc):
    """ run in thread
    """
    email = EmailMessage(subject, msg, settings.EMAIL_FROM, 
                         to, [], cc = cc)
    email.send()