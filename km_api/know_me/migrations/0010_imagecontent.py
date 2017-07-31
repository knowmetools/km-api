# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 19:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0009_auto_20170731_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('image_resource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='know_me.MediaResource', verbose_name='image resource')),
                ('media_resource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='know_me.MediaResource', verbose_name='media resource')),
                ('profile_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image_content', to='know_me.ProfileItem', verbose_name='profile item')),
            ],
            options={
                'verbose_name_plural': 'profile item image content',
                'verbose_name': 'profile item image content',
            },
        ),
    ]
