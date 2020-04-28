from rest_framework import serializers

from .models import Invite


class InviteCreateSerializer(serializers.ModelSerializer):
    to_username = serializers.ReadOnlyField(source='to.username')
    by_username = serializers.ReadOnlyField(source='by.username')

    class Meta:
        fields = ['to', 'by', 'by_username', 'to_username']
        model = Invite


class InviteListSerializer(serializers.ModelSerializer):
    to_username = serializers.ReadOnlyField(source='to.username')
    by_username = serializers.ReadOnlyField(source='by.username')
    school_number = serializers.ReadOnlyField(source='get_school_number')

    class Meta:
        model = Invite
        fields = ['to', 'by', 'to_username', 'by_username', 'school_number']
