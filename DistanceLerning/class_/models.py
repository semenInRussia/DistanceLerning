# Create your models here.

from django.contrib.auth import get_user_model
from django.db import models

from main.models import School

User = get_user_model()


class ClassModel(models.Model):
    number_class = models.IntegerField("number")
    char_class = models.CharField("char", max_length=2)
    school = models.ForeignKey(School, verbose_name="school", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name="owner", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.number_class}{self.char_class}  {self.school}"