# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 19:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0022_profileaccessor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaresource',
            name='km_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_resources', related_query_name='media_resource', to='know_me.KMUser', verbose_name='km_user'),
        ),
        migrations.AlterField(
            model_name='profileitem',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', related_query_name='item', to='know_me.ProfileTopic', verbose_name='profile topic'),
        ),
        migrations.AlterField(
            model_name='profiletopic',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', related_query_name='topic', to='know_me.Profile', verbose_name='profile'),
        ),
    ]
