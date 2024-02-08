from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('addTask/', views.create_task, name='add_task'),
    path('cancel_task/<int:task_id>/', views.cancel_task, name='cancel_task'),
    path('profile/', views.ProfileData, name='profile')
]