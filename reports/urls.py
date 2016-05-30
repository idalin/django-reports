#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dalin at 16-5-9
from django.conf.urls import patterns, url, include
from reports import views
import xadmin
xadmin.autodiscover()
app_name = 'reports'


#urlpatterns = [
#    url(r'^$', views.TestView.as_view(), name='index'),
#    url(r'^$', views.IndexView.as_view(), name='login'),
#    url(r'^$', views.IndexView.as_view(), name='logout'),
#    url(r'^$', views.IndexView.as_view(), name='register'),
#    url(r'^cd/$', views.CreateDatasourceView.as_view(), name='create'),
#]
urlpatterns = [
    url('^', include(xadmin.site.urls)),
]
