from django.urls import path
from tasks.views import show_task, admin_dashboard, user_dashboard, create_task, update_task

urlpatterns = [
    path('', show_task),
    path('admin-dashboard/', admin_dashboard, name="admin-dashboard"),
    path('user-dashboard/', user_dashboard, name="user-dashboard"),
    path('create-task/', create_task, name="create-task"),
    path('update-task/<int:id>', update_task, name="update-task")
]
