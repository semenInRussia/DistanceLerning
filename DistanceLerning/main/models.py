from django.db import models
from django.contrib.auth import get_user_model, get_user

# Create your models here.
from django.urls import reverse

from class_.models import ClassModel

User = get_user_model()


class School(models.Model):
    number = models.IntegerField("Номер", unique=True)
    owner = models.ForeignKey(User, verbose_name="Директор", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Школа"
        verbose_name_plural = "Школы"

    def __str__(self):
        return f"{self.number}"

    def get_absolute_url(self):
        return reverse("SchoolDetail", kwargs={
            "pk": self.pk,
        })


class BindSchoolTeacherModel(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.school} {self.user}'

    class Meta:
        verbose_name = 'Контакт школы и учителя'
        verbose_name_plural = 'Контакты школы и учителя'
        ordering = ['-created']


class BindStudentClassModel(models.Model):
    klass = models.ForeignKey(ClassModel, on_delete=models.CASCADE, verbose_name='Класс')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.klass} {self.user}'

    class Meta:
        verbose_name = 'Контакт школьника и класса'
        verbose_name_plural = 'Контакты школьника и класса'
        ordering = ['-created']
