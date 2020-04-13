from django.urls import path, include
from .views import *

urlpatterns = [
    path("school/", SchoolApi.as_view(), name="SchoolAll"),
    path("school/<int:pk>/", SchoolDetailApi.as_view(), name="SchoolDetail"),
    path("school/<int:pk>/", include('class_.urls')),
]