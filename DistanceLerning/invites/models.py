from django.db import models
from django.contrib.auth import get_user_model
from main.models import School

User = get_user_model()

class Invite(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель', related_name="+")
    by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Получатель', related_name="+")

    @property
    def get_school_number(self) -> int:
        if School.objects.filter(owner=self.by):
            # User has school
            return School.objects.get(owner=self.by).number

        return 0
