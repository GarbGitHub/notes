from notes.models import Note


def counter_obj(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(author=request.user.pk)

        if len(notes) > 0:
            count_is_active = notes.filter(is_active=True).count()
            count_is_favorites = notes.filter(is_favorites=True).count()
            count_is_basket = notes.filter(is_active=False).count()
            return {
                'count_is_active': count_is_active,
                'count_is_favorites': count_is_favorites,
                'count_is_basket': count_is_basket
            }
        else:
            return {}
    else:
        return {}
