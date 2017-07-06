from dashboard.models import VEXGolbalSettings


def permission_check(user):
    if user.is_authenticated():
        return user.myuser.permission > 1
    else:
        return False

def generate_user_context(request):
    user = request.user if request.user.is_authenticated() else None
    use_context = {'user':user}
    return use_context

def use_global_deploy_version():
    global_setting = VEXGolbalSettings.objects.all()
    if global_setting.count() > 0:
        return global_setting[0].use_default_version

