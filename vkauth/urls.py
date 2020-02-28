from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('vkcode/', views.vkcode, name='vkcode')
]