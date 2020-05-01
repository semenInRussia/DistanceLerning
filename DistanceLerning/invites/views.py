from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework.generics import get_object_or_404, ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Invite, Answer
from .serializers import InviteCreateSerializer, InviteListSerializer, InviteAnswerSerializer

User = get_user_model()


class InviteSend(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest) -> Response:
        # get by user
        to_username = request.data['username']
        user: User = get_object_or_404(User, username=to_username)

        # Init data
        data_for_save = {
            'by': request.user.id,
            'to': user.id,
        }

        # Init serializer
        serializer = InviteCreateSerializer(data=data_for_save)

        # Check
        if serializer.is_valid():
            serializer.save()
            # OK
            return Response(serializer.data, status=201)
        # Bad
        return Response(status=400)


class InviteList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InviteListSerializer

    def get_queryset(self) -> QuerySet:
        queryset = Invite.objects.all().filter(to=self.request.user)
        return queryset


class InviteAnswer(ListCreateAPIView):
    serializer_class = InviteAnswerSerializer

    def get_queryset(self):
        return Answer.objects.all().filter(
            to=self.request.user
        )
