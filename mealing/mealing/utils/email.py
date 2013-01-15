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

def send_mail(subject, msg, to, cc, use_thread = True):
    """ to send text email
    """
    if use_thread:
        thread = threading.Thread(target = _send_mail_thread, name = "send_email_cli", args = (subject, msg, to , cc))
        thread.setDaemon(True)
        #thread.start()
        thread.run()
    else:
        _send_mail_thread(subject, msg, to, cc)
    
    
def _send_mail_thread(subject, msg, to, cc):
    """ run in thread
    """
    new_msg = msg
    new_msg += "\r\n\r\n\r\n\r\n"
    new_msg += "\r\n=====\r\n"
    new_msg += u"风行订餐 <http://mealing.funshion.com>"
    email = EmailMessage(subject, new_msg, settings.EMAIL_FROM, 
                         to, [], cc = cc)
    email.send()