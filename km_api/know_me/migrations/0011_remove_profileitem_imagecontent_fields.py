# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 20:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0010_imagecontent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileitem',
            name='text',
        ),
    ]