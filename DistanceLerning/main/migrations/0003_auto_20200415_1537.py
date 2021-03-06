# Generated by Django 3.0.5 on 2020-04-15 12:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20200409_2001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='school',
            options={'verbose_name': 'Школа', 'verbose_name_plural': 'Школы'},
        ),
        migrations.AlterField(
            model_name='school',
            name='number',
            field=models.IntegerField(unique=True, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='school',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Директор'),
        ),
    ]
