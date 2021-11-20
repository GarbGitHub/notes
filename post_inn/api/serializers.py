from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from accounts.models import User
from notes.models import Note
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id', 'email', 'name', 'full_name')


class ThinUserSerializer(ModelSerializer):
    """
    Если вы используете стандартные классы маршрутизаторов, это будет строка в формате <имя_модели>-detail
    """
    url = HyperlinkedIdentityField(view_name='users-detail')

    class Meta:
        model = User
        fields = ('id', 'url')


class NoteSerializer(ModelSerializer):
    # Для связи поста к автору один к одному
    # author = SerializerMethodField(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'created', 'is_active', 'is_favorites')

    # def get_author(self, obj):
    #     # return {
    #     #     'id': f'{obj.author.id}',
    #     #     'first_name': f'{obj.author.name}',
    #     #     'last_name': f'{obj.author.full_name}',
    #     #     'email': f'{obj.author.email}',
    #     # }
    #     return str(obj.author.id)  # obj.author.id, obj.author.name, obj.author.email


class ThinNoteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='notes-detail')

    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'created', 'is_active', 'is_favorites', 'url')


# Basket
class BasketSerializer(NoteSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'created', 'update', 'is_active', 'is_favorites')


class ThinBasketSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='basket-detail')

    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'created', 'update', 'is_active', 'is_favorites', 'url')
