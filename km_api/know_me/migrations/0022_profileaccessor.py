# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 16:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import permission_utils.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0021_kmuseraccessormodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileAccessor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_write', models.BooleanField(default=False, help_text='Does the user have write access.', verbose_name='can write')),
                ('km_user_accessor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_accessors', related_query_name='profile_accessor', to='know_me.KMUserAccessor', verbose_name='know me user accessor')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_accessors', related_query_name='profile_accessor', to='know_me.Profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'profile accessor',
                'verbose_name_plural': 'profile accessors',
            },
            bases=(permission_utils.model_mixins.IsAuthenticatedMixin, models.Model),
        ),
    ]