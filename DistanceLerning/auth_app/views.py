from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404


# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Teacher, Student, Directer
from .serializers import RegistrationSerializer, UserAllSerializer, UserUpdateSerializer

User = get_user_model()

class AuthenticationApi(APIView):
    def post(self, request: HttpRequest) -> Response:
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: HttpRequest) -> Response:
        qs = User.objects.all()
        serializer = UserAllSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailApi(APIView):
    def get_object(self, pk: int):
        user = get_object_or_404(User, pk=pk)
        return user

    def get(self, request: HttpRequest, pk: int) -> Response:
        serializer = UserAllSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: HttpRequest, pk: int) -> Response:
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request: HttpRequest, pk: int) -> Response:
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
