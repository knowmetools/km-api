# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 19:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0002_profilegroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('row_type', models.PositiveSmallIntegerField(choices=[(1, 'grouped row'), (2, 'paged row'), (3, 'text row'), (4, 'visual row')], verbose_name='row type')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', related_query_name='row', to='know_me.ProfileGroup', verbose_name='profile group')),
            ],
            options={
                'verbose_name': 'profile row',
                'verbose_name_plural': 'profile rows',
            },
        ),
    ]
