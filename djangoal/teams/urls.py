from django.urls import path

from . import views

app_name = 'teams'  # application namespace

urlpatterns = [
    path('', views.TeamListViewMixed.as_view(), name='list'),
    path('<int:pk>/', views.TeamDetailViewMixed.as_view(), name='detail'),
    path('create/', views.TeamCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', views.TeamUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.TeamDeleteView.as_view(), name='delete'),
]
