from rest_framework import serializers

from .models import ClassModel, MessageModel


class ClassListSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = ClassModel
        fields = ("owner", "school", "char_class", "number_class", "id", "owner_name")

class MessageClassSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    class_name = serializers.ReadOnlyField(source='klass.get_class_name')

    class Meta:
        model = MessageModel
        fields = ['owner', "owner_name", 'klass', 'class_name', 'text']
