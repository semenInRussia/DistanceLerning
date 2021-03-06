from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import School, BindStudentClassModel, BindSchoolTeacherModel
# Create your views here.
from .permissions import IsDirecter, IsOwnerSchool, UserIsInSchool
from .serializers import SchoolListSerializer, SchoolCreateSerializer, BindTeacherUserSerializer, AssessmentSerializer, \
    BindStudentClassSerializer

# School CRUD
from auth_app.serializers import UserAllSerializer

from auth_app.permissions import IsActiveUser

from class_.permissions import IsOwnerClass

from auth_app.models import Assessment

from auth_app.models import Diary

from class_.models import ClassModel

User = get_user_model()

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
    permission_classes = [IsOwnerSchool, IsActiveUser]

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
    permission_classes = [IsActiveUser, IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.data._mutable:
            request.data._mutable = True

        if request.data.get('school_number'):
            request.data['school'] = get_object_or_404(School, number=request.data['school_number']).pk
        request.data['user'] = request.user.pk

        return self.create(request, *args, **kwargs)


class BindStudentClass(CreateAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = BindStudentClassSerializer

    def get_klass(self):
        request_data = self.request.data
        if self.request.GET:
            request_data = self.request.GET
        char_class = request_data.get('char_class')
        number_class = request_data.get('number_class')

        school = self.get_school()
        klass = get_object_or_404(ClassModel, char_class=char_class,
                                  number_class=number_class,
                                  school=school)

        return klass

    def get_school(self):
        request_data = self.request.data

        if self.request.GET:
            request_data = self.request.GET

        number = request_data.get('school_number')
        pk = request_data.get('school')

        if number:
            return get_object_or_404(School, number=number)
        else:
            return get_object_or_404(School, pk=pk)

    def post(self, request, *args, **kwargs):
        if not request.data._mutable:
            request.data._mutable = True

        request.data['klass'] = self.get_klass().pk

        request.data['user'] = request.user.pk

        return self.create(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        user_ids = BindStudentClassModel.objects.all().filter(
            klass=self.get_klass()
        ).values_list('user_id', flat=True)

        queryset = User.objects.all().filter(id__in=user_ids)
        serializer = UserAllSerializer(queryset, many=True)

        return Response(data=serializer.data)


class ListTeacherInSchool(APIView):
    permission_classes = [UserIsInSchool]

    def get_school(self, pk):
        obj = get_object_or_404(School, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request: HttpRequest, pk):
        qs = BindSchoolTeacherModel.objects.all().filter(school=self.get_school(pk)) \
            .values('user')
        serializer = UserAllSerializer(qs, many=True)
        return Response(data=serializer.data, status=200)


# [FAILING]
# to do create Rate view
class Rate(ListCreateAPIView):
    serializer_class = AssessmentSerializer
    permission_classes = [IsOwnerClass, IsActiveUser]

    def get_queryset(self):
        return Assessment.objects.all().filter(diary_student=self.request.user)

    def get_class(self):
        return None

    def post(self, request, *args, **kwargs):
        self.check_object_permissions(request, self.get_class())
        if not request.data._mutable:
            request.data._mutable = True

        request.data['diary'] = self.get_diary(request.data.get('student'))

        super().post(request, *args, **kwargs)

    def get_diary(self, student_id: int):
        return get_object_or_404(Diary, student_id=student_id)
