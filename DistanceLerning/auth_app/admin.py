from django.contrib import admin
from .models import Teacher, Student, Directer, Subject, Assessment, Diary

# Register your models here.

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Directer)
admin.site.register(Subject)
admin.site.register(Assessment)
admin.site.register(Diary)