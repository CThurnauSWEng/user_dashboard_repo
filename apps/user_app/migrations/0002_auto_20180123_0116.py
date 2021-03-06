# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-23 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='desc',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_level',
            field=models.IntegerField(default=1),
        ),
    ]
