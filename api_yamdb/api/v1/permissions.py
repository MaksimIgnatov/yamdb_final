from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Проверка прав администратора."""

    message = 'Изменять контент может только администратор!'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Кастомный пермишн, позволящий редактировать и удалять обьект.

    только его автору, модератору или администратору.
    """

    message = 'Пользователь не является автором поста'

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'DELETE'):
            if request.user.is_authenticated:
                return (request.user.is_admin
                        or request.user.is_moderator
                        or obj.author == request.user)
        return True


class IsAdmin(permissions.BasePermission):
    """Проверка прав администратора."""

    message = 'Вы должны быть админом чтобы получить доступ.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
