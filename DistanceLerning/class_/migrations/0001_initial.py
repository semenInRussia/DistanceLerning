# Generated by Django 3.0.5 on 2020-04-12 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20200409_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_class', models.IntegerField(verbose_name='number class')),
                ('char_class', models.CharField(max_length=2, verbose_name='char class')),
                ('main_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='main teacher')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.School', verbose_name='school')),
            ],
        ),
    ]