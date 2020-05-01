from django.db import models
from django.contrib.auth import get_user_model
from main.models import School

User = get_user_model()

class Invite(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель', related_name="+")
    by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Получатель', related_name="+")
    created = models.DateTimeField(auto_now_add=True)

    @property
    def get_school_number(self) -> int:
        if School.objects.filter(owner=self.by):
            # User has school
            return School.objects.get(owner=self.by).number

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

    class Meta:
        ordering = ['-created']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f"answer: {self.invite}"
