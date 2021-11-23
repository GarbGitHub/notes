"""post_inn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )
from accounts import urls as auth_urls
from fordev import urls as fordev_urls

urlpatterns = [
    path('', include('notes.urls')),
    path('fordev/', include(fordev_urls, namespace='fordev'), name='fordev'),
    path('auth/', include(auth_urls, namespace='auth'), name='auth'),
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', 'rest_framework')),  # авторизация в api
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
