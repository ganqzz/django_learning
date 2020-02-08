from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import store.views
import store.api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/<int:id>/', store.views.show, name='show-product'),
    path('cart/', store.views.cart, name='shopping-cart'),
    path('', store.views.index, name='list-products'),
    path('api/v1/products/', include('store.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # only in debug mode
