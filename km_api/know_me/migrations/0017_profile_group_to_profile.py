# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 21:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import permission_utils.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0016_rename_profile_to_kmuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_default', models.BooleanField(default=False, help_text='The default profile is displayed initially.', verbose_name='is default')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('km_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profiles', related_query_name='profile', to='know_me.KMUser', verbose_name='know me user')),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
            bases=(permission_utils.model_mixins.IsAuthenticatedMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='profilegroup',
            name='km_user',
        ),
        migrations.RemoveField(
            model_name='profiletopic',
            name='group',
        ),
        migrations.AlterField(
            model_name='profiletopic',
            name='topic_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'profileed topic'), (2, 'paged topic'), (3, 'text topic'), (4, 'visual topic')], verbose_name='topic type'),
        ),
        migrations.DeleteModel(
            name='ProfileGroup',
        ),
        migrations.AddField(
            model_name='profiletopic',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', related_query_name='topic', to='know_me.Profile', verbose_name='profile'),
        ),
    ]