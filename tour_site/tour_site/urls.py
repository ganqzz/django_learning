from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

import api.views
from . import views

router = DefaultRouter()
router.register(r'packages', api.views.PackageViewSet,
                basename='packages')  # basenameを明示して下のpublicと混同しないようにする
router.register(r'wishlist', api.views.WishlistItemViewSet)
router.register(r'public/packages', api.views.PublicPackageViewSet)  # これ
router.register(r'bookings', api.views.BookingViewSet)

urlpatterns = [
    path('', views.top, name='top'),

    path('api/v1/', include((router.urls, 'apiv1',))),
    path('admin/', admin.site.urls),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
