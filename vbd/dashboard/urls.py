'''
Created on Jun 28, 2017

@author: xieyanyang
'''

from django.conf.urls import url

from dashboard import views, op_views, result_views


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
    url(r'^op/update$', op_views.update_benchmark_config, name='update_benchmark_config'),
    
    
    # Benchmark operation Home
    url(r'^bop$', op_views.benchmark_operation, name='benchmark_operation'),
    
    # Benchmark result Home
    url(r'^result/(?P<test_type>.+)', result_views.benchmark_result, name='benchmark_result'),
    
    # period scrapy component status
    url(r'^scrapy$', op_views.period_scrapy_component_status_by_status_cmd, name='scrapy_status'), 
    
]
