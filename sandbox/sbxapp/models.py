from django.db import models


class DtDemo(models.Model):
    dt = models.DateTimeField(auto_now_add=True)


class Simple(models.Model):
    text = models.CharField(max_length=10)
    number = models.IntegerField(null=True)
    url = models.URLField(default='www.example.com')

    def __str__(self):
        return self.url


class Hash(models.Model):
    text = models.TextField()
    hash = models.CharField(max_length=64)

    def __str__(self):
        return self.text


class Car(models.Model):
    name = models.CharField(max_length=20)
    make = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        return self.name
