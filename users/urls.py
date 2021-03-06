from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'users'
urlpatterns = [
    path('signin/', views.LoginView.as_view(), name='login'),
    path('signout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.RegisterView.as_view(), name='register'),
    path('confirm/<token>', views.register_confirm, name='confirm'),
    path('user/<user_username>/', views.user, name='user'),
    path('profile/<pk>/', views.Profile.as_view(), name='profile'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('follower/<username>/', views.FollowerView.as_view(), name='follower'),
    path('following/<username>/', views.FollowedView.as_view(), name='followed'),
    path('follow/<username>/', views.follow, name='follow'),
    path('unfollow/<username>/', views.unfollow, name='unfollow'),
    path('collect/<int:blog_id>/', views.collect, name='collect'),
    path('uncollect/<int:blog_id>/', views.uncollect, name='uncollect'),
]
