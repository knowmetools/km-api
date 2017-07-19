# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_emailaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailaddress',
            name='primary',
            field=models.BooleanField(default=False, help_text='The primary address receives all account notifications.', verbose_name='is primary'),
        ),
    ]
