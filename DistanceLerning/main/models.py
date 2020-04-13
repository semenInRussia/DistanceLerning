from django.db import models
from django.contrib.auth import get_user_model, get_user
# Create your models here.
User = get_user_model()

class School(models.Model):
    number = models.IntegerField("Number", unique=True)
    owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.number}"
