from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from notes.models import Note
from api.serializers import NoteSerializer, ThinNoteSerializer, UserSerializer, ThinUserSerializer
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
    model = Note
    queryset = model.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthor,)
    # http_method_names = ['get', 'put', 'post']  # если необходимо использовать определенные методы

    def list(self, request, *args, **kwags):
        notes = Note.objects.filter(author=request.user.pk)  # только свои заметки
        context = {'request': request}
        serializer = ThinNoteSerializer(notes, many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """При добавлении записи получаем автора из реквеста"""
        serializer.save(author=self.request.user)
