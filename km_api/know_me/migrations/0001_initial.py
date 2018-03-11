# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-11 03:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import know_me.models
import permission_utils.model_mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KMUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The time that the Know Me user was created.', verbose_name='created at')),
                ('image', models.ImageField(blank=True, help_text="The image to use as the user's hero image.", max_length=255, null=True, upload_to=know_me.models.get_km_user_image_upload_path, verbose_name='image')),
                ('quote', models.TextField(blank=True, help_text='A quote to introduce the user.', null=True, verbose_name='quote')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='The time that the Know Me user was last updated.', verbose_name='updated at')),
                ('user', models.OneToOneField(help_text='The user who owns the Know Me app account.', on_delete=django.db.models.deletion.CASCADE, related_name='km_user', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Know Me user',
                'verbose_name_plural': 'Know Me users',
            },
            bases=(permission_utils.model_mixins.IsAuthenticatedMixin, models.Model),
        ),
    ]
