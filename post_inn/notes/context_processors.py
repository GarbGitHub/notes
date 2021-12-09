from notes.models import Note


def counter_obj(request) -> dict:
    """
    Подсчет количества заметок текущего пользователя для вывода в меню
    :param request:
    :return: dict
    """
    context_data = {}

    if request.user.is_authenticated:
        notes = Note.objects.filter(author=request.user.pk)

        count_is_active = notes.filter(is_active=True).count()
        count_is_favorites = notes.filter(is_favorites=True).count()
        count_is_basket = notes.filter(is_active=False).count()

        context_data['count_is_active'] = count_is_active
        context_data['count_is_favorites'] = count_is_favorites
        context_data['count_is_basket'] = count_is_basket

    return context_data
