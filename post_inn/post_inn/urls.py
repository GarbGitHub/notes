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
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )
from accounts import urls as auth_urls
from notes.views import offline
from .views import robots_txt
from .yasg import urlpatterns as doc_urls
from fordev import urls as fordev_urls
from notes import urls as notes_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(notes_urls, namespace='notes'), name='notes'),
    path("robots.txt", robots_txt),
    path("offline.html", offline),
    path('sw.js', (TemplateView.as_view(template_name='notes/sw.js', content_type='application/javascript', )), name='sw.js'),
    path('pwabuilder-sw.js', (TemplateView.as_view(template_name='notes/pwabuilder-sw.js', content_type='application/javascript', )), name='pwabuilder-sw.js'),
    path('fordev/', include(fordev_urls, namespace='fordev'), name='fordev'),
    path('auth/', include(auth_urls, namespace='auth'), name='auth'),
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', 'rest_framework')),  # авторизация в api
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('summernote/', include('django_summernote.urls')),
]
urlpatterns += doc_urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
