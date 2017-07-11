# -*- coding=utf-8 -*-
'''
Created on Jun 30, 2017

@author: xieyanyang
'''

'''
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'common-templates')),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # 自定义session处理方法. 可以将期望的数据加入到context中.
                'authen.context_processor.fillup_user_into_context',
            ],
        },
    },
]
'''

#将username填充到context中, 使得templetes中可以通过{{username}}获取
def fillup_user_into_context(request):
    user = request.user if request.user.is_authenticated() else None
    return {'user':user, 'username': request.session.get('username', None)}