from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class AdminCriticOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.is_superuser or request.user.is_critic


class AdminCriticOrOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):
        if request.user.is_superuser:
            return True

        return request.user.is_critic and request.user == user
