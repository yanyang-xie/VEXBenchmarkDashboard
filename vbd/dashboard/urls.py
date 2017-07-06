'''
Created on Jun 28, 2017

@author: xieyanyang
'''

from django.conf.urls import url

from dashboard import views, op_views

urlpatterns = [
    # Examples:
    #url(r'^$', 'dashboard.views.home', name='home'),
    url(r'^global_settings$', views.global_settings, name='global_settings'),
    url(r'^env_setting$', op_views.env_setting, name='env_setting'),
    
    url(r'^op/status$', op_views.fetch_component_status, name='fetch_compontent_status'),
    url(r'^op/execute$', op_views.execute_cmd, name='execute_cmd'),
    
    
    url(r'^bop$', views.benchmark_operation, name='benchmark_operation'),
    
    url(r'^config$', views.env_settings, name='env_settings'),
    
    url(r'^result/(?P<test_type>.+)', views.benchmark_result, name='benchmark_result'),
]
