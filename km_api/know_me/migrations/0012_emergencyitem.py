# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 21:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import permission_utils.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0011_remove_profileitem_imagecontent_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmergencyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('km_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_items', related_query_name='emergency_item', to='know_me.KMUser', verbose_name='know me user')),
                ('media_resource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emergency_items', related_query_name='emergency_item', to='know_me.MediaResource', verbose_name='media resource')),
            ],
            options={
                'verbose_name_plural': 'emergency items',
                'verbose_name': 'emergency item',
            },
            bases=(permission_utils.model_mixins.IsAuthenticatedMixin, models.Model),
        ),
    ]
