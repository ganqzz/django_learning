# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-22 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('F', 'First Player To Move'), ('S', 'Second Player To Move'), ('W', 'First Player Wins'), ('L', 'Second Player Wins'), ('D', 'Draw')], default='F', max_length=1),
        ),
    ]