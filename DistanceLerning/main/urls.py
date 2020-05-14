from django.urls import path, include
from . import views

urlpatterns = [
    path("diary/", views.Rate.as_view(), name='rate'),
    path("school/", views.SchoolApi.as_view(), name="SchoolAll"),
    path("school/<int:pk>/", views.SchoolDetailApi.as_view(), name="SchoolDetail"),
    path('school/<int:pk>/team/', views.ListTeacherInSchool.as_view(), name='team'),
    path("school/<int:pk>/", include('class_.urls')),
    path("bind-school/", views.BindSchoolTeacher.as_view(), name='bind_user_teacher'),
    path("bind-class/", views.BindStudentClass.as_view(), name='bind_student_class'),
]
