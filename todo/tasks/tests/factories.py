import factory.fuzzy
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import Task


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)  # unique fields

    username = factory.Faker('name')
    email = factory.Sequence(lambda n: f'person{n}@example.com')


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    owner = factory.SubFactory(UserFactory)
    title = factory.Faker('word')
    description = factory.Faker('text')
    due_date = factory.fuzzy.FuzzyDate(timezone.now(),
                                       timezone.now() + timezone.timedelta(days=10))
    # complete_time = factory.Faker('past_datetime')
