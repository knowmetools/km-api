# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 04:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import know_me.models


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0003_profilerow'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('resource', models.FileField(max_length=255, upload_to=know_me.models.get_media_resource_upload_path, verbose_name='resource')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_items', related_query_name='gallery_item', to='know_me.Profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'gallery item',
                'verbose_name_plural': 'gallery items',
            },
        ),
    ]
