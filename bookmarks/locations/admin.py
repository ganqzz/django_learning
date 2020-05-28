from django.contrib import admin

from . import models

admin.register(models.Bookmark)
admin.register(models.Comment)
admin.register(models.Note)
admin.register(models.Like)
