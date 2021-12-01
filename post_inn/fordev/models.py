from django.db import models


class PageCategory(models.Model):
    name = models.CharField(verbose_name='имя',
                            max_length=64,
                            unique=True)

    description = models.CharField(verbose_name='описание',
                                   max_length=256,
                                   blank=True,
                                   null=True)

    is_active = models.BooleanField(db_index=True, verbose_name='активна', default=True)

    created = models.DateTimeField(auto_now_add=True)

    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} id: {self.pk} -- {self.created}'

    class Meta:
        verbose_name = 'категория',
        verbose_name_plural = 'категории'


class Page(models.Model):
    category = models.ForeignKey(
        PageCategory,
        verbose_name='категория',
        on_delete=models.CASCADE)

    title = models.CharField(
        verbose_name='название',
        max_length=128
    )

    description = models.TextField(verbose_name='краткое содержание',
                                   blank=True,
                                   null=True)

    text = models.TextField(verbose_name='текст',
                            null=True)

    created = models.DateTimeField(auto_now_add=True)

    update = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(db_index=True, verbose_name='активный', default=True)
    is_boxed = models.BooleanField(db_index=True, verbose_name='закрепленный', default=False)

    def __str__(self):
        return f'{self.title} id: {self.id} -- {self.created}'

    class Meta:
        verbose_name = 'страница',
        verbose_name_plural = 'страницы'

    @staticmethod
    def get_items():
        return Page.objects.filter(is_active=True).order_by('created')
