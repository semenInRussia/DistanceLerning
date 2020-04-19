# Generated by Django 3.0.5 on 2020-04-15 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directer',
            name='subject',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auth_app.Subject', verbose_name='subject'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subject',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auth_app.Subject', verbose_name='subject'),
        ),
    ]