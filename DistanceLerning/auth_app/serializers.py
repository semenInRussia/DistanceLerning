from django.contrib.auth import get_user_model
from rest_framework import serializers

# Creating your serializers here.
from .models import Student, Directer, Teacher

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        role = validated_data['role']
        models_role = {
            'student': Student,
            'directer': Directer,
            'teacher': Teacher
        }

        customer_model = None
        if role in models_role:
            customer_model = models_role[role]

        customer = customer_model(user=user )
        print(validated_data.get('subject'))
        if role == 'teacher' or role == 'directer':
            customer.subject = validated_data.get('subject')

        print(user.id)
        customer.save()
