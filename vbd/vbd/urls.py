from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'dashboard.views.homepage', name='homepage'),
    url(r'^about$', 'dashboard.views.about', name='about'),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app1/', include('authen.urls')),
    url(r'^app2/', include('dashboard.urls')),
]

