from django.urls import path

from . import views

urlpatterns = [
    path('', views.AuthenticationApi.as_view(), name="RegistrationApi")
]