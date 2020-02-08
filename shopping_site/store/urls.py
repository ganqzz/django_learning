from django.urls import path

from . import api_views

urlpatterns = [
    path('', api_views.ProductList.as_view(), name='api-list-products'),
    path('new', api_views.ProductCreate.as_view()),
    path('<int:id>/', api_views.ProductRetrieveUpdateDestroy.as_view()),
    path('<int:id>/stats', api_views.ProductStats.as_view()),
]
