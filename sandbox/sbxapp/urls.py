from django.urls import path

from . import views

app_name = 'sbxapp'  # application namespace

urlpatterns = [
    path('home/', views.home),
    path('', views.dt_all2),
]
