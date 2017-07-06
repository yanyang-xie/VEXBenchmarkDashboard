# -*- coding:utf-8 -*-
import logging
import json

from django.http.response import HttpResponse
from django.shortcuts import render_to_response

from dashboard.models import OperationGroup, VEXOperation, Operation, VEXVersion
from dashboard.utils import generate_user_context, get_default_deploy_version


logger = logging.getLogger(__name__)

def env_operation(request):
    context = {'active_menu':'env_operation'}
    context.update(generate_user_context(request))
    
    vex_operation_list = VEXOperation.objects.all()
    if get_default_deploy_version() is True :
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

def get_component_status_by_status_cmd():
    #@todo: 这个是将来定时, 从数据库中找出所有有status url的model,然后抓取status
    pass

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
    
    json_data = json.dumps(status_list)
    logger.debug('Fetch Operation status: %s' %(json_data))
    return HttpResponse(json_data, content_type="application/json")

def _generate_component_status_basic_dict(vex_op):
    op_dict = {'id':vex_op.id, 'name':vex_op.name}
    if vex_op.status is not None:
        op_dict.update({'status': 1 if vex_op.status.status_flag is True else 0})
    else:
        op_dict.update({'status':2})
        
    return op_dict