from django.conf.urls import include, url
from django.contrib import admin
from dashboard import views

handler404 = 'dashboard.views.page_not_found'
handler500 = 'dashboard.views.page_error'

urlpatterns = [
    # Examples:
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about$', views.about, name='about'),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('authen.urls')),
    url(r'', include('dashboard.urls')),
    
    url(r'^captcha/', include('captcha.urls')),
]

