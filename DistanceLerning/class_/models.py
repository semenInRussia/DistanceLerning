# Create your models here.

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class ClassModel(models.Model):
    number_class = models.IntegerField("Цифра")
    char_class = models.CharField("Буква", max_length=2)
    school = models.ForeignKey("main.School", verbose_name="Школа", on_delete=models.CASCADE, related_name='+')
    owner = models.ForeignKey(User, verbose_name="Создатель", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def get_class_name(self):
        return f"{self.number_class}{self.char_class.lower()}"

    def get_absolute_url(self):
        return reverse("class_detail", kwargs={
            "pk": self.school.pk,
            "pk_class": self.pk,
        })

    def __str__(self):
        return f"{self.number_class}{self.char_class}  {self.school}"


class MessageModel(models.Model):
    text = models.TextField(verbose_name='Текст')
    klass = models.ForeignKey('ClassModel', on_delete=models.CASCADE, verbose_name='Класс')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Отправитель')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время отправки')
