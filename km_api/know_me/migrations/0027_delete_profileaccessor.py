# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 21:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0026_update_kmuseraccessor_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileaccessor',
            name='km_user_accessor',
        ),
        migrations.RemoveField(
            model_name='profileaccessor',
            name='profile',
        ),
        migrations.DeleteModel(
            name='ProfileAccessor',
        ),
    ]
