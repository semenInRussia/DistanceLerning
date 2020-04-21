from django.urls import path

from . import views

urlpatterns = [
    path('subject/', views.SubjectApi.as_view(), name='subject'),
    path('subject/<int:pk>', views.SubjectDetail.as_view(), name='subject_detail'),
]