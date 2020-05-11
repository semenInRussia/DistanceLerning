# Generated by Django 3.0.5 on 2020-05-11 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invites', '0004_answer_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='is_invite_to_class',
            field=models.BooleanField(default=False, verbose_name='Это приглашения в класс?'),
        ),
        migrations.AddField(
            model_name='invite',
            name='is_invite_to_school',
            field=models.BooleanField(default=False, verbose_name='Это приглашения в школу??'),
        ),
    ]
