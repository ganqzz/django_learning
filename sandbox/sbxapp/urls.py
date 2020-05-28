from django.urls import path

from . import views

app_name = 'sbxapp'  # application namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('hello/<name>/', views.hello, name='hello'),
    path('dt/', views.dt_all),
    path('dt2/', views.dt_all2),
    path('tags_filters/', views.tags_filters, name='tags_filters'),
    path('form_example/', views.form_example, name='form-example'),
    path('upload/', views.upload_file, name='upload-file'),

    path('hashing/', views.hashing_list, name='hashing-home'),
    path('hashing/create', views.create_hash, name='hashing-create'),
    path('hashing/quickhash', views.get_hash_ajax, name='hashing-quickhash'),
    path('hashing/<str:hash>/', views.hash_detail, name='hashing-detail'),  # 位置注意

    path('car_app/', views.car_list, name='car-list'),
    path('car_app/create', views.CarEditView.as_view(), name='car-create'),
    path('car_app/<int:pk>/', views.car_detail, name='car-detail'),
    path('car_app/<int:pk>/update', views.CarEditView.as_view(), name='car-update'),
    path('car_app/<int:pk>/delete', views.car_delete, name='car-delete'),

    path('nplus1/demo1', views.PostIndex.as_view(), name='nplus1-demo1'),
    path('nplus1/demo2', views.PostIndex2.as_view(), name='nplus1-demo2'),
]
