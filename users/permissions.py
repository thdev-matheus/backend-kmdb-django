from rest_framework import permissions
from rest_framework.views import Request, View

from users.models import User


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User) -> bool:
        return request.user == user or request.user.is_superuser
