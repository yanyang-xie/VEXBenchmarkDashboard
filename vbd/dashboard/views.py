from django.shortcuts import render

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
