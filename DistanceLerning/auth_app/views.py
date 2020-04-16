from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer, Teacher, Student, Directer
from .serializers import RegistrationSerializer


class AuthenticationApi(APIView):
    def post(self, request: HttpRequest) -> Response:
        role: str = request.data.get('role')

        customer_role = None
        if role == 'teacher':
            customer_role = Teacher
        elif role == 'student':
            customer_role = Student
        elif role == 'directer':
            customer_role = Directer

        print(role, request.data)

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            customer_role.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
