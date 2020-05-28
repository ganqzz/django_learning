from django.contrib import admin

from . import models

admin.register(models.Product)
admin.register(models.Order)
