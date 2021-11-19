from django.db.models import Model, CharField, TextField, DateTimeField, ForeignKey, SET_NULL, BooleanField

from accounts.models import User


class Note(Model):
    author = ForeignKey(User, null=True, blank=False, on_delete=SET_NULL)
    title = CharField(verbose_name='Заголовок', max_length=128)
    text = TextField(verbose_name='Краткое содержание', blank=True)
    full_text = TextField(verbose_name='Полное содержание', blank=True)
    created = DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    update = DateTimeField(verbose_name='Дата обновления', auto_now=True)
    is_favorites = BooleanField(db_index=True, verbose_name='В избранном', default=False)
    is_active = BooleanField(db_index=True, verbose_name='Активный', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = "Заметки"
        ordering = ['-update']

