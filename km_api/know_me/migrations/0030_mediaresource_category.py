# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0029_mediaresourcecategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaresource',
            name='category',
            field=models.ForeignKey(blank=True, help_text='The category that the resource is a part of.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media_resources', related_query_name='media_resource', to='know_me.MediaResourceCategory', verbose_name='category'),
        ),
    ]
