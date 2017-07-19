from dashboard.models import VEXGolbalSettings, KubernetesSettings


def permission_check(user):
    if user.is_authenticated():
        return user.myuser.permission > 1
    else:
        return False

def generate_user_context(request):
    #user = request.user if request.user.is_authenticated() else None
    #use_context = {'user':user}
    #return use_context
    
    user = request.user if request.user.is_authenticated() else None
    return {'user':user, 'username': request.session.get('username', None)}

def use_global_deploy_version():
    global_setting = VEXGolbalSettings.objects.all()
    if global_setting.count() > 0:
        return global_setting[0].use_default_version

def get_kube_host():
    kube_setting = KubernetesSettings.objects.all()
    if kube_setting.count() > 0:
        s = kube_setting[0]
        return s.kubectl_ip_address, s.kubectl_ssh_key_file,s.kubectl_ssh_user, s.kubectl_ssh_port
    else:
        return None,None,None,None

def get_grafana_server():
    global_setting = VEXGolbalSettings.objects.all()
    if global_setting.count() > 0:
        return global_setting[0].grafana_http_address
    else:
        return None

def get_prometheus_server():
    global_setting = VEXGolbalSettings.objects.all()
    if global_setting.count() > 0:
        return global_setting[0].prometheus_http_address
    else:
        return None

