from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import School
# Create your views here.
from .permissions import IsDirecter, IsOwnerSchool, UserIsInSchool
from .serializers import SchoolListSerializer, SchoolCreateSerializer, BindTeacherUserSerializer

# School CRUD
from auth_app.serializers import UserAllSerializer


class SchoolApi(APIView):
    # permissions
    permission_classes = [IsDirecter]

    # GET
    def get(self, request) -> Response:
        qs = School.objects.all()
        serializer = SchoolListSerializer(qs, many=True)
        return Response(serializer.data)

    # POST
    def post(self, request) -> Response:
        request.data['owner'] = request.user.id

        serializer = SchoolCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# School Receiver
class SchoolDetailApi(APIView):
    # Permissions
    permission_classes = [IsOwnerSchool]

    def get_object(self, pk):
        school = get_object_or_404(School, pk=pk)
        self.check_object_permissions(self.request, school)
        return school

    def get(self, request, pk) -> Response:
        serializer = SchoolListSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk) -> Response:
        school = self.get_object(pk)
        serializer = SchoolListSerializer(school, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk) -> Response:
        school = self.get_object(pk)
        school.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BindSchoolTeacher(CreateAPIView):
    serializer_class = BindTeacherUserSerializer

    def post(self, request, *args, **kwargs):
        if not request.data._mutable:
            request.data._mutable = True

        if request.data.get('school_number'):
            request.data['school'] = get_object_or_404(School, number=request.data['school_number']).pk
        request.data['user'] = request.user.pk

        return self.create(request, *args, **kwargs)


class ListTeacherInSchool(APIView):
    permission_classes = [UserIsInSchool]

    def get_school(self, pk):
        obj = get_object_or_404(School, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request: HttpRequest, pk):
        qs = BindSchoolTeacher.objects.all().filter(school=self.get_school(pk))\
            .values('user')
        serializer = UserAllSerializer(qs, many=True)
        return Response(data=serializer.data, status=200)