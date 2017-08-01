# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 16:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0014_listcontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='text')),
                ('list_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', related_query_name='entry', to='know_me.ListContent', verbose_name='list content')),
            ],
            options={
                'verbose_name': 'list entry',
                'verbose_name_plural': 'list entries',
            },
        ),
    ]
