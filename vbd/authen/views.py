# -*- coding:utf-8 -*-
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from authen.forms import ForgetPwdForm, ResetPasswordForm

from .forms import registrationForm, loginForm, settingpasswordForm
from .models import MyUser

def user_register(request):
    user = None
    if request.method == 'POST':
        # TODO 头像添加
        form = registrationForm(request.POST)
        if form.is_valid():
            information = form.cleaned_data
            username=information.get('username')
            password=information.get('password')
            email=information.get('email')
            
            new_user = User.objects.create_user(username=username, email=email, password=password, )
            new_user.save()
            forumUser = MyUser(user=new_user)
            forumUser.nickname = information.get('nickname')
            forumUser.save()
            #user_login(request)
            return HttpResponseRedirect(reverse('login'))
    else:
        form = registrationForm()

    context = {'form': form, 'user': user}
    return render(request, 'authen/user_register.html', context)

def user_login(request):
    user = None
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            information = form.cleaned_data
            username=information.get('username')
            password=information.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = str(user)
                return HttpResponseRedirect(reverse('homepage'))
    else:
        form = loginForm()
        user = None

    context = {'form': form, 'user': user}
    return render(request, 'authen/user_login.html', context)

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))

@login_required()
def user_set_password(request):
    # 重设密码
    user = request.user if request.user else None
    if request.method == 'POST' and user is not None:
        form = settingpasswordForm(request.POST, user=request.user)
        if form.is_valid():
            password = form.cleaned_data.get('password_new')
            user.set_password(password)
            user.save()
            messages.success(request, u'密码成功更新')
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = settingpasswordForm()
    context = {
        'form': form, 'user': user,
    }

    return render(request, 'authen/user_setpassword.html', context)

def user_forget_password(request):
    user = request.user
    
    if request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        # Validate the form: the captcha field will automatically
        # check the input
        if form.is_valid():
            human = True
        
            associated_users= User.objects.get(email=form.cleaned_data.get('email'))
            c = {
                'email': associated_users.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'your site',
                'uid': urlsafe_base64_encode(force_bytes(associated_users.pk)),
                'user': associated_users,
                'token': default_token_generator.make_token(associated_users),
                'protocol': 'http',
                }
            subject_template_name='registration/password_reset_subject.txt' 
            # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
            email_template_name='registration/password_reset_email.html'    
            # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, DEFAULT_FROM_EMAIL , [associated_users.email], fail_silently=False)
        
            context = {'form': form, 'user': user, 'send_status': True}
        else:
            context = {'form': form, 'user': user, 'send_status': False}
        return render(request, 'authen/user_forget_password.html', context)
    else:
        #刷新验证码
        if request.GET.get('newsn')=='1':
            csn=CaptchaStore.generate_key()
            cimageurl= captcha_image_url(csn)
            return HttpResponse(cimageurl)
        
        form = ForgetPwdForm()
    context = {'form': form, 'user': user, 'send_status': False}
    return render(request, 'authen/user_forget_password.html', context)

def reset_password_confirm(request, uidb64, token):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        UserModel = get_user_model()
        
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
        else:
            messages.error(request,'The reset password link is no longer valid.')
        
        context = {'form': form, 'user': user}
        return render(request, 'authen/user_reset_password_confirm.html', context)
    else:
        form = ResetPasswordForm()
        UserModel = get_user_model()
        
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
            messages.error(request,'The reset password link is no longer valid.')
        
        context = {'form': form, 'user': user}
        return render(request, 'authen/user_reset_password_confirm.html', context)
        
        
