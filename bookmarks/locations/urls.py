from django.urls import path, include, re_path
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
    re_path(r'', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')), ]

standardview_urlpatterns = [
    re_path(r'^bookmarks_trad_view/$', BookmarkListView.as_view()),
    re_path(r'^bookmarks_trad_view/(?P<pk>[0-9]+)/$', BookmarkDetailView.as_view()),
    re_path(r'^bookmarks_class_view/$', BookmarkList.as_view()),
    re_path(r'^bookmarks_class_view/(?P<pk>[0-9]+)/$', BookmarkDetail.as_view()),
    re_path(
        r'^bookmarks_viewset/$',
        BookmarkViewSet.as_view({'get': 'list', 'post': 'create'})
    ),
    re_path(
        r'^bookmarks_viewset/(?P<pk>[0-9]+)/$',
        BookmarkViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
            'delete': 'destroy'
        })
    ),
]

urlpatterns += format_suffix_patterns(standardview_urlpatterns)
