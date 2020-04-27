from auth_app.models import Directer
from rest_framework.permissions import BasePermission


class IsDirecter(BasePermission):
    def has_permission(self, request, view):
        # User is directer
        return request.user.is_authenticated and bool(request.user.customer)


class IsOwnerSchool(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and Directer.owner.id == request.user.id
