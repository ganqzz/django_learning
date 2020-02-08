from datetime import timedelta
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from oauth2_provider.models import get_application_model, get_access_token_model
from api.models import Package, PackagePermission
from api.serializers import BookingSerializer


def create_access_token(user):
    token_expiration_time = timezone.now() + timedelta(minutes=60)
    token = get_access_token_model().objects.create(
        user=user,
        scope='read write packages',
        token='test{}{}'.format(
            user.id,
            int(token_expiration_time.timestamp()),
        ),
        application=get_application_model().objects.first(),
        expires=token_expiration_time,
    )
    return token


def auth_header(token):
    return {'HTTP_AUTHORIZATION': 'Bearer {}'.format(token)}


class PackageViewSetTestCase(APITestCase):
    def test_only_logged_in_users_can_view_packages(self):
        response = self.client.get('/api/v1/packages/')
        self.assertEqual(response.status_code, 401)

        user = User.objects.create(username='user')
        token = create_access_token(user)
        response = self.client.get('/api/v1/packages/', **auth_header(token))
        self.assertEqual(response.status_code, 200)

        token.scope = 'packages'
        token.save()
        response = self.client.get('/api/v1/packages/', **auth_header(token))
        self.assertEqual(response.status_code, 403)


class PackagePermissionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.auth_user = auth_header(create_access_token(self.user))
        self.package = Package.objects.create(
            category='a', name='package', price=0.0, rating='medium', tour_length=1
        )
        self.other_user = User.objects.create(username='other_user')
        self.auth_other_user = auth_header(create_access_token(self.other_user))
        self.other_package = Package.objects.create(
            category='a', name='other_package', price=1.0, rating='medium', tour_length=1
        )

        PackagePermission.set_can_write(self.user, self.package)
        PackagePermission.set_can_write(self.other_user, self.other_package)

    def test_user_cannot_write_other_users_packages(self):
        self.assertTrue(PackagePermission.can_write(self.user, self.package))
        self.assertFalse(PackagePermission.can_write(self.user, self.other_package))

    def test_user_cannot_access_other_users_packages(self):
        response = self.client.get(
            '/api/v1/packages/{}/'.format(self.package.id),
            **self.auth_user
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/api/v1/packages/{}/'.format(self.other_package.id),
            **self.auth_user
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(
            '/api/v1/packages/{}/'.format(self.other_package.id),
            **self.auth_other_user
        )
        self.assertEqual(response.status_code, 200)


class CachingTestCase(APITestCase):
    def test_wishlist_cache(self):
        package = Package.objects.create(category='a', name='package', price=0.0, rating='medium',
                                         tour_length=1)
        self.assertIsNone(cache.get('wishlist:wishlist-items'))
        response = self.client.get('/api/v1/wishlist/')
        self.assertListEqual(response.data, [])
        self.assertListEqual(cache.get('wishlist:wishlist-items'), [])

        response = self.client.post('/api/v1/wishlist/', {'id': package.id})
        self.assertIsNone(cache.get('wishlist:wishlist-items'))

        response = self.client.get('/api/v1/wishlist/')
        self.assertListEqual(response.data, [package.id])
        self.assertListEqual(cache.get('wishlist:wishlist-items'), [package.id])


class SortingFilteringTestCase(APITestCase):
    def setUp(self):
        Package.objects.all().delete()

    def test_sorting_and_filtering(self):
        discount_package = Package.objects.create(category='a', name='a', price=1.0, rating='easy',
                                                  tour_length=1)
        expensive_package = Package.objects.create(category='b', name='b', price=99.0,
                                                   rating='medium', tour_length=2)
        user = User.objects.create(username='user')
        token = create_access_token(user)

        response = self.client.get('/api/v1/public/packages/', **auth_header(token))
        ids = list(map(lambda result: result['id'], response.data['results']))
        self.assertListEqual(ids, [expensive_package.id, discount_package.id])

        response = self.client.get('/api/v1/public/packages/?search=a', **auth_header(token))
        ids = list(map(lambda result: result['id'], response.data['results']))
        self.assertListEqual(ids, [discount_package.id])

        response = self.client.get('/api/v1/public/packages/?price_min=50.00', **auth_header(token))
        ids = list(map(lambda result: result['id'], response.data['results']))
        self.assertListEqual(ids, [expensive_package.id])


class ValidationTestCase(APITestCase):
    def test_invalid_start_date_returns_error(self):
        user = User.objects.create(username='user')
        auth = auth_header(create_access_token(user))

        data = {
            'category': 'tour',
            'name': 'Example',
            'promo': 'promo',
            'price': 12.34,
            'tour_length': 1,
            'rating': 'easy',
            'start': '01/01/2019',
            'thumbnail_url': '/images/hogehoge.gif',
        }

        response = self.client.post('/api/v1/packages/', data, **auth)
        self.assertEqual(response.status_code, 400)
        self.assertRegex(response.data['start'][0], 'wrong format')

        data['start'] = '2019-01-01'
        response = self.client.post('/api/v1/packages/', data, **auth)
        self.assertEqual(response.status_code, 201)

    def test_invalid_street_address_returns_error(self):
        data = {
            'name': 'Example',
            'email_address': 'example@localhost',
            'street_address': 'Invalid St.',
            'city': 'City',
            'package': 1,
        }
        response = self.client.post('/api/v1/bookings/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['street_address'][0],
            BookingSerializer.STREET_ADDRESS_ERROR
        )
        data['street_address'] = '11 Abc St.'
        response = self.client.post('/api/v1/bookings/', data)
        self.assertEqual(response.status_code, 201)
