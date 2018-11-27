# -*- coding: utf-8 -*-
# @Date    : 2018-11-27 16:11:20
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
from django.forms import EmailField
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.conf import settings
from .models import myUser


class RegisterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = myUser
        fields = ("username", "email")
        field_classes = {'username': UsernameField}
