from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView

from .models import Message
from .serializers import MessageSerializer


class message(ListCreateAPIView):
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
