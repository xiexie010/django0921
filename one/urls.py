from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'one'
urlpatterns = [
    url('index/', views.index),
    url('login/', views.login),
    url('register/', views.register),
    url('uploadform',views.uploadform),
    url('home',views.home),
    path('getUserFromId/<int:userid>',views.getUserFromId),
    url('createUser', views.createUser),
]
