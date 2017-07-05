# -*- coding:utf-8 -*-
import logging

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
