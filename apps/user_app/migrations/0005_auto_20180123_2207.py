# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-23 22:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_auto_20180123_2203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='msg',
            old_name='user',
            new_name='user_id',
        ),
    ]