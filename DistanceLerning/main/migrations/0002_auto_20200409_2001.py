# Generated by Django 3.0.5 on 2020-04-09 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='number',
            field=models.IntegerField(unique=True, verbose_name='Number'),
        ),
    ]
