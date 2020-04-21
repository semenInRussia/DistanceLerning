from django.contrib.auth import get_user_model, authenticate
from django.db import IntegrityError
from rest_framework import serializers

# Creating your serializers here.
from .models import Student, Directer, Teacher, Subject, Diary

# Get user model
User = get_user_model()


# Create your serializers...

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=255)
#     password = serializers.CharField(max_length=255)
#


class RegistrationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=10)
    subject = serializers.IntegerField(default=1)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role', 'subject']

    def create(self, validated_data):
        # todo check email
        try:
            # Create user
            user = User.objects.create_user(
                validated_data['username'],
                validated_data['email'],
                validated_data['password']
            )
        except IntegrityError:
            # If user is be
            # Get user...
            user = authenticate(
                username=validated_data['username'],
                password=validated_data['password']
            )

        role = validated_data['role']

        # All types customers...
        models_role = {
            'student': Student,
            'directer': Directer,
            'teacher': Teacher
        }

        # Choose customer type...
        customer_model = None
        if role in models_role:
            customer_model = models_role[role]

        customer = customer_model(user=user)

        if role == 'teacher' or role == 'directer':
            customer.subject = Subject.objects.get(id=validated_data.get('subject'))
            customer.save()
        elif role == 'student':
            customer.save()
            Diary.create(student=customer)

        return user


class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id', 'is_staff']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
