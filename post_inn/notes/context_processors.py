from notes.models import Note, Tag
import operator


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


def get_tags_list(request):
    context_data = {'user_tags': []}
    if request.user.is_authenticated:
        tags = Tag.objects.values_list('id', 'title').filter(author=request.user.pk, is_active=True)
        for el in tags:
            count = Note.get_count_post_in_tag(user_pk=request.user.pk, tag_pk=el[0])
            context_data['user_tags'].append({'tag_id': f'{el[0]}', 'tag_name': f'{el[1]}', 'tag_count': count})

        sort_list = sorted(context_data['user_tags'], key=operator.itemgetter('tag_count'))
        context_data = {'user_tags': sort_list}
    return context_data
