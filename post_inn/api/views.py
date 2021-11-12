from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from notes.models import Note
from api.serializers import NoteSerializer, ThinNoteSerializer, UserSerializer
from rest_framework.permissions import IsAdminUser
from .permission import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model


# viewsets
class UserViewsSet(ModelViewSet):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class NoteViewSet(ModelViewSet):
    model = Note
    queryset = model.objects.filter()
    serializer_class = NoteSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)  # Если не авторизован, только читать
    permission_classes = (IsAuthorOrReadOnly,)  # Если не автор, то только читать

    # http_method_names = ['get', 'put', 'post']  # если необходимо использовать определенные методы

    def list(self, request, *args, **kwags):
        # notes = Note.objects.all()  # все заметки
        notes = Note.objects.filter(author=request.user.pk)  # только свои заметки
        context = {'request': request}
        serializer = ThinNoteSerializer(notes, many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """При добавлении записи получаем автора из реквеста"""
        serializer.save(author=self.request.user)
