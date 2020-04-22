# Create your models here.

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from main.models import School

User = get_user_model()


class ClassModel(models.Model):
    number_class = models.IntegerField("Цифра")
    char_class = models.CharField("Буква", max_length=2)
    school = models.ForeignKey(School, verbose_name="Школа", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name="Создатель", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def get_absolute_url(self):
        return reverse("class_detail", kwargs={
            "pk": self.school.pk,
            "pk_class": self.pk,
        })

    def __str__(self):
        return f"{self.number_class}{self.char_class}  {self.school}"
