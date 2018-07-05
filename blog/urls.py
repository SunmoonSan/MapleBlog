#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 18-4-10 下午11:23
# @site  : https://github.com/SunmoonSan
from django.urls import path
from . import views

from haystack.views import SearchView

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    # path('', SearchView(), name='haystack_search'),
    path('home_modify_intro/', views.home_modify_intro, name='home_modify_intro'),
    path('archive/', views.archive, name='archive'),
    path('profile/', views.profile, name='profile'),
    path('imagecrop/', views.my_image, name='imagecrop'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='blog_login'),
    path('logout/', views.logout, name='blog_logout'),
    path('publish/', views.blog_publish, name='blog_publish'),
    # path('list/', views.blog_list, name='blog_list'),
    path('list/', views.BlogListView.as_view(), name='article_list'),
    path('detail/<int:article_id>/', views.blog_detail, name='blog_detail'),
    path('publish_comment/', views.blog_publish_comment, name='blog_publish_comment'),
    path('like_article/', views.blog_like_article, name='like_article'),
    path('like_comment/', views.blog_like_comment, name='like_comment'),
    path('reply_comment/', views.blog_reply_comment, name='reply_comment'),
    path('reply_reply/', views.blog_reply_reply, name='reply_reply')
]
