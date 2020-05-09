import os.path

from rest_framework.test import APITestCase

from shopping_site import settings
from store.models import Product


class ProductCRUDTestCase(APITestCase):
    fixtures = ['store/data/fixtures.json']

    def test_create_product(self):
        initial_product_count = Product.objects.count()
        product_attrs = {
            'name': 'New Product',
            'description': 'Awesome product',
            'price': '123.45',
        }
        response = self.client.post('/api/v1/products/new', product_attrs)
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(
            Product.objects.count(),
            initial_product_count + 1,
        )
        for attr, expected_value in product_attrs.items():
            self.assertEqual(response.data[attr], expected_value)
        self.assertEqual(response.data['is_on_sale'], False)
        self.assertEqual(
            response.data['current_price'],
            float(product_attrs['price']),
        )

    def test_delete_product(self):
        initial_product_count = Product.objects.count()
        product_id = Product.objects.first().id
        self.client.delete('/api/v1/products/{}/'.format(product_id))
        self.assertEqual(
            Product.objects.count(),
            initial_product_count - 1,
        )
        self.assertRaises(
            Product.DoesNotExist,
            Product.objects.get, pk=product_id,
        )

    def test_list_products(self):
        products_count = Product.objects.count()
        response = self.client.get('/api/v1/products/')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], products_count)
        self.assertEqual(len(response.data['results']), products_count)

    def test_update_product(self):
        product = Product.objects.first()
        response = self.client.patch(
            '/api/v1/products/{}/'.format(product.id),
            {
                'name': 'New Product',
                'description': 'Awesome product',
                'price': 123.45,
            },
            format='json',
        )
        updated = Product.objects.get(pk=product.id)
        self.assertEqual(updated.name, 'New Product')

    def test_upload_product_photo(self):
        product = Product.objects.first()
        original_photo = product.photo
        photo_path = os.path.join(settings.BASE_DIR,
                                  'store/data/products/vitamin-multi.jpg')
        with open(photo_path, 'rb') as photo_data:
            response = self.client.patch('/api/v1/products/{}/'.format(product.id),
                                         {'photo': photo_data, },
                                         format='multipart')
        self.assertEqual(response.status_code, 200)

        # 既に同名のファイルがある場合、ランダムな文字列が付加された別ファイルとして保存される
        self.assertNotEqual(response.data['photo'], original_photo)

        try:
            updated = Product.objects.get(pk=product.id)
            expected_photo = os.path.join(settings.MEDIA_ROOT,
                                          'products', 'vitamin-multi')
            self.assertTrue(updated.photo.path.startswith(expected_photo))
        finally:
            os.remove(updated.photo.path)
