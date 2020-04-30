from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()

class Message(models.Model):
    to = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='Получатель')
    from_user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='Отправитель')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Текст')
    subject = models.CharField(verbose_name='Тема', max_length=255)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f"{self.subject}"
