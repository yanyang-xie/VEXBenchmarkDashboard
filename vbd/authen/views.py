# -*- coding:utf-8 -*-
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render

from authen.forms import ForgetPwdForm

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
        
        context = {'form': form, 'user': user, 'send_status': True}
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