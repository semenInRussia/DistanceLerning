from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView

from .serializers import MessageSerializer


class message(ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return MessageSerializer.objects.all().filter(
            to=self.request.user,
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        request.data['from_user'] = request.user
        self.create(request, *args, **kwargs)
