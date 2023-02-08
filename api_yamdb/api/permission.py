from rest_framework import permissions


class AdminAnonPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated is False:
            return request.method in permissions.SAFE_METHODS
        return (
            (request.user.role == 'admin')
            or request.user.is_staff
        )


class AdminOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.user.role == 'admin')
            or request.user.is_staff
        )


class AuthorModeratorAdminPermission(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated is False:
            return request.method in permissions.SAFE_METHODS
        return (
            request.user.role in ('moderator', 'admin',)
            or request.user.is_staff
            or request.user == obj.author
        )
