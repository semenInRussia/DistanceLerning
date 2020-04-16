from django.db import models
from django.contrib.auth import get_user_model, get_user

# Create your models here.
User = get_user_model()


class School(models.Model):
    number = models.IntegerField("Номер", unique=True)
    owner = models.ForeignKey(User, verbose_name="Директор", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Школа"
        verbose_name_plural = "Школы"

    def __str__(self):
        return f"{self.number}"
