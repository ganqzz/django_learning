from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.top, name='top'),

    path('sandbox/', include('sbxapp.urls')),
    path('pizza/', include('pizza.urls')),

    path('no_slash', views.trailing_slash),
    path('slash/', views.trailing_slash),
    path('params/', views.params),
]

# Debug Toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),
                   ] + urlpatterns
