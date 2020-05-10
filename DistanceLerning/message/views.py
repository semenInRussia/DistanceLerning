from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Message
from .serializers import MessageSerializer
from auth_app.permissions import IsActiveUser


class message(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.all().filter(
            to=self.request.user,
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        if not request.data._mutable:
            request.data._mutable = True
        request.data['from_user'] = request.user.id
        return self.create(request, *args, **kwargs)
