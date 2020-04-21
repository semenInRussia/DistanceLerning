from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import School
# Create your views here.
from .permissions import IsDirecter, IsOwnerSchool
from .serializers import SchoolListSerializer, SchoolCreateSerializer


# School CRUD
class SchoolApi(APIView):
    # permissions
    permission_classes = (IsAdminUser | IsDirecter,)

    # GET
    def get(self, request) -> Response:
        qs = School.objects.all()
        serializer = SchoolListSerializer(qs, many=True)
        return Response(serializer.data)

    # POST
    def post(self, request) -> Response:
        # todo get invites to join to School

        request.data['owner'] = request.user.id

        serializer = SchoolCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# School Receiver
class SchoolDetailApi(APIView):
    # Permissions
    permission_classes = (IsOwnerSchool, IsAdminUser)

    def get_object(self, pk):
        school = get_object_or_404(School, pk=pk)
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
