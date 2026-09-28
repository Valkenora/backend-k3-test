"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .template_views import login_view, dashboard_view, hira_list_view, hira_create_view, ptw_list_view, ptw_create_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/hira/', include('hira.urls')),
    path('api/ptw/', include('ptw.urls')),
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('hira/', hira_list_view, name='hira-list'),
    path('hira/create/', hira_create_view, name='hira-create'),
    path('ptw/', ptw_list_view, name='ptw-list'),
    path('ptw/create/', ptw_create_view, name='ptw-create'),
    path('api/audit/', include('audit.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)