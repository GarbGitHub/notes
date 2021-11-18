# from rest_framework.serializers import Serializer, IntegerField, CharField, ModelSerializer, HyperlinkedIdentityField, \
#     SerializerMethodField
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from notes.models import Note
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id', 'email', 'password', 'name', 'admin', 'staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        :param validated_data: верификация полей на основе описания модели класса
        :return:
        """
        password = validated_data.pop('password', '')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)


class NoteSerializer(ModelSerializer):
    # Для связи поста к автору один к одному
    author = SerializerMethodField(read_only=True)

    class Meta:
        model = Note
        fields = '__all__'

    def get_author(self, obj):
        return str(obj.author.id)  # obj.author.id, obj.author.name, obj.author.email


class ThinNoteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='notes-detail')

    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'url', 'created', 'is_active')

# class NoteSerializer(Serializer):
#     id = IntegerField(read_only=True)
#     title = CharField(required=True, max_length=250)
#     text = CharField(required=False, allow_blank=True)
#
#     def create(self, validated_data):
#         return Note.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.text = validated_data.get('text', instance.text)
#         instance.save()
#         return instance
