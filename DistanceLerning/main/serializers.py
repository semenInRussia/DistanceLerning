from rest_framework import serializers
from .models import School, BindSchoolTeacherModel
from invites.models import Invite

from auth_app.models import Assessment


class SchoolListSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = School
        fields = ("number", "owner_name", "id")


class SchoolCreateSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = School
        fields = ("number", "owner", "owner_name")


class BindTeacherUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['user', 'school', 'created']
        model = BindSchoolTeacherModel

    # def create(self, validated_data):
    #     from invites.models import Answer
    #
    #     invites = Invite.objects.all().filter(to_id=validated_data['user'])
    #     # assert bool(Answer.objects.filter(school_id=validated_data['school'], renouncement=True, invite_id__in=invites))
    #     return super(self).create(validated_data)

class AssessmentSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='diary.student.user.username')

    class Meta:
        model = Assessment
        fields = ['value', 'diary', 'student', 'student_name']
