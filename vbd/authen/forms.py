# -*- coding:utf-8 -*-
"""
用户进行验证时的表单
"""
import re

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from .models import MyUser

# 方便选择
error_messages = {
    'username': {
        'required': u'用户名必须填写',
        'min_length': u'用户名长度过短(5-128)个字符',
        'max_length': u'用户名长度过长(5-128)个字符',
        'invalid': u'用户名格式错误，只能包含字母、数字、下划线',
    },
    'nickname': {
        'min_length': u'昵称长度过短(5-128)个字符',
        'max_length': u'昵称长度过长(5-128)个字符',
        'invalid': u'昵称格式错误，只能包含字母、数字、下划线',
    },
    'email': {
        'required': u'电子邮件地址必须填写',
        'invalid': u'不是正确的电子邮件格式',
    },
    'password': {
        'required': u'密码必须填写',
        'min_length': u'密码长度过短(4-15)个字符',
        'max_length': u'密码长度过长(4-15)个字符',
    }
}

class registrationForm(forms.Form):
    username = forms.CharField(help_text='请输入你的用户名', required=True, min_length=5, max_length=128, error_messages=error_messages['username'],)
    nickname = forms.CharField(help_text='请输入你的昵称', min_length=5, max_length=128, error_messages=error_messages['nickname'],)
    password = forms.CharField(help_text='请输入你的密码', required=True, min_length=5, max_length=128, error_messages=error_messages['password'])
    password_repeat = forms.CharField(help_text='重复密码', required=True, min_length=5, max_length=128, error_messages=error_messages['password'])
    email = forms.EmailField(help_text='请输入你的注册邮箱', required=True, error_messages=error_messages['email'])

    class Meta:
        model = MyUser
        #exclude = ['user',]

    # 使用 clean__attribute 来对属性进行验证
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('用户名中只能包含字母、数字和下划线')
        
        try:
            MyUser.objects.get(user__username=username)
            raise forms.ValidationError(u'用户名已经被注册')
        except MyUser.DoesNotExist:
            if username in settings.RESERVED:
                raise forms.ValidationError(u'用户名中包含保留字符或者敏感字符')

        # 最终都要返回该属性
        return username

    def clean_email(self):
        # 验证是否被注册过
        email = self.cleaned_data.get('email')
        try:
            email = MyUser.objects.get(user__email=email)
            raise forms.ValidationError(u'邮箱已经被注册')
        except MyUser.DoesNotExist:
            return email

    def clean_password_repeat(self):
        # 验证密码是否相同
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError(u'密码确认错误')
        return password_repeat

    def save(self):
        # save函数不用 Super(),默认的保留关键字 commit=True
        user = super(registrationForm, self).save()
        return user


class loginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=128,
                               help_text=u'请输入用户名',
                               error_messages=error_messages.get('username'))
    password = forms.CharField(min_length=5, max_length=128,
                               help_text=u'请输入密码',
                               error_messages=error_messages.get('password'))

    def __init__(self, *args, **kwargs):

        super(loginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
                'username',
                'password',

        )

    # 重载 clean 方法
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(u'用户名或密码不正确')
        elif not user.is_active:
            raise forms.ValidationError(u'该用户已被管理员设置为未激活状态')

        return password


# 重新设置密码
class settingpasswordForm(forms.Form):
    password_old = forms.CharField(min_length=4, max_length=128,
                                   help_text=u'请输入之前的密码')

    password_new = forms.CharField(min_length=4, max_length=128,
                                   error_messages=error_messages.get('password'),
                                   help_text='请输入新的密码')
    password_repeat = forms.CharField(min_length=4, max_length=128,
                                      error_messages=error_messages.get('password'),
                                      help_text='请再次输入新的密码'
                                      )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(settingpasswordForm, self).__init__(*args, **kwargs)

    def clean_password_old(self):
        # 只验证，将更新的工作放在 views 里做
        password_old = self.cleaned_data.get('password_old')
        if not self.user.check_password(password_old):
            raise forms.ValidationError(u'原始密码错误')
        
        return password_old
    
    def clean_password_repeat(self):
        # 只验证，将更新的工作放在 views 里做
        password_new = self.cleaned_data.get('password_new')
        password_repeat = self.cleaned_data.get('password_repeat')

        if password_new != password_repeat:
            raise forms.ValidationError(u'两次密码不统一')
        return password_new

