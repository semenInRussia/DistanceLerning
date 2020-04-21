from django.contrib.auth import get_user_model
from django.db import models
from main.models import School

# Create your models here.

User = get_user_model()


class Customer:
    def isDirecter(self, school: School):
        return False

    role: str = None

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="user")

    def __str__(self):
        return f"{self.user.username} {self.role}"


class Subject(models.Model):
    name = models.CharField("name", max_length=170)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Урок", default=0)
user_field = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", default=0)


class Teacher(models.Model, Customer):
    role: str = "teacher"
    subject = subject
    user = user_field

    def __str__(self):
        return f"{self.role} {self.subject} {self.user}"

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"


class Student(models.Model, Customer):
    role: str = "student"
    user = user_field

    def __str__(self):
        return f"{self.role} {self.user}"

    def isDirecter(self, school: School):
        return False

    class Meta:
        verbose_name = "Школьник"
        verbose_name_plural = "Школьники"


class Directer(models.Model, Customer):
    role: str = 'directer'
    subject = subject
    user = user_field

    def __str__(self):
        return f"{self.role} {self.subject} {self.user}"

    class Meta:
        verbose_name = "Директор"
        verbose_name_plural = "Директора"

    def isDirecter(self, school: School):
        return school.owner.id == self.id


class Assessment(models.Model):
    value = models.IntegerField("Оценка")
    diary = models.ForeignKey('Diary', on_delete=models.CASCADE, verbose_name="Дневник")

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        return f"{self.value} {self.diary}"

    @classmethod
    def create(cls, value: int, diary):
        return cls(value=value, diary=diary).save()


class Diary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Школьник")

    class Meta:
        verbose_name = "Дневник"
        verbose_name_plural = "Дневники"

    def __str__(self):
        return f"Дневник {self.student}"

    @classmethod
    def create(cls, student: models.Model):
        diary = cls()
        diary.student = student
        diary.save()
        return diary
