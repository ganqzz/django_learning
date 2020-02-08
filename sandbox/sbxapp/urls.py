from django.urls import path

from . import views

app_name = 'sbxapp'  # application namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('hello/<name>/', views.hello, name='hello'),
    path('dt2/', views.dt_all2),
    path('form_example/', views.form_example, name='form-example'),
    path('upload/', views.upload_file, name='upload-file'),

    path('hashing/', views.hashing_list, name='hashing-home'),
    path('hashing/create', views.create_hash, name='hashing-create'),
    path('hashing/quickhash', views.get_hash_ajax, name='hashing-quickhash'),
    path('hashing/<str:hash>/', views.hash_detail, name='hashing-detail'),  # 位置注意

    path('car_app/', views.car_list, name='car-list'),
    path('car_app/create', views.CarView.as_view(), name='car-create'),
    path('car_app/<int:pk>/', views.CarView.as_view(), name='car-detail'),
    path('car_app/<int:pk>/delete', views.car_delete, name='car-delete'),
]
