# Create your permissions here...
import time

from django.http import HttpRequest
from django.utils import timezone
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerClass(BasePermission):
    message = "You isn't owner class"

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
