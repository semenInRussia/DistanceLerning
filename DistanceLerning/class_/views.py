from django.contrib.auth import get_user
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from main.models import School
# Create your views here.
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .models import ClassModel, MessageModel
from .permissions import IsOwnerClass
from .serializers import ClassListSerializer, MessageClassSerializer
from auth_app.permissions import IsActiveUser

from auth_app.serializers import UserAllSerializer
from main.models import BindStudentClassModel


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


class SendMessageToClass(ListCreateAPIView):
    serializer_class = MessageClassSerializer
    permission_classes = [IsOwnerClass, IsActiveUser]

    def get_queryset(self):
        return MessageModel.objects.all().filter(klass=self.get_object_school())

    def get_object_school(self):
        obj = get_object_or_404(ClassModel, school_id=self.kwargs['pk'], pk=self.kwargs['pk_class'])
        self.check_object_permissions(obj=obj, request=self.request)
        return obj

    def create(self, request, *args, **kwargs):
        if not request.data._mutable:
            request.data._mutable = True

        request.data['owner'] = request.user.id
        request.data['klass'] = self.get_object_school().id

        return super().create(request, *args, **kwargs)


class ClassTeam(ListAPIView):
    serializer_class = UserAllSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]

    def get_queryset(self):
        # get queryset on user=request.user
        bind_qs = BindStudentClassModel.objects.all().filter(user=self.request.user)

        # get user
        return bind_qs.views('user')
