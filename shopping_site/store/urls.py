from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('products/<int:pk>/', views.show, name='show-product'),
    path('', views.index, name='list-products'),

    path('api/v1/products/', views.ProductList.as_view(), name='api-list-products'),
    path('api/v1/products/new', views.ProductCreate.as_view()),
    path('api/v1/products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view()),
    path('api/v1/products/<int:pk>/stats', views.ProductStats.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # only in debug mode
