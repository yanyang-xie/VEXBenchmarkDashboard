# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase

from authen.models import MyUser

class MyUserTestCase(TestCase):
    def setUp(self):
        self.user_name = 'test_user_fake_1'
        self.password = 'test_user_fake_1@fake.com'
        self.nickname = 'test_user_fake_nick_name_1'

    def test_version_insert(self):
        user = User.objects.create(username=self.user_name, password=self.password)
        MyUser.objects.create(nickname=self.nickname, user=user)
        
        my_user = MyUser.objects.get(user__username=self.user_name)
        self.assertEqual(my_user.nickname, self.nickname)
    
    def tearDown(self):
        MyUser.objects.filter(nickname=self.nickname).delete()