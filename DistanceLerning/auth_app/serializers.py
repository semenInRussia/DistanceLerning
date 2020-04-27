from typing import NamedTuple

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.db import IntegrityError
from django.template.loader import render_to_string
from rest_framework import serializers

from .models import Student, Directer, Teacher, Subject, Diary

# Creating your serializers here.

# Get user model
User = get_user_model()

# Email
class BaseSendData(NamedTuple):
    template_name: str = '_email/activation.html'
    context: dict = {}
    subject_title: str = ''
    subject: str = f'[DistanceLerning] {subject_title}'
    to_email: str = ''
    from_email: str = settings.DEFAULT_FROM_EMAIL


def base_send_email(data: BaseSendData):
    html = render_to_string(data.template_name, context=data.context)
    send_mail(subject=data.subject,
              message=None,
              from_email=data.from_email,
              recipient_list=[data.to_email]
              )


# Customers
def create_customer(user: User, role: str, subject: int = 0):
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
        customer.subject = Subject.objects.get(id=subject)
        customer.save()
    elif role == 'student':
        customer.save()
        Diary.create(student=customer)

    return customer


# auth
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegistrationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=10)
    subject = serializers.IntegerField(default=1)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role', 'subject']

    def create(self, validated_data):
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

        # Send email
        data = BaseSendData(context={
            "user": user,
        }, subject_title="Активация пользователя",
            to_email=user.email)

        base_send_email(data)

        role = validated_data['role']

        create_customer(role=role,
                        subject=validated_data['subject'],
                        user=user)
        user.is_active = False
        return user


class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id', 'is_staff']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
