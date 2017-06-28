'''
Created on Jun 28, 2017

@author: xieyanyang
'''

from django.conf.urls import url

urlpatterns = [
    # Examples:
    #url(r'^$', 'dashboard.views.home', name='home'),
    url(r'^bop$', 'dashboard.views.benchmark_operation', name='benchmark_operation'),
    url(r'^envop$', 'dashboard.views.env_operation', name='env_operation'),
    url(r'^config$', 'dashboard.views.env_settings', name='env_settings'),
    
    url(r'^result/(?P<test_type>.+)', 'dashboard.views.benchmark_result', name='benchmark_result'),
]
