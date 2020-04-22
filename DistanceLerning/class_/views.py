from django.contrib.auth import get_user
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from main.models import School
# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .models import ClassModel
from .permissions import IsOwnerClass
from .serializers import ClassListSerializer


class ClassApi(APIView):
    def get_school(self, pk: int) -> School:
        return get_object_or_404(School, pk=pk)

    def get(self, request: HttpRequest, pk: int) -> Response:
        school = self.get_school(pk=pk)
        qs = ClassModel.objects.all().filter(school=school)
        serializer = ClassListSerializer(qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, pk: int) -> Response:
        request.data['owner'] = get_user(request).id
        request.data['school'] = self.get_school(pk).id

        serializer = ClassListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ClassApiDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassListSerializer
    permission_classes = [IsOwnerClass]
    queryset = ClassModel.objects.all()

    def get_school(self, pk: int):
        return get_object_or_404(School, pk=pk)

    def get_object(self):
        # Url kwargs
        pk = self.kwargs["pk"]
        pk_class = self.kwargs["pk_class"]

        # Get school
        school = self.get_school(pk)

        # get object
        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=pk_class, school=school)

        # check permissions
        self.check_object_permissions(self.request, obj)
        return obj

