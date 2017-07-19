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
    url(r'^settings/global$', views.global_settings, name='global_settings'),
    url(r'^settings/kubernetes$', views.kubernetes_settings, name='kubernetes_settings'),
    
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
    
    # cpu usage
    url(r'^usage/cpu$', op_views.get_cpu_usages, name='cpu_usage'),
    url(r'^usage/memory$', op_views.get_memory_usages, name='memory_usage'),
]
