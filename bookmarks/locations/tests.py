from datetime import timedelta
from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count
from django.test import TestCase
from django.test import tag
from django.utils import timezone
from oauth2_provider.models import get_application_model, get_access_token_model
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .models import Bookmark, Note, Comment, Like
from .views import BookmarkViewSet


def set_up_bookmarks():
    bookmark1 = Bookmark(link="https://www.yahoo.co.jp/")
    bookmark1.save()
    bookmark2 = Bookmark(link="https://www.msn.com/")
    bookmark2.save()
    bookmark3 = Bookmark(link="https://www.bbc.com/")
    bookmark3.save()
    note = Note(text="This is a note", bookmark=bookmark2)
    note.save()
    comment = Comment(bookmark=bookmark3, text="This is a comment")
    comment.save()
    like1 = Like(bookmark=bookmark1)
    like1.save()
    like2 = Like(comment=comment)
    like2.save()


def create_user_access_token():
    user = get_user_model().objects.create(username='user')
    token_expiration_time = timezone.now() + timedelta(minutes=60)
    token = get_access_token_model().objects.create(
        user=user,
        scope='read write packages',
        token='test{}{}'.format(
            user.id,
            int(token_expiration_time.timestamp())
        ),
        application=get_application_model().objects.first(),
        expires=token_expiration_time
    )
    return token


def auth_header(token):
    return {
        'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)
    }


class BookmarkViewSetIntegrationTest(APITestCase):
    def setUp(self):
        super().setUp()
        set_up_bookmarks()
        self.auth_header = auth_header(create_user_access_token())

    @tag('integration_test')
    def test_get(self):
        result = self.client.get('/locations/bookmarks/', **self.auth_header)
        stream = BytesIO(result.content)
        data = JSONParser().parse(stream)  # paginationが有効な時は、dictになることに注意
        self.assertEqual(len(data), 6)  # migration:3 + setUp:3

    @tag('integration_test')
    def test_add_like_it(self):
        bookmark = Bookmark.objects.annotate(num_likes=Count('likes')).get(id=6)
        self.assertEqual(bookmark.num_likes, 0)

        result = self.client.post('/locations/bookmarks/6/add_like/', **self.auth_header)
        bookmark = Bookmark.objects.annotate(num_likes=Count('likes')).get(id=6)
        self.assertEqual(bookmark.num_likes, 1)

        result = self.client.post('/locations/bookmarks/6/add_like/', **self.auth_header)
        bookmark = Bookmark.objects.annotate(num_likes=Count('likes')).get(id=6)
        self.assertEqual(bookmark.num_likes, 2)


class BookmarkViewSetUnitTest(TestCase):
    def setUp(self):
        super().setUp()
        set_up_bookmarks()

    @tag('unit_test')
    @patch('locations.views.Response')
    @patch('locations.views.BookmarkViewSet.get_object')
    @patch('locations.views.Like')
    def test_add_like_ut(self, l_patch, go_patch, r_patch):
        factory = APIRequestFactory()
        request = factory.post(
            '/locations/bookmarks/6/add_like/', {}
        )
        view = BookmarkViewSet()
        result = view.add_like(request)
        self.assertEqual(go_patch.call_count, 1)
        self.assertEqual(l_patch.call_count, 1)
        self.assertEqual(l_patch.return_value.bookmark, go_patch.return_value)
        self.assertEqual(l_patch.return_value.save.call_count, 1)
        self.assertEqual(r_patch.call_count, 1)
        self.assertEqual(r_patch.call_args[0], ({'status': 'bookmark like set'},))
        self.assertEqual(r_patch.call_args[1], {'status': status.HTTP_201_CREATED})
        self.assertEqual(result, r_patch.return_value)
