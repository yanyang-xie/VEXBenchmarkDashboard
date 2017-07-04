# -*- coding:utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.forms import VEXGolbalSettingsFrom
from dashboard.models import VEXGolbalSettings

@login_required 
def global_settings(request):
    context = _generate_user_context(request)
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

# Create your views here.
def homepage(request):
    context = _generate_user_context(request)
    return render(request, 'dashboard/vod.html', context)

def about(request):
    context = _generate_user_context(request)
    return render(request, 'about.html', context)

def benchmark_operation(request):
    context = {'active_menu':'benchmark_operation'}
    context.update(_generate_user_context(request))
    
    return render(request, 'dashboard/vod.html', context)

def env_operation(request):
    context = {'active_menu':'env_operation'}
    context.update(_generate_user_context(request))
    return render(request, 'dashboard/vod.html', context)

def env_settings(request):
    context = {'active_menu':'env_settings'}
    context.update(_generate_user_context(request))
    return render(request, 'dashboard/vod.html', context)

def benchmark_result(request, test_type):
    context = {'active_menu':'benchmark_result'}
    context.update(_generate_user_context(request))
    return render(request, 'dashboard/vod.html', context)

def _generate_user_context(request):
    user = request.user if request.user.is_authenticated() else None
    use_context = {'user':user}
    return use_context
