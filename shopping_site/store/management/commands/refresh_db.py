import random

from django.core.management import BaseCommand
from datetime import timedelta
from django.utils import timezone

from store.models import Product, Order


class Command(BaseCommand):
    help = """**** Refresh DB ****"""

    def handle(self, *args, **options):
        Product.objects.all().delete()

        now = timezone.now()

        Product(
            pk=1, name='Mineral Water Strawberry',
            description='Natural-flavored strawberry with an anti-oxidant kick.', price=1.00,
            photo='products/mineralwater-strawberry.jpg',
        ).save()
        Product(
            pk=2, name='Mineral Water Raspberry',
            description='Flavoured with raspberry, loaded with anti-oxidants.', price=2.00,
            photo='products/mineralwater-raspberry.jpg',
            sale_start=now + timedelta(days=20),
            sale_end=None,
        ).save()
        Product(
            pk=3, name='Vitamin A 10,000 IU (125 caplets)', price=3.00,
            description='Vitamin A is essential for normal and night vision, and helps maintain healthy skin and mucous membranes.',
            sale_start=now - timedelta(days=10),
            sale_end=None,
            photo='products/vitamin-a.jpg',
        ).save()
        Product(
            pk=4, name='Vitamin B-Complex (100 caplets)', price=3.00,
            description='Contains a combination of essential B vitamins that help convert food to energy.',
            sale_start=now,
            sale_end=now + timedelta(days=10),
            photo='products/vitamin-bcomplex.jpg',
        ).save()

        Order.objects.all().delete()

        for i in range(1, 11):
            Order(pk=i,
                  product_id=i % 4 + 1,
                  quantity=random.randint(1, 20)).save()
