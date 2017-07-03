# -*- coding:utf-8 -*-
import re

from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate

from .models import MyUser

# 方便选择错误消息
error_messages = {
    'username': {
        'required': u'Username is required',
        'min_length': u'Username is too short(5-128)',
        'max_length': u'Username is too long(5-128)',
        'invalid': u'Username format is illegal (support number, letters and _)',
    },
    'nickname': {
        'min_length': u'Nickname is too short(5-128)',
        'max_length': u'Nickname is too long(5-128)',
        'invalid': u'Username format is illegal (support number, letters and _)',
    },
    'email': {
        'required': u'Email is required',
        'invalid': u'Email format is not validated',
    },
    'password': {
        'required': u'Password is required',
        'min_length': u'Password is too short(4-15)',
        'max_length': u'Password is too long(4-15)',
    }
}

class registrationForm(forms.Form):
    username = forms.CharField(help_text='Please input your user name', required=True, min_length=5, max_length=128, error_messages=error_messages['username'],)
    nickname = forms.CharField(help_text='Please input your nick name', min_length=5, max_length=128, error_messages=error_messages['nickname'],)
    password = forms.CharField(help_text='Please input your password', required=True, min_length=5, max_length=128, error_messages=error_messages['password'])
    password_repeat = forms.CharField(help_text='Please confirm your password', required=True, min_length=5, max_length=128, error_messages=error_messages['password'])
    email = forms.EmailField(help_text='Please input your email', required=True, error_messages=error_messages['email'])

    class Meta:
        model = MyUser
        # exclude = ['user',]

    # 使用 clean__attribute 来对属性进行验证
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username format is illegal (support number, letters and _)')
        
        try:
            MyUser.objects.get(user__username=username)
            raise forms.ValidationError(u'Username is registered')
        except MyUser.DoesNotExist:
            if username in settings.RESERVED:
                raise forms.ValidationError(u'Username contains illegal words')

        # 最终都要返回该属性
        return username

    def clean_email(self):
        # 验证是否被注册过
        email = self.cleaned_data.get('email')
        try:
            email = MyUser.objects.get(user__email=email)
            raise forms.ValidationError(u'Email is registered')
        except MyUser.DoesNotExist:
            return email

    def clean_password_repeat(self):
        # 验证密码是否相同
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError(u'The two password fields didn\'t match.')
        return password_repeat

    def save(self):
        # save函数不用 Super(),默认的保留关键字 commit=True
        user = super(registrationForm, self).save()
        return user


class loginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=128,
                               help_text=u'Please input your user Name',
                               error_messages=error_messages.get('username'))
    password = forms.CharField(min_length=5, max_length=128,
                               help_text=u'Please input your password',
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
            raise forms.ValidationError(u'Password is not right')
        elif not user.is_active:
            raise forms.ValidationError(u'The user is not active')

        return password


# 重新设置密码
class settingpasswordForm(forms.Form):
    password_old = forms.CharField(min_length=4, max_length=128,
                                   help_text=u'Please input older password')

    password_new = forms.CharField(min_length=4, max_length=128,
                                   error_messages=error_messages.get('password'),
                                   help_text='Please input new password')
    password_repeat = forms.CharField(min_length=4, max_length=128,
                                      error_messages=error_messages.get('password'),
                                      help_text='Please input new password once more'
                                      )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(settingpasswordForm, self).__init__(*args, **kwargs)

    def clean_password_old(self):
        # 只验证，将更新的工作放在 views 里做
        password_old = self.cleaned_data.get('password_old')
        if not self.user.check_password(password_old):
            raise forms.ValidationError(u'Older password is wrong')
        
        return password_old
    
    def clean_password_repeat(self):
        # 只验证，将更新的工作放在 views 里做
        password_new = self.cleaned_data.get('password_new')
        password_repeat = self.cleaned_data.get('password_repeat')

        if password_new != password_repeat:
            raise forms.ValidationError(u'The two password fields didn\'t match.')
        return password_new

class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True, help_text='Please input your email')
    captcha = CaptchaField(error_messages={"invalid": u"Verification code is wrong"}, help_text='Please input verification code')
    
    def clean_email(self):
        # 验证是否被注册过
        email = self.cleaned_data.get('email')
        try:
            MyUser.objects.get(user__email=email)
            return email
        except MyUser.DoesNotExist:
            raise forms.ValidationError(u'The email is not registered')

class ResetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"), widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'], code='password_mismatch', )
        return password2
