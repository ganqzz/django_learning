from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import SimpleHelloWorldAPI, BookmarkListView, BookmarkDetailView, \
    BookmarkList, BookmarkDetail, BookmarkViewSet, CommentViewSet, NoteViewSet

router = routers.DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('hello_api/<str:name>/', SimpleHelloWorldAPI.as_view(), name='hello-api'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

standardview_urlpatterns = [
    path('bookmarks_trad_view/', BookmarkListView.as_view()),
    path('bookmarks_trad_view/<int:pk>/', BookmarkDetailView.as_view()),
    path('bookmarks_class_view/', BookmarkList.as_view()),
    path('bookmarks_class_view/<int:pk>/', BookmarkDetail.as_view()),
    path('bookmarks_viewset/', BookmarkViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('bookmarks_viewset/<int:pk>/',
         BookmarkViewSet.as_view({
             'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
             'delete': 'destroy'
         })),
]

urlpatterns += format_suffix_patterns(standardview_urlpatterns)
