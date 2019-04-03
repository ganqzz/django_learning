from enum import Enum

from django.db import models


class Size(Enum):
    # name = value
    S = 'Small'
    M = 'Medium'
    L = 'Large'

    @classmethod
    def get_choices(cls):
        return tuple((e.name, e.value) for e in cls)


SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
)


class Pizza(models.Model):
    topping1 = models.CharField(max_length=20)
    topping2 = models.CharField(max_length=20)
    # size = models.CharField(choices=SIZE_CHOICES, max_length=1, default='M')
    size = models.CharField(choices=Size.get_choices(), max_length=1, default=Size.M.name)

    def __str__(self):
        return 'Pizza(size={}, topping1="{}", topping2="{}")'.format(
            self.get_size_display(), self.topping1, self.topping2)
