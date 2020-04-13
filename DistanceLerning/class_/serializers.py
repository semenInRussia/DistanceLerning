from rest_framework import serializers

from .models import ClassModel


class ClassListSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = ClassModel
        fields = ("owner", "school", "char_class", "number_class", "id", "owner_name")
