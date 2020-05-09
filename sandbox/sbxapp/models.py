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
        return '{}: {} ({})'.format(self.make, self.name, self.year)


# --- N+1 Demo

class Category(models.Model):
    """カテゴリー"""
    name = models.CharField('カテゴリ名', max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """タグ"""
    name = models.CharField('タグ名', max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    """記事"""
    title = models.CharField('タイトル', max_length=255)
    category = models.ForeignKey(Category, related_name='+',
                                 verbose_name='カテゴリ', on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name='+', verbose_name='タグ')

    def __str__(self):
        return self.title
