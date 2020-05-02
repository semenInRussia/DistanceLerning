from auth_app.models import Directer
from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.permissions import BasePermission

from .models import BindSchoolTeacherModel


class IsDirecter(BasePermission):
    def has_permission(self, request: HttpRequest, view):
        # User is directer
        return request.user.is_authenticated and \
               bool(Directer.objects.filter(user=request.user))


class IsOwnerSchool(BasePermission):
    message = "You isn't owner school"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class UserIsInSchool(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            BindSchoolTeacherModel.objects.all().filter(school=obj, user=request.user)
        )
