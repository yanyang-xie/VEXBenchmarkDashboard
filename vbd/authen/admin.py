# -*- coding:utf-8 -*-

"""
Register your model here
注册关于用户的信息
"""
from django.contrib import admin

from .models import MyUser


class ForumUserAdmin(admin.ModelAdmin):
    # 参见：http://stackoverflow.com/questions/163823/can-list-display-in-a-django-modeladmin-display-attributes-of-foreignkey-field
    list_display = ('get_name',)

    search_fields = ('get_name',)

    def get_name(self, obj):
        return obj.user.username

    get_name.admin_order_field = 'user'


admin.site.register(MyUser, ForumUserAdmin)
