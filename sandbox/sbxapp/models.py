from django.db import models


class DtDemo(models.Model):
    dt = models.DateTimeField(auto_now_add=True)
