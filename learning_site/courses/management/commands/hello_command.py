from django.core.management import BaseCommand


class Command(BaseCommand):
    # Show this when the user types help
    help = "Help for hello_command"

    def handle(self, *args, **options):
        print("Hello from Command!")
