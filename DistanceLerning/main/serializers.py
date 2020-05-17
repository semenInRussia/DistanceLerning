from auth_app.models import Assessment
from rest_framework import serializers

from .models import School, BindSchoolTeacherModel, BindStudentClassModel


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


class BindStudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = BindStudentClassModel
        fields = ['user', 'klass', 'created']


class AssessmentSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='diary.student.user.username')

    class Meta:
        model = Assessment
        fields = ['value', 'diary', 'student', 'student_name']
