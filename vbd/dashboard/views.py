from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'dashboard/vod.html')

def about(request):
    return render(request, 'about.html')

def benchmark_operation(request):
    context = {'active_menu':'benchmark_operation'}
    return render(request, 'dashboard/vod.html', context)

def env_operation(request):
    context = {'active_menu':'env_operation'}
    return render(request, 'dashboard/vod.html', context)

def env_settings(request):
    context = {'active_menu':'env_settings'}
    return render(request, 'dashboard/vod.html', context)

def benchmark_result(request, test_type):
    context = {'active_menu':'benchmark_result'}
    return render(request, 'dashboard/vod.html', context)
