from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upcoming", views.get_upcoming_movies, name="upcoming"),
    path("gener", views.get_gener_based, name="gener"),
    path("login/", views.login, name="login"),
    path('signup/', views.signup, name='signup'),
    
]

