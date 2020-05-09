from django.core.management import BaseCommand

from shopping_site import settings


class Command(BaseCommand):
    help = """**** Copy initial images to uploads folder ****"""

    def handle(self, *args, **options):
        print(settings.BASE_DIR)
