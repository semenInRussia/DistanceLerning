from rest_framework import serializers
from .models import School


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
