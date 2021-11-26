from django.db.models import BooleanField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from accounts.models import User
from notes.models import Note
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'view' in self.context and self.context['view'].action in ['create']:
            self.fields.pop('last_login', None)
            self.fields.pop('staff', None)
            self.fields.pop('is_active', None)
            self.fields.pop('admin', None)
        if 'view' in self.context and self.context['view'].action in ['list']:
            self.fields.pop('email', None)

    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = '__all__'

    def create(self, validated_data):
        return UserSerializer.objects.create(**validated_data)


class UserRegistration(ModelSerializer):

    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id', 'email', 'name', 'last_name', 'password' )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)


class SerializerWithoutEmailField(ModelSerializer):
    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id', 'name', 'last_name')


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
    author = SerializerMethodField(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'author', 'title', 'text', 'created', 'update', 'is_active', 'is_favorites')

    def get_author(self, obj):
        return {
            'id': f'{obj.author.id}',
            'first_name': f'{obj.author.name}',
            'last_name': f'{obj.author.last_name}',
            'email': f'{obj.author.email}',
        }
        # return str(obj.author.id)  # obj.author.id, obj.author.name, obj.author.email


class NoteCreateSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', 'text')


class ThinNoteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='notes-detail')

    class Meta:
        model = Note
        fields = ('id', 'author', 'title', 'text', 'created', 'update', 'is_active', 'is_favorites', 'url')


class SerializerOnlyIsFavoritesField(ModelSerializer):
    """Удалить из избранного"""

    class Meta:
        model = Note
        queryset = model.objects.all()
        fields = ('is_favorites',)


class ThinFavoritesSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='favorites-detail')

    class Meta:
        model = Note
        fields = 'id', 'author', 'title', 'text', 'created', 'update', 'is_active', 'is_favorites', 'url'


# Basket
class BasketSerializer(ModelSerializer):
    class Meta:
        model = Note
        queryset = model.objects.all()
        fields = '__all__'


class SerializerOnlyIsActiveField(ModelSerializer):
    """Восстановить заметку из корзины"""

    class Meta:
        model = Note
        queryset = model.objects.all()
        fields = ('is_active',)


class ThinBasketSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='basket-detail')

    class Meta:
        model = Note
        queryset = model.objects.all()
        fields = '__all__'


class UpdateBasketSerializer(ModelSerializer):
    class Meta:
        model = Note
        queryset = model.objects.all()
        fields = 'is_active'
