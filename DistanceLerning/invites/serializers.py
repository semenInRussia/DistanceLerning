from rest_framework import serializers

from .models import Invite, Answer


class InviteCreateSerializer(serializers.ModelSerializer):
    to_username = serializers.ReadOnlyField(source='to.username')
    by_username = serializers.ReadOnlyField(source='by.username')

    class Meta:
        fields = ['to', 'by', 'by_username', 'to_username', 'pk']
        model = Invite


class InviteListSerializer(serializers.ModelSerializer):
    to_username = serializers.ReadOnlyField(source='to.username')
    by_username = serializers.ReadOnlyField(source='by.username')
    school_number = serializers.ReadOnlyField(source='get_school_number')

    class Meta:
        model = Invite
        fields = ['to', 'by', 'to_username', 'by_username', 'school_number', 'created', 'pk', 'is_invite_to_class',
                  'is_invite_to_school']


class InviteAnswerSerializer(serializers.ModelSerializer):
    school_number = serializers.ReadOnlyField(source='invite.get_school_number')

    class Meta:
        model = Answer
        fields = ['text', 'renouncement', 'invite', 'school_number', 'created', 'pk', 'owner',
                  'is_invite_to_class', 'is_invite_to_school']

    def validate(self, attrs):
        values = [attrs['is_invite_to_class'], attrs['is_invite_to_school']]

        if (True not in values) and (False not in values):
            raise serializers.ValidationError('set is_invite_to_school or is_invite_to_school at true or false')
