from django.contrib.auth import get_user
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from .models import ClassModel
from .serializers import ClassListSerializer
from main.models import School


class ClassApi(APIView):
    def get_school(self, pk: int) -> School:
        return get_object_or_404(School, pk=pk)

    def get(self, request: HttpRequest, pk: int) -> Response:
        qs = ClassModel.objects.all().filter(school=self.get_school(pk))
        serializer = ClassListSerializer(qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, pk: int) -> Response:
        request.data['owner'] = get_user(request).id
        request.data['school'] = self.get_school(pk).id

        serializer = ClassListSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ClassApiDetail(APIView):
    def get_school(self, pk: int) -> School:
        return get_object_or_404(School, pk=pk)

    def get_class(self, pk_class: int, school: School) -> ClassModel:
        return get_object_or_404(ClassModel, pk=pk_class, school=school)

    def get(self, request: HttpRequest, pk: int, pk_class: int) -> Response:
        school = self.get_school(pk)
        class_ = self.get_class(school=school, pk_class=pk_class)
        serializer = ClassListSerializer(class_)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, pk: int, pk_class: int) -> Response:
        school = self.get_school(pk)
        class_ = self.get_class(school=school, pk_class=pk_class)
        class_.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: HttpRequest, pk: int, pk_class: int) -> Response:
        school = self.get_school(pk)
        class_ = self.get_class(school=school, pk_class=pk_class)
        serializer = ClassListSerializer(instance=class_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
