from django.urls import path

from . import views

urlpatterns = [
    path('send/', views.InviteSend.as_view(), name='send_invite'),
    path('list/', views.InviteList.as_view(), name='list_invite'),
    path('answer/', views.InviteAnswer.as_view(), name='answer_to_invite'),
]