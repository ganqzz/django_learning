from django.urls import path

from . import views

app_name = 'hashing'  # application namespace

urlpatterns = [
    path('', views.home, name='home'),
    # no trailing slash
    path('hash/<str:hash>', views.hash, name='hash'),
    path('quickhash', views.quickhash, name='quickhash'),
]
