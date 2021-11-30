from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS

from accounts.models import User
from notes.models import Note
from api.serializers import NoteSerializer, ThinNoteSerializer, UserSerializer, ThinUserSerializer, \
    ThinBasketSerializer, BasketSerializer, UpdateBasketSerializer, SerializerWithoutEmailField, \
    ThinFavoritesSerializer, SerializerOnlyIsFavoritesField, NoteCreateSerializer, SerializerOnlyIsActiveField, \
    UserRegistration
from .permission import IsAuthor, IsAuthUser, IsAuthUserExcludePost


# Users
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(
        operation_summary="Получить детальную информацию о своем пользователе по {id}",
        operation_description="Получить детальную информацию пользователе по {id}. "
                              'Что бы узнать id пользователя, можно воспользоваться методом "users_list"',
        # operation_id="Method ID",
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='id пользователя (числовой тип)')
        ],
        responses={200: UserSerializer()}
    )
)
@method_decorator(
    name='list', decorator=swagger_auto_schema(
        operation_summary="Узнать id текущего пользователя",
        operation_description="Не требуется дополнительных параметров, в ответ вернется список из одного пользователя.",
        # operation_id="Method ID",
        responses={200: ThinUserSerializer()}
    )
)
@method_decorator(
    name='update', decorator=swagger_auto_schema(
        operation_summary='Внести изменения в профиль пользователя',
        operation_description='{name} - имя\n{last_name} - фамилия',
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='id пользователя (числовой тип)'),
        ],
        responses={200: ThinUserSerializer()}
    )
)
@method_decorator(
    name='create', decorator=swagger_auto_schema(
        operation_summary='Зарегистрировать нового пользователя (для неавторизованных пользователей)',
        operation_description='Вы должны быть не авторизованными, иначе сервер ответит 500 ошибкой\n\n'
                              '{email} - * email\n{name} - имя\n{last_name} - фамилия\n{password} - * пароль',
        responses={201: UserRegistration()}
    )
)
class UserViewsSet(ModelViewSet):
    """
    Информация о текущем пользователе
    """
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'put', 'post']

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if (self.action == 'list' and self.request.user.is_anonymous) or (
                self.action == 'create' and self.request.user.is_anonymous):
            serializer_class = UserRegistration

        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = SerializerWithoutEmailField

        return serializer_class

    def list(self, request, *args, **kwargs):
        context = {'request': request}
        queryset = self.model.objects.filter(id=request.user.pk)

        if (self.action == 'list' and self.request.user.is_anonymous) or (
                self.action == 'create' and self.request.user.is_anonymous):
            serializer = UserRegistration(queryset, many=True, context=context)

        else:
            serializer = ThinUserSerializer(queryset, many=True, context=context)

        return Response(serializer.data)

    def _allowed_methods(self):
        """Запрещаем Get в список"""
        # Для анонимов только регистрация
        if self.request.user.is_anonymous:
            return [m for m in super(UserViewsSet, self)._allowed_methods() if m not in ['GET']]

        # Для авторизованных только просмотр и правка
        # if self.request.user.is_authenticated:
        else:
            return [m for m in super(UserViewsSet, self)._allowed_methods() if m not in ['POST']]

    def get_permissions(self):
        if (self.action == 'list' and self.request.user.is_anonymous) or (
                self.action == 'create' and self.request.user.is_anonymous):
            self.permission_classes = [BasePermission, ]

        else:
            self.permission_classes = [IsAuthUser, ]

        return super(UserViewsSet, self).get_permissions()


# Notes
@method_decorator(
    name='list', decorator=swagger_auto_schema(
        operation_summary="Список активных заметок",
        operation_description="Не требуется дополнительных параметров, в ответ вернется список заметок.",
        # operation_id="Method ID",
        responses={200: NoteSerializer()}
    )
)
@method_decorator(
    name='update', decorator=swagger_auto_schema(
        operation_summary='Изменить заметку: заголовок, текст, удалить в корзину, добавить в избранное, дата и время',
        operation_description="{title} - заголовок"
                              "\n{text} - текст заметки"
                              "\n{is_active} - не удалена (true), удалена (false)"
                              "\n{is_favorites} - в избранном (true), не в избранном (false)"
                              "\n{created} - дата и время создания: YYYY-MM-DDThh:mm:ss (2005-08-09T18:31:42)",
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='id заметки (числовой тип)'),
        ],
        responses={200: NoteSerializer()}
    )
)
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(
        operation_summary="Получить детальную информацию о заметке",
        operation_description="Получить детальную информацию заметки по id. "
                              'Что бы узнать id нужной заметки, можно воспользоваться методом "notes_list"',
        # operation_id="Method ID",
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='id заметки (числовой тип)')
        ],
        responses={200: NoteSerializer()}
    )
)
@method_decorator(
    name='create', decorator=swagger_auto_schema(
        operation_summary='Создать новую заметку',
        operation_description="{title} - заголовок"
                              "\n{text} - текст заметки"
                              "\n{created} - дата и время создания: YYYY-MM-DDThh:mm:ss (2005-08-09T18:31:42)",
        responses={201: ThinNoteSerializer()}
    )
)
class NoteViewSet(ModelViewSet):
    """Активные заметки пользователя"""
    model = Note
    queryset = model.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthor,)
    http_method_names = ['get', 'put', 'post']

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user.pk, is_active=True)

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'POST':
            serializer_class = NoteCreateSerializer

        return serializer_class

    def list(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = ThinNoteSerializer(self.get_queryset(), many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """При добавлении записи получаем автора из реквеста"""
        serializer.save(author=self.request.user)


# Favorites
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(
        operation_summary='Получить детальную информацию о заметке в "Избранном"',
        operation_description='Получить детальную информацию заметки по id.'
                              'Что бы узнать id нужной заметки, можно воспользоваться методом "favorites_list".',
        # operation_id="Method ID",
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='id заметки (числовой тип)')
        ],
        responses={200: NoteSerializer()}
    )
)
@method_decorator(
    name='update', decorator=swagger_auto_schema(
        operation_summary='Удалить из "Избранного"',
        operation_description='Для удаления заметки из "Избранного" - для {is_favorites} установите значение false.',
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='id заметки (числовой тип)'),
        ],
        responses={200: NoteSerializer()}
    )
)
@method_decorator(
    name='list', decorator=swagger_auto_schema(
        operation_summary='Список заметок в "Избранном"',
        operation_description="Не требуется дополнительных параметров.",
        # operation_id="Method ID",
        responses={200: NoteSerializer()}
    )
)
class NoteFavoritesViewSet(ModelViewSet):
    """Избранное"""
    model = Note
    queryset = model.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthor,)
    http_method_names = ['get', 'put']

    def _allowed_methods(self):
        """Запрещаем POST в список"""
        return [m for m in super(NoteFavoritesViewSet, self)._allowed_methods() if m not in ['POST']]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user.pk, is_active=True, is_favorites=True)

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = SerializerOnlyIsFavoritesField

        return serializer_class

    def list(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = ThinFavoritesSerializer(self.get_queryset(), many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """При добавлении записи получаем автора из реквеста"""
        serializer.save(author=self.request.user)


# Basket
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(
        operation_summary='Получить детальную информацию о заметке в "Корзине"',
        operation_description='Получить детальную информацию заметки по id. '
                              'Что бы узнать id нужной заметки, можно воспользоваться методом "basket_list".',
        # operation_id="Method ID",
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='id заметки (числовой тип)')
        ],
        responses={200: BasketSerializer()}
    )
)
@method_decorator(
    name='list', decorator=swagger_auto_schema(
        operation_summary='Список удаленных заметок (в корзине)',
        operation_description="Не требуется дополнительных параметров.",
        # operation_id="Method ID",
        responses={200: ThinBasketSerializer()}
    )
)
@method_decorator(
    name='update', decorator=swagger_auto_schema(
        operation_summary='Восстановить заметку из корзины',
        operation_description='Для восстановления заметки из "Корзины" - для {is_active} установите значение true.',
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='id заметки (числовой тип)'),
        ],
        responses={201: BasketSerializer()}
    )
)
@method_decorator(
    name='destroy', decorator=swagger_auto_schema(
        operation_summary='Удалить заметку из корзины',
        operation_description='Окончательно удаляет заметку без возможности восстановления. '
                              'Что бы узнать id нужной заметки, воспользуйтесь методом "basket_list"',
        manual_parameters=[
            openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER,
                              description='id заметки (числовой тип)'),
        ],
        responses={204: "Object deleted successfully"}
    )
)
class NoteBasketViewSet(ModelViewSet):
    """Корзина"""
    model = Note
    queryset = model.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthor,)
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        notes = self.queryset.filter(author=self.request.user.pk, is_active=False)
        return notes

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = SerializerOnlyIsActiveField

        return serializer_class

    def list(self, request, *args, **kwags):
        context = {'request': request}
        serializer = ThinBasketSerializer(self.get_queryset(), many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """При добавлении записи получаем автора из реквеста"""
        serializer.save(author=self.request.user)
