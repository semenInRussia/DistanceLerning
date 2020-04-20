from django.urls import path

from . import views

urlpatterns = [
    # todo logout
    path('login/', views.LoginView.as_view(), name="login"),
    path('', views.AuthenticationApi.as_view(), name="RegistrationApi"),
    path('<int:pk>', views.UserDetailApi.as_view(), name='UserDetail'),
]