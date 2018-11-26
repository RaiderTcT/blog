# -*- coding: utf-8 -*-
# @Date    : 2018-11-26 22:25:29
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
