from django.urls import path, include
from . import views

urlpatterns = [
    path("school/", views.SchoolApi.as_view(), name="SchoolAll"),
    path("school/<int:pk>/", views.SchoolDetailApi.as_view(), name="SchoolDetail"),
    path("school/<int:pk>/", include('class_.urls')),
    path("message/", views.BindSchoolTeacher.as_view(), name='bind_user_teacher')
]
