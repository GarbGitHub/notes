from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        """
        Получить доступ к чтению списка или детальной записи (GET),
        и доступ к добавлению нового объекта (POST)
        :param request:
        :param view:
        :return: Вернуть True, если разрешение предоставлено, в противном случае - False.
        """
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Получить доступ к редактированию и удалению (PUT, DEL)
        :param self:
        :param request:
        :param view:
        :param obj:
        :return: Вернуть True, если разрешение предоставлено, в противном случае - False.
        """
        # Если это метод Get и пользователь прошел аутентификацию
        if request.method in SAFE_METHODS and request.user.pk == obj.author.pk:  # список методов: ('GET', 'HEAD', 'OPTIONS')
            return True

        # Если необходимы действия над объектом, проверяем пользователя: является он ли автором объекта
        return obj.author == request.user


class IsAuthUser(BasePermission):

    def has_permission(self, request, view):
        """
        Получить доступ к чтению списка или детальной записи (GET),
        и доступ к добавлению нового объекта (POST)
        :param request:
        :param view:
        :return: Вернуть True, если разрешение предоставлено, в противном случае - False.
        """
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Получить доступ к редактированию и удалению (PUT, DEL)
        :param self:
        :param request:
        :param view:
        :param obj:
        :return: Вернуть True, если разрешение предоставлено, в противном случае - False.
        """
        # Если это метод Get и пользователь прошел аутентификацию
        if request.method in SAFE_METHODS and request.user.pk == obj.pk:  # список методов: ('GET', 'HEAD', 'OPTIONS')
            return True

        # Если необходимы действия над объектом, проверяем пользователя: является он ли автором объекта
        return obj.pk == request.user.pk



