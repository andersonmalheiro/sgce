"""SGCE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^manager/login/$', auth_views.login, {'template_name': 'manager/login.html'}, name='login'),
    url(r'^manager/logout/$', auth_views.logout, {'template_name': 'manager/logout.html'}, name='logout'),
    url(r'^manager/password_change/$', auth_views.password_change, {'template_name': 'manager/password_change.html'}, name='password_change'),
    url(r'^manager/password_change/done/$', auth_views.password_change, name='password_change_done'),
    url(r'^admin/', admin.site.urls),
    url(r'', include('app.urls')),    
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
