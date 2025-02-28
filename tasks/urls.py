from django.urls import path
from tasks.views import show_task, admin_dashboard, user_dashboard, create_task

urlpatterns = [
    path('', show_task),
    path('admin-dashboard/', admin_dashboard),
    path('user-dashboard/', user_dashboard),
    path('create-task/', create_task)
]
