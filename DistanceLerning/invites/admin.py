from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'invite', 'renouncement', 'created']


@admin.register(models.Invite)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['to', 'by', 'created']
