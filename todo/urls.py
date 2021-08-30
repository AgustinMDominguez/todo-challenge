from django.urls import path

from . import views

urlpatterns = [
    path('up', views.check_if_online, name="app is online"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logged_in', views.check_token, name="request token is valid"),
    path('create-profile', views.create_profile, name="create profile"),
    path('add-task', views.add_task, name="add task"),
    path('search-tasks', views.search_tasks, name="search tasks"),
    path('task/<int:task_id>/done', views.done, name="task done"),
    path('task/<int:task_id>/update', views.update_task, name="update task"),
    path('task/<int:task_id>/delete', views.delete_task, name="delete task"),
    path(
        'task/<int:task_id>/children',
        views.task_children,
        name="task children"
    ),
]
