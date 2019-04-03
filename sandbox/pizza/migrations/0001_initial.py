# Generated by Django 2.1.3 on 2019-03-27 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topping1', models.CharField(max_length=20)),
                ('topping2', models.CharField(max_length=20)),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='M', max_length=1)),
            ],
        ),
    ]
