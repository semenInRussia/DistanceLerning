from django.urls import path

from . import views

urlpatterns = [
    path('message/', views.message.as_view(), name='message'),
]