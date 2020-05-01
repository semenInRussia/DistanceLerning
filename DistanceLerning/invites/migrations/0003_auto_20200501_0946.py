# Generated by Django 3.0.5 on 2020-05-01 06:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invites', '0002_answer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-created'], 'verbose_name': 'Ответ', 'verbose_name_plural': 'Ответы'},
        ),
        migrations.AlterModelOptions(
            name='invite',
            options={'ordering': ['-created'], 'verbose_name': 'Приглашение', 'verbose_name_plural': 'Приглашения'},
        ),
        migrations.AddField(
            model_name='answer',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invite',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='renouncement',
            field=models.BooleanField(default=False, verbose_name='Согласен'),
        ),
    ]
