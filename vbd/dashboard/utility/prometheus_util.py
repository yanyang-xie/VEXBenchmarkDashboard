# -*- coding:utf-8 -*-
import datetime
import json

from dateutil.relativedelta import relativedelta
import requests

from dashboard.utility.date_util import datetime_2_long, convert_long_2_gmt_time

#time_window=-1, 抓取一小时之前的数据
def prometheus_query_range(prometheus_server, query, time_window=-1):
    base_url = '%s/api/v1/query_range' %(prometheus_server)
    
    now_long = datetime_2_long(datetime.datetime.now())
    one_hour_ago_long =  datetime_2_long(datetime.datetime.now() + relativedelta(hours=time_window))
    
    url = '%s?query=%s&start=%s&end=%s&step=60' %(base_url, query, one_hour_ago_long, now_long)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r
        else:
            return None
    except:
        print 'timeout'
    
def get_memory_usage_from_prometheus(prometheus_server):
    query = 'sum (container_memory_working_set_bytes{id="/",kubernetes_io_hostname=~".*"}) / sum (machine_memory_bytes{kubernetes_io_hostname=~".*"}) * 100'
    response = prometheus_query_range(prometheus_server, query)
    if response is not None:
        json_data = json.loads(response.text)
        metrics = json_data['data']['result']
        
        values_dict = _merge_prometheus_data(metrics)
        if len(values_dict) > 0:
            keys = values_dict.keys()
            keys.sort()
            value = values_dict[keys[-1]]
            return value[0]
        else:
            return 0
    else:
        return 0

def get_cpu_usage_from_prometheus(prometheus_server):
    query = '100 - (avg by (cpu) (irate(node_cpu{mode="idle", instance=~".*"}[5m])) * 100)'
    response = prometheus_query_range(prometheus_server, query)
    if response is not None:
        json_data = json.loads(response.text)
        metrics = json_data['data']['result']
        values_dict = _merge_prometheus_data(metrics)
        
        # convert to armchart format
        #{"date": "Thu Jul 13 2017 00:33:17 GMT+0800 (CST)", "value": 1 });
        armchart_values = []
        keys = values_dict.keys()
        keys.sort()
        for time_value in keys:
            data_list = values_dict[time_value]
            value = sum(data_list)/len(data_list)
            armchart_values.append({"date":convert_long_2_gmt_time(time_value), "value": float('%.2f' % float(value))})
        return armchart_values
    else:
        return []

# Prometheus默认会几秒钟抓一起, 因此,一分钟之内会有多组数据, _merge_prometheus_data是把相同时间戳的数据合并
def _merge_prometheus_data(metrics):
    values_dict = {}
    for metric in metrics:
        value_metrics = metric['values']
        for time_value, metric_value in value_metrics:
            metric_value = float('%.2f' % float(metric_value))
            if values_dict.has_key(time_value):
                values_dict[time_value].append(metric_value)
            else:
                values_dict[time_value] = [metric_value]
    
    return values_dict

if __name__ == '__main__':
    prometheus_server = 'http://52.220.45.230:30900'    
    #query = '100 - (avg by (cpu) (irate(node_cpu{mode="idle", instance=~".*"}[5m])) * 100)'
    #print prometheus_query_range(prometheus_server, query)
    
    #armchart_values = get_cpu_usage_from_prometheus(prometheus_server)
    #for v in armchart_values:
    #    print v
    
    value = get_memory_usage_from_prometheus(prometheus_server)
    print value
    