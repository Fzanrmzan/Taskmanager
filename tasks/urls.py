from django.urls import path
from .views import dashboard, update_task_status
from .views import (
    TaskListCreateView, TaskDetailView, 
    register, user_login, user_logout, 
    dashboard, update_task, delete_task,
)

urlpatterns = [
    # API Routes
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # Auth Routes
    path('accounts/login/', user_login, name='login'),
    path('accounts/register/', register, name='register'),
    path('accounts/logout/', user_logout, name='logout'),

    # Dashboard & Task Management
    path('dashboard/', dashboard, name='dashboard'),
    path('update_task_status/<int:task_id>/', update_task_status, name='update_task_status'),

    path('update_task/<int:task_id>/', update_task, name='update_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('update_task_status/<int:task_id>/', update_task_status, name='update_task_status'),
]
