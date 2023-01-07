from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('chat/', views.index,name="index"),
    path('chat/<str:room_name>/', views.room,name="room"),

    path('create_chat_user/', views.create_chat_user,name="create_chat_user"),
    path('delete_chat_user/<int:pk>/', views.create_chat_user,name="create_chat_user"),

    path('create_chat_room/', views.create_chat_room,name="create_chat_room"),
    path('delete_chat_room/<int:pk>/', views.delete_chat_room,name="delete_chat_room"),

    path('get_users_chat_rooms/<int:pk>/', views.get_users_chat_rooms,name="get_users_chat_rooms"),
    path('get_users_chat_msg/<int:pk>/', views.get_users_chat_msg,name="get_users_chat_msg"),

]
