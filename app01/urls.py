#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"
# Date: 2017/11/22


from django.conf.urls import url

from  app01 import views

urlpatterns = [
    url(r'^poll/$', views.poll),
    url(r'^comment/$', views.comment),
    url(r'^manage/$', views.manage),
    url(r'^uploadFile$', views.uploadFile),
    url(r'^backend/addArticle/$', views.addArticle),
    url(r'^commentTree/(?P<article_id>\d+)$', views.commentTree),
    url(r'^(?P<username>.*)/(?P<condition>tag|category|date)/(?P<para>.*)', views.homeSite),  # 个人首页分类地址
    url(r'^(?P<username>.*)/p/(?P<para>.*)', views.articleDetail),  # 文章具体内容地址
    url(r'^(?P<username>.*)', views.homeSite, name="aaa"),  # 个人首页地址

]
