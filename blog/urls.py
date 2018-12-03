# -*- coding: utf-8 -*-
# @Date    : 2018-11-26 22:25:29
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
from django.urls import path
from . import views
from django.conf import settings
app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mdeditor/', views.BlogCreate.as_view(), name='blog-add'),
    path('mdeditor/<int:pk>/', views.BlogUpdate.as_view(), name='blog-edit'),
    path('article/<int:article_id>', views.Article.as_view(), name='article'),
    path('article/<username>/', views.UserBlogList.as_view(), name="blog-list"),
    path('post/public/<int:id>', views.post_public, name='public'),
    path('post/private/<int:id>', views.post_private, name='private'),
    path('cancel/<int:id>', views.cancel, name='cancel'),
    path('trash/<int:id>', views.move_to_trash, name='trash'),
    path('delete/<int:id>', views.delete_blog_completely, name='delete'),
    path('recover/<int:id>', views.recover, name='recover'),
]
