from auth_app.models import Directer
from django.http import HttpRequest
from rest_framework.permissions import BasePermission


class IsDirecter(BasePermission):
    def has_permission(self, request, view):
        # User is directer
        return request.user.is_authenticated and bool(Directer.objects.filter(user=request.user))


class IsOwnerSchool(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and Directer.owner.id == request.user.id
