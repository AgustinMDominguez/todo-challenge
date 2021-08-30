from django.urls import path

from . import views

urlpatterns = [
    path('up', views.check_if_online, name="app is online"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('create-profile', views.create_profile, name="create profile"),
    path('logged_in', views.is_logged_in, name="user is logged in"),
]
