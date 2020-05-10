from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    message = 'You are not activated'

    def has_permission(self, request, view):
        return request.user.is_active or (request.method in permissions.SAFE_METHODS)


class IsCustomerUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsLoginUser(BasePermission):
    message = 'You are not this user'

    def has_object_permission(self, request, view, obj):
        return (request.user == obj) or (request.method in permissions.SAFE_METHODS)
