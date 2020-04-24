from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Invite
from .serializers import InviteCreateSerializer, InviteListSerializer

User = get_user_model()


class InviteSend(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """
        POST
        :type request: HttpRequest
        """

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
