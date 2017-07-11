# -*- coding:utf-8 -*-
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

from dashboard.forms import VEXGolbalSettingsFrom
from dashboard.models import VEXGolbalSettings
from dashboard.utils import generate_user_context


logger = logging.getLogger(__name__)

# Create your views here.
def homepage(request):
    context = generate_user_context(request)
    return render(request, 'dashboard/homepage.html', context)

def page_not_found(request):
    return render_to_response('404.html')

def page_error(request):
    return render_to_response('500.html')

def about(request):
    context = generate_user_context(request)
    return render(request, 'about.html', context)

@login_required 
def global_settings(request):
    context = generate_user_context(request)
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










