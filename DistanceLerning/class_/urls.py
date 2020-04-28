from django.urls import path

from . import views

urlpatterns = [
    path('class/', views.ClassApi.as_view(), name='class'),
    path('class/<int:pk_class>', views.ClassApiDetail.as_view(), name='class_detail'),
    path('class/<int:pk_class>/send/', views.SendMessageToClass.as_view(), name='class_detail_send_message'),
]