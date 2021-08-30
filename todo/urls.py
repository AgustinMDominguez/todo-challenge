from django.urls import path

from . import views

urlpatterns = [
    path('up', views.checkOnline, name="app is online"),
    path('login', views.login, name="login"),
    path('logged_in', views.is_logged_in, name="user is logged in"),
]