# -*- coding:utf-8 -*-
import logging
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

from dashboard.forms import VEXGolbalSettingsFrom, KubernetesSettingsFrom
from dashboard.models import VEXGolbalSettings, \
    KubernetesSettings, kube_file_folder


logger = logging.getLogger(__name__)

# Create your views here.
def homepage(request):
    #context = generate_user_context(request)
    context = {}
    return render(request, 'dashboard/homepage.html', context)

def page_not_found(request):
    return render_to_response('404.html')

def page_error(request):
    return render_to_response('500.html')

def about(request):
    #context = generate_user_context(request)
    context = {}
    return render(request, 'about.html', context)

@login_required 
def global_settings(request):
    #context = generate_user_context(request)
    context = {}
    if request.method == 'POST':
        form = VEXGolbalSettingsFrom(request.POST)
        if form.is_valid():
            VEXGolbalSettings.objects.all().delete()
            form.save()
        
        context['form'] = form
        return render(request, 'dashboard/global_settings.html', context)
    else:
        
        settings = VEXGolbalSettings.objects.all()
        if len(settings) > 0:
            # 给form初始值, 两种方式
            '''
            form = VEXGolbalSettingsFrom(initial={'grafana_http_address': settings[0].grafana_http_address,
                                                  'kubectl_ip_address': settings[0].kubectl_ip_address
                                                  })
            '''
            form = VEXGolbalSettingsFrom(instance = settings[0])
        else:
            form = VEXGolbalSettingsFrom()    
        
        context['form'] = form
        return render(request, 'dashboard/global_settings.html', context)


@login_required 
def kubernetes_settings(request):
    #context = generate_user_context(request)
    context = {}
    if request.method == 'POST':
        form = KubernetesSettingsFrom(request.POST, request.FILES)
        if form.is_valid():
            KubernetesSettings.objects.all().delete()
            '''
            key_file = request.FILES['kubectl_ssh_key_file']
            
            #store key file
            from vbd.settings import MEDIA_ROOT
            store_dir = MEDIA_ROOT + os.sep + kube_file_folder
            filename = os.path.join(store_dir, key_file.name);
            
            if os.path.exists(filename): 
                os.remove(filename)
            
            fobj = open(filename,'wb');
            for chrunk in key_file.chunks():
                fobj.write(chrunk);
            fobj.close();
            '''
            
            form.save()
        context['form'] = form
        return render(request, 'dashboard/kubernetes_settings.html', context)
    else:
        
        settings = KubernetesSettings.objects.all()
        if len(settings) > 0:
            # 给form初始值, 两种方式
            form = KubernetesSettingsFrom(instance = settings[0])
        else:
            form = KubernetesSettingsFrom(initial={'kubectl_ssh_user':'root', 'kubectl_ssh_port':22})    
        
        context['form'] = form
        return render(request, 'dashboard/kubernetes_settings.html', context)










