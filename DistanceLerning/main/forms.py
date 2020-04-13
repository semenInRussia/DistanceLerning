from django import forms
from django.contrib.auth import get_user_model

# Write us Forms for models...
from DistanceLerning.main.models import School

User = get_user_model()


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
