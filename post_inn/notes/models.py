from datetime import datetime

from django.db.models import Model, CharField, TextField, DateTimeField, ForeignKey, BooleanField, ManyToManyField, \
    CASCADE

from accounts.models import User


class Tag(Model):
    author = ForeignKey(User, verbose_name='Автор', null=True, blank=False, on_delete=CASCADE)
    title = CharField(verbose_name='Тег', max_length=128)
    created = DateTimeField(verbose_name='Дата и время создания', default=datetime.now)
    update = DateTimeField(verbose_name='Дата обновления', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = "Теги"
        ordering = ['-created', ]

    @staticmethod
    def get_tag(user_pk):
        return Tag.objects.filter(author=user_pk)

    @staticmethod
    def get_author_tag(request, tag_pk):
        """
        Получить author_pk коллекции (папки, тега)
        :param request:
        :param tag_pk:
        :return: author_pk or Noon
        """
        return Tag.objects.values_list('author').filter(author=request.user, id=tag_pk).first()


class Note(Model):
    author = ForeignKey(User, verbose_name='Автор', null=True, blank=False, on_delete=CASCADE)
    title = CharField(verbose_name='Заголовок', max_length=128)
    text = TextField(verbose_name='Текст заметки', blank=True)
    full_text = TextField(verbose_name='Полное содержание', blank=True)
    tags = ManyToManyField(Tag, db_index=True, verbose_name='Тэг', blank=True)
    created = DateTimeField(verbose_name='Дата и время создания', default=datetime.now)
    update = DateTimeField(verbose_name='Дата обновления', auto_now=True)
    is_favorites = BooleanField(db_index=True, verbose_name='В избранном', default=False)
    is_active = BooleanField(db_index=True, verbose_name='Активный', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заметку'
        verbose_name_plural = "Заметки"
        ordering = ['-is_active', '-is_favorites', '-created', ]

    @staticmethod
    def get_count_post_in_tag(user_pk, tag_pk):
        return Note.objects.filter(is_active=True, author=user_pk, tags=tag_pk).count()
