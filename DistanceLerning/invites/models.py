from django.db import models
from django.contrib.auth import get_user_model
from main.models import School
from rest_framework.generics import get_object_or_404

from main.models import BindSchoolTeacherModel

from auth_app.models import Student, Teacher

User = get_user_model()


class Invite(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель', related_name="+")
    by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Получатель', related_name="+")
    created = models.DateTimeField(auto_now_add=True)

    @property
    def is_invite_to_class(self) -> bool:
        return bool(Student.objects.all().filter(user=self.by))

    @property
    def is_invite_to_school(self) -> bool:
        return bool(Teacher.objects.all().filter(user=self.by))

    @property
    def get_school_number(self) -> int:
        if self.is_invite_to_school:
            if School.objects.filter(owner=self.by):
                # User has school
                return School.objects.get(owner=self.by).number
        elif self.is_invite_to_class:
            # get bind with teacher
            qs = BindSchoolTeacherModel.objects.filter(user=self.by)
            if qs:
                bind_with_school = qs.first()
                return bind_with_school.school.number
        return 0

    class Meta:
        ordering = ['-created']
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'

    def __str__(self):
        return f'{self.by} -> {self.to}'


class Answer(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текст')
    invite = models.OneToOneField("Invite", on_delete=models.CASCADE, verbose_name='Приглашение')
    renouncement = models.BooleanField(verbose_name='Согласен', default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Отправитель')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f"answer: {self.invite}"
