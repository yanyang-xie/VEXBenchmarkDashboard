# -*- coding:utf-8 -*-
"""
用正则来匹配访问的 url 路径
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.user_register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^set_password/$', views.user_set_password, name='set_password'),
    url(r'^forget_password/$', views.user_forget_password, name='forgetPassword'),
    
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.reset_password_confirm, name='password_reset_confirm'), 
]
