from django.contrib import admin

from . import models

admin.register(models.Thread)
admin.register(models.Reply)
