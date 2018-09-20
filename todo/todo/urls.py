from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tasks import views as tasks_views
from .views import Home, register
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Home
    path('', Home.as_view(), name='home'),

    # Authentication and registration
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),

    # Task management
    path('tasks/',
        login_required(tasks_views.TaskListView.as_view(), login_url='login'),
        name='tasks'),

    path('task/',
        login_required(tasks_views.NewTaskView.as_view()),
        name='task-add'),

    path('task/<int:task_id>/',
        login_required(tasks_views.TaskView.as_view()),
        name='task-edit'),

    path('delete/<int:task_id>/',
        login_required(tasks_views.DeleteTaskView.as_view()),
        name='task-delete'),

    path('toggle/<int:task_id>/',
        login_required(tasks_views.toggle_complete_view),
        name='task-toggle'),

    # Django admin
    path('admin/', admin.site.urls),
]
