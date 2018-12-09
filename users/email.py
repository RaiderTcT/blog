# -*- coding: utf-8 -*-
# @Date    : 2018-12-07 14:52:36
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
import threading
from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings


class MyEmailThread(threading.Thread):
    """多线程，发送邮件"""

    def __init__(self, subject_template_name, email_template_name, context, from_email,
                 recipient_list, fail_silently):
        threading.Thread.__init__(self)
        self.subject = loader.render_to_string(subject_template_name, context)
        self.subject = ''.join(self.subject.splitlines())
        self.body = loader.render_to_string(email_template_name, context)
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently

    # 发送邮件
    def run(self):
        email_message = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        print("fedffffdf")
        return email_message.send(self.fail_silently)


# 创建线程 start 启动线程活动，会调用run方法

def register_mail(token, user, recipient_list, current_site, use_https=False, *args, **kwargs):
    subject_template_name = 'email/register.txt'
    email_template_name = 'email/register.html'
    from_email = settings.EMAIL_HOST_USER
    fail_silently = False
    site_name = domain = current_site
    context = {
        'domain': domain,
        'site_name': site_name,
        'user': user,
        'token': token,
        'protocol': 'https' if use_https else 'http',
    }
    MyEmailThread(subject_template_name, email_template_name, context, from_email,
                  recipient_list, fail_silently).start()


# def send_mail(self, subject_template_name, email_template_name,
#               context, from_email, to_email, html_email_template_name=None):
#     """
#     Send a django.core.mail.EmailMultiAlternatives to `to_email`.
#     """
#     subject = loader.render_to_string(subject_template_name, context)
#     # Email subject *must not* contain newlines
#     subject = ''.join(subject.splitlines())
#     body = loader.render_to_string(email_template_name, context)

#     email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
#     if html_email_template_name is not None:
#         html_email = loader.render_to_string(html_email_template_name, context)
#         email_message.attach_alternative(html_email, 'text/html')

#     email_message.send()
