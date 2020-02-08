from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Profile(models.Model):
    """ User追加情報 """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], blank=True)

    def __str__(self):
        return self.user.username
