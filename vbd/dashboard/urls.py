'''
Created on Jun 28, 2017

@author: xieyanyang
'''

from django.conf.urls import url

from dashboard import views, op_views

urlpatterns = [
    # Examples:
    #url(r'^$', 'dashboard.views.home', name='home'),
    
    # settings --> globalSettings
    url(r'^global_settings$', views.global_settings, name='global_settings'),
    
    # Basic Environment setting Home
    url(r'^env_setting$', op_views.env_setting, name='env_setting'),
    
    # Components status and operation
    url(r'^op/status$', op_views.fetch_component_status, name='fetch_compontent_status'),
    url(r'^op/execute$', op_views.execute_cmd, name='execute_cmd'),
    url(r'^op/update$', op_views.update_operation_config, name='update_operation_config'),
    
    
    # Benchmark operation Home
    url(r'^bop$', op_views.benchmark_operation, name='benchmark_operation'),
    
    
    
    
    
    
    
    url(r'^config$', views.env_settings, name='env_settings'),
    
    url(r'^result/(?P<test_type>.+)', views.benchmark_result, name='benchmark_result'),
]
