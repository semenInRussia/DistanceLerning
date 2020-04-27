from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(),name='logout'),
    path('', views.AuthenticationApi.as_view(), name="RegistrationApi"),
    path('<int:pk>', views.UserDetailApi.as_view(), name='UserDetail'),
]
