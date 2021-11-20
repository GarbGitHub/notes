from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from notes.models import Note
from api.serializers import NoteSerializer, ThinNoteSerializer, UserSerializer, ThinUserSerializer, \
    ThinBasketSerializer, BasketSerializer
from .permission import IsAuthor, IsAuthUser


class UserViewsSet(ModelViewSet):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthUser,)

    def _allowed_methods(self):
        """Запрещаем POST в список"""
        return [m for m in super(UserViewsSet, self)._allowed_methods() if m not in ['POST']]

    def list(self, request, *args, **kwargs):
        context = {'request': request}
        queryset = self.model.objects.filter(id=request.user.pk)
        serializer = ThinUserSerializer(queryset, many=True, context=context)
        return Response(serializer.data)


class NoteViewSet(ModelViewSet):
    """
    Все заметки пользователя: активные и удаленные (в корзине)
    """
    # http_method_names = ['get', 'put', 'post']  # если необходимо использовать определенные методы

    model = Note
    queryset = model.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(author=self.request.user.pk, is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = ThinNoteSerializer(self.get_queryset(), many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """При добавлении записи получаем автора из реквеста"""
        serializer.save(author=self.request.user)


# class NoteActiveViewSet(ModelViewSet):
#     """Все активные заметки пользователя"""
#     model = Note
#     queryset = model.objects.all()
#     serializer_class = NoteSerializer
#     permission_classes = (IsAuthor,)
#
#     def get_queryset(self):
#         queryset = self.queryset
#         query_set = queryset.filter(author=self.request.user.pk, is_active=True)
#         return query_set
#
#     def list(self, request, *args, **kwargs):
#         context = {'request': request}
#         serializer = ThinActiveNoteSerializer(self.get_queryset(), many=True, context=context)
#         return Response(serializer.data)
#
#     def perform_create(self, serializer):
#         """При добавлении записи получаем автора из реквеста"""
#         serializer.save(author=self.request.user)


class NoteBasketViewSet(NoteViewSet):
    """Корзина пользователя"""
    serializer_class = BasketSerializer
    # http_method_names = ['get', 'put', 'post']  # если необходимо использовать определенные методы

    def _allowed_methods(self):
        """Запрещаем POST в список"""
        return [m for m in super(NoteBasketViewSet, self)._allowed_methods() if m not in ['POST']]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(author=self.request.user.pk, is_active=False)
        return query_set

    def list(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = ThinBasketSerializer(self.get_queryset(), many=True, context=context)
        return Response(serializer.data)

    # def perform_create(self, serializer):
    #     """При добавлении записи получаем автора из реквеста"""
    #     serializer.save(author=self.request.user)
