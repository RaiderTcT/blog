# -*- coding: utf-8 -*-
# @Date    : 2018-11-26 22:25:29
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
from django.urls import path
from . import views
from django.conf import settings
app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('mdeditor/', views.BlogCreate.as_view(), name='blog-add'),
    path('mdeditor/<int:pk>/', views.BlogUpdate.as_view(), name='blog-edit'),
    path('article/<int:article_id>', views.Article.as_view(), name='article'),
    path('article/<username>/', views.BlogList.as_view(), name="blog-list"),
]
