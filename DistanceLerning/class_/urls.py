from django.urls import path

from . import views

urlpatterns = [
    path('class/', views.ClassApi.as_view(), name='ClassApi'),
]