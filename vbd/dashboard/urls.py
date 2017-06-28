'''
Created on Jun 28, 2017

@author: xieyanyang
'''

from django.conf.urls import url

from dashboard import views

urlpatterns = [
    # Examples:
    #url(r'^$', 'dashboard.views.home', name='home'),
    url(r'^bop$', views.benchmark_operation, name='benchmark_operation'),
    url(r'^envop$', views.env_operation, name='env_operation'),
    url(r'^config$', views.env_settings, name='env_settings'),
    
    url(r'^result/(?P<test_type>.+)', views.benchmark_result, name='benchmark_result'),
]
