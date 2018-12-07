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
    path('article/<int:article_id>/', views.BlogCommentView.as_view(), name='article'),
    path('articlelist/<username>/', views.UserBlogListView.as_view(), name="blog-list"),
    path('postlist/', views.PostListAllView.as_view(), name='postlist'),
    path('postlist/public/', views.PostListPublicView.as_view(), name='postlist-public'),
    path('postlist/private/', views.PostListPrivateView.as_view(), name='postlist-private'),
    path('postlist/draft/', views.PostListDraftView.as_view(), name='postlist-draft'),
    path('postlist/trash/', views.PostListTrashView.as_view(), name='postlist-trash'),
    path('post/public/<int:id>/', views.post_public, name='public'),
    path('post/private/<int:id>/', views.post_private, name='private'),
    path('cancel/<int:id>/', views.cancel, name='cancel'),
    path('trash/<int:id>/', views.move_to_trash, name='trash'),
    path('delete/<int:id>/', views.delete_blog_completely, name='delete'),
    path('recover/<int:id>/', views.recover, name='recover'),
    path("collection/", views.CollectionListView.as_view(), name='collection'),
    path('search/', views.SearchView.as_view(), name="search")

]
