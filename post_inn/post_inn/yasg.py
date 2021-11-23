from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

title = 'Notes API'
short_description = f'{title} предоставляет возможность взаимодействия с Сервисом Notes с целью получения различных ' \
                    f'данных, а также выполнения операций обновления, добавления, удаления. \n\n ' \
                    f'\n\nАутентификация\n\n Каждый запрос к Notes API (за исключение аутентификации) должен ' \
                    f'содержать аутентификационный токен (access token).' \
                    f'\nДля получения токена необходимо выполнить метод token_create. В ответ вы получите два токена:' \
                    f'\n - access token для запросов, имеет время жизни' \
                    f'\n - refresh token (с большим временем жизни чем access token) необходим для создания нового ' \
                    f'access токена, если он больше не действительный. Используйте метод token_refresh_create\n\n'

schema_view = get_schema_view(
    openapi.Info(
        title=title,
        default_version='v1',
        description=short_description,
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
