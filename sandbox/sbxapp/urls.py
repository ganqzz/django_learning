from django.urls import path

from . import views

app_name = 'sbxapp'  # application namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('example/', views.form_example, name='example'),
    path('upload/', views.upload_file, name='upload-file'),
    path('dt2/', views.dt_all2),
]
