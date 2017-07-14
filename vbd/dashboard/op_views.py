# -*- coding:utf-8 -*-
from datetime import datetime
import json
import logging
import subprocess

from dateutil.relativedelta import relativedelta
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import requests

from dashboard.models import OperationGroup, VEXOperation, Operation, VEXVersion, \
    CHOICES_TYPE, VEXPerfTestOperation, ServiceStatus, SERVICE_STATUS_TYPE
from dashboard.utils import use_global_deploy_version

logger = logging.getLogger(__name__)

def benchmark_operation(request):
    context = {'active_menu':'benchmark_operation'}
    #context.update(generate_user_context(request))
    
    vex_operation_list = VEXPerfTestOperation.objects.filter(perf_config__isnull=False)
    context.update({'vex_operation_list': vex_operation_list,})
    logger.debug('perf_op_index context: %s' %(context))
    
    return render_to_response('dashboard/perf_operation.html', context)

# update benchmark test configuration
@csrf_exempt
def update_benchmark_config(request):
    try:
        #print request.POST.items()
        pk = request.POST.get('pk')
        name = request.POST.get('name')
        value = int(request.POST.get('value'))
        logger.debug('Update: pk:%s, name:%s, value:%s' %(pk, name , value))
        vex_op_object = get_object_or_404(VEXPerfTestOperation, pk=pk)
        perf_config = vex_op_object.perf_config
        
        if name.find('content_size')>-1: perf_config.content_size=value
        if name.find('bitrate_number')>-1: perf_config.bitrate_number=value
        if name.find('warm_up_minute')>-1: perf_config.warm_up_minute=value
        
        if name.find('session_number')>-1:
            # to linear, if it is running, then session number could not be decreased.
            if perf_config.test_type in [CHOICES_TYPE[-1][0],] and vex_op_object.status_flag is True and value < perf_config.session_number:
                logger.error('Linear performance test is running, value of %s must be larger than before' %(name))
                response = HttpResponseBadRequest('Linear performance test is running, value of %s must be larger than before' %(name))
                return response
            else: 
                perf_config.session_number=value
        
        perf_config.save()
        return HttpResponse('Saved')
    except ValueError, e:
        logger.error('Value of %s must be int. %s' %(name, e))
        response = HttpResponseBadRequest('Value of %s must be int' %(name))
        return response
    except Exception, e:
        logger.error('Failed to save the change. %s' %e)
        response = HttpResponseServerError('Server ERROR')
        return response

# Execute command
def execute_cmd(request):
    try:
        op_id = request.GET.get('op_id')
        op_tag = request.GET.get('op_tag')
        vex_op = request.GET.get('vex_op')
        logger.debug("Operation:[id:%s, tag:%s, is_vex_op:%s]" %(op_id, op_tag, vex_op))
        
        command, obj = _get_operation_command(op_id, op_tag, vex_op)
        logger.debug("Operation:[id:%s, tag:%s]. Command is [%s]" % (op_id, op_tag, command))
        if command == "":
            raise Exception("Not found command['%s']" %(op_tag))
        
        # for vex customization
        if op_tag == 'deploy':
            # 如果设置了使用全局统一的版本, 那么则取默认的版本, 否则使用单独设置的版本
            is_use_global_deploy_version = use_global_deploy_version()
            if is_use_global_deploy_version is True:
                try:
                    version = get_object_or_404(VEXVersion, enable=True)
                except:
                    version = obj.deploy_version
            else:
                version = obj.deploy_version
            command += ' -v %s' %(version.version)
        
        stdout, stderr, ex = _execute_command(command, obj.command_timeout, True)
        if stderr is not None and len(stderr) > 0:
            logger.error("Failed to execute ['%s'] operation. Reason:[%s]" %(op_tag, str(stderr)))
            json_data = json.dumps({"status_code": 500, "message":"Failed to execute ['%s'] operation. Reason:[%s]" %(op_tag, str(stderr).replace('\n', ''))})
            #logger.error("Failed to execute ['%s'] operation. Reason:[%s]" %(op_tag, str(stderr).replace('\n', '')))
            return HttpResponse(json_data, content_type="application/json")
        elif ex is not None:
            logger.error("Failed to execute ['%s'] operation. Reason:[%s]" %(op_tag, str(ex)))
            json_data = json.dumps({"status_code": 500, "message":"Failed to execute ['%s'] operation. Reason:[%s]" %(op_tag, str(ex).replace('\n', ''))})
            return HttpResponse(json_data, content_type="application/json")
        else:
            status_flag = None
            if op_tag == 'start':
                status_flag = True
            elif op_tag == 'stop':
                status_flag = False
            
            if status_flag is not None:
                service_status_obj = obj.status
                service_status_obj.status_flag = status_flag
                service_status_obj.save()
                logger.debug('Save operation status for %s to %s' %(obj.name, status_flag))
        
        logger.info("Operation:[id:%s, tag:%s]. Command is %s, response is '%s'" % (op_id, op_tag, command, stdout))
        # You can dump a lot of structured data into a json object, such as lists and tuples
        json_data = json.dumps({"status_code": 200, "message": "Success to execute %s [%s]" %(op_tag.lower(), obj.name.lower())})
        return HttpResponse(json_data, content_type="application/json")
    except Exception, e:
        logger.error("Internal Server ERROR. Failed to execute [%s] operation. %s" %(op_tag, e))
        json_data = json.dumps({"status_code": 500, "message":"Internal Server ERROR. <p>%s</p>" %(str(e))})
    return HttpResponse(json_data, content_type="application/json")

# Index of environment settings
def env_setting(request):
    context = {'active_menu':'env_setting'}
    #context.update(generate_user_context(request))
    
    vex_operation_list = VEXOperation.objects.all()
    if use_global_deploy_version() is True :
        version_objs = VEXVersion.objects.filter(is_default=True)
        if version_objs.count() > 0:
            for vex_operation in vex_operation_list:
                vex_operation.deploy_version = version_objs[0]
    
    operation_list = []
    groups = OperationGroup.objects.all()
    if groups.count() > 0:
        for group in groups:
            ops = Operation.objects.filter(group=group)
            if ops.count() > 0:
                operation_list.append(ops)
    
    no_group_ops = Operation.objects.filter(group=None)
    if no_group_ops.count() > 0:
        operation_list.append(no_group_ops)
        
    context.update({'operation_list': operation_list, 'vex_operation_list':vex_operation_list})

    logger.debug('Env operation context: %s' %(context))
    return render_to_response('dashboard/env_opertion.html', context)

#定时从数据库中找出所有有status url的model,然后抓取status
def period_scrapy_component_status():
    logger.debug("Start to scrapy component status")
    try:
        status_objs = ServiceStatus.objects.filter(status_cmd__isnull=False, )
        
        from vbd.settings import sched
        for status_obj in status_objs:
            execute_time = datetime.now() + relativedelta(seconds=+3)
            sched.add_date_job(_scrapy_component_status, execute_time, args=(status_obj, execute_time,))
    except Exception, e:
        print e
    logger.debug("Finish to scrapy component status")

def _scrapy_component_status(status_obj, execute_time):
    status_command = status_obj.status_cmd
    logger.debug("Start to scrapy by cmd at %s: %s" %(execute_time, status_command))
    stdout, stderr, ex = None, None,None
    if status_obj.status_cmd_type == SERVICE_STATUS_TYPE[0][0]:
        # shell
        stdout, stderr, ex = _execute_command(status_command)
    else:
        stdout, stderr, ex = _execute_command(status_command, status_obj.status_cmd_timeout, False)
    
    if ex is not None:
        #logger.error(type(ex))
        logger.error("Scrapy error: cmd:%s, timestamp:%s, error:%s" %(status_command, execute_time, str(type(ex))[0:200]))
        status_obj.status_response = str(ex)
        status_obj.status_flag=False
        status_obj.save()
        
    elif stderr is None or len(stderr) == 0:
        # get right status response
        logger.debug("Scrapy succeed: cmd:%s, timestamp:%s, message:%s" %(status_command, execute_time, stdout))
        status_obj.status_response = stdout
        status_obj.status_flag=True
        status_obj.save()
        
        # to vex operation, need parse its response
        _pasre_vex_components(status_obj)
    else:
        logger.error("Scrapy error: cmd:%s, timestamp:%s, error:%s" %(status_command, execute_time, str(stderr)[0:200]))
        status_obj.status_response = stderr
        status_obj.status_flag=False
        status_obj.save()

def _pasre_vex_components(status_obj):
    if VEXOperation.objects.filter(status=status_obj):
        logger.info("parse vex obj")

def fetch_component_status(request):
    status_list = []
    
    #get vex operation list
    vex_operation_list = VEXOperation.objects.all()
    for vex_op in vex_operation_list:
        op_dict = _generate_component_status_basic_dict(vex_op)
        op_dict.update({'tag':'vex_op', 'build_info': vex_op.build_info, 'running_version':vex_op.running_version})
        status_list.append(op_dict)
    
    #get operation list
    operation_list = Operation.objects.all()
    for op in operation_list:
        op_dict = _generate_component_status_basic_dict(op)
        op_dict.update({'tag':'basic_op'})
        status_list.append(op_dict)
    
    #get operation list
    benchmark_operation_list = VEXPerfTestOperation.objects.all()
    for op in benchmark_operation_list:
        op_dict = _generate_component_status_basic_dict(op)
        op_dict.update({'tag':'benchmark_op'})
        status_list.append(op_dict)
    
    json_data = json.dumps(status_list)
    logger.debug('Fetch Operation status: %s' %(json_data))
    return HttpResponse(json_data, content_type="application/json")

def _execute_command(cmd, timeout=30, is_shell=True):
    try:
        if is_shell is True:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=is_shell) 
            stdout, stderr = process.stdout.readlines(), process.stderr.readlines() 
            
            #import os, signal
            #os.kill(process.pid, signal.SIGKILL)
            return stdout, stderr, None
        else:
            #do_http
            r = requests.get(cmd, timeout=timeout)
            if r.status_code != 200 and r.status_code != 204:
                logger.debug('Service is not running. Cmd is %s, response status code is %s' %(cmd, r.status_code))
                return None, 'Service is not running', None
            else:
                return r.text, None, None
    except Exception, e:
        logger.error('Execute command error. Cmd is %s. Error is %s' %(cmd, e))
        return None, None, e

def _generate_component_status_basic_dict(vex_op):
    op_dict = {'id':vex_op.id, 'name':vex_op.name}
    if vex_op.status is not None:
        op_dict.update({'status': 1 if vex_op.status.status_flag is True else 0})
    else:
        op_dict.update({'status':2})
        
    return op_dict

def _get_operation_command(op_id, op_tag, is_vex_operation):
    if is_vex_operation == 'true':
        obj = get_object_or_404(VEXOperation, pk=op_id)
    else:
        obj = get_object_or_404(Operation, pk=op_id)
        
    command = ""
    if op_tag == "start" or op_tag == "run":
        command = obj.start_command
    elif op_tag == "stop":
        command = obj.stop_command
    elif op_tag == "status":
        command = obj.status_command
    elif op_tag == "result":
        command = obj.result_collect_command
    elif op_tag == "deploy":
        command = obj.deploy_command
    return command, obj

# get cluster cpu usage info 
def get_cpu_usages(requests):
    #@todo: get data from prometheus
    url = "";
    data_list = []
    data_list.append({"date": "Thu Jul 13 2017 00:33:17 GMT+0800 (CST)", "value": 1 });
    data_list.append({"date": "Thu Jul 13 2017 00:34:17 GMT+0800 (CST)", "value": 7 });
    data_list.append({"date": "Thu Jul 13 2017 00:35:17 GMT+0800 (CST)", "value": 13 });
    data_list.append({"date": "Thu Jul 13 2017 00:36:17 GMT+0800 (CST)", "value": 6 });
    data_list.append({"date": "Thu Jul 13 2017 00:33:17 GMT+0800 (CST)", "value": 40 });
    data_list.append({"date": "Thu Jul 13 2017 00:38:17 GMT+0800 (CST)", "value": 60 });
    data_list.append({"date": "Thu Jul 13 2017 00:40:17 GMT+0800 (CST)", "value": 20 });
    data_list.append({"date": "Thu Jul 13 2017 00:45:17 GMT+0800 (CST)", "value": 46 });
    data_list.append({"date": "Thu Jul 13 2017 00:48:17 GMT+0800 (CST)", "value": 55 });
    
    json_data = json.dumps(data_list)
    logger.debug('CPU Usage: %s' %(json_data))
    return HttpResponse(json_data, content_type="application/json")

def get_memory_usages(requests):
    #@todo: get data from prometheus
    url = "";
    data_list = []
    data_list.append({
              "category": "Wine left in the barrel",
              "value1": 30,
              "value2": 70
            });
    
    json_data = json.dumps(data_list)
    logger.debug('CPU Usage: %s' %(json_data))
    return HttpResponse(json_data, content_type="application/json")


