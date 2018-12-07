# -*- coding: utf-8 -*-
# @Date    : 2018-12-06 14:06:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
from django.forms import ModelForm, TextInput, Textarea
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ""}
        widget = {
            "text": Textarea({'cols': 80, 'rows': 20}),
        }
