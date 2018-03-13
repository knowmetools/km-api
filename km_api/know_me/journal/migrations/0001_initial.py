# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-12 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import know_me.journal.models
import permission_utils.model_mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('know_me', '0002_kmuseraccessor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, help_text='The file attached to the journal entry.', upload_to=know_me.journal.models.get_entry_attachment_upload_path, verbose_name='attachment')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The time that the entry was created.', verbose_name='created at')),
                ('text', models.TextField(help_text='The text that the entry contains.', verbose_name='text')),
                ('updated_at', models.DateTimeField(auto_now_add=True, help_text='The time that the entry was last updated.', verbose_name='updated at')),
                ('km_user', models.ForeignKey(help_text='The Know Me user who owns the entry.', on_delete=django.db.models.deletion.CASCADE, related_name='journal_entries', related_query_name='journal_entry', to='know_me.KMUser', verbose_name='Know Me user')),
            ],
            options={
                'verbose_name': 'journal entry',
                'verbose_name_plural': 'journal entries',
            },
            bases=(permission_utils.model_mixins.IsAuthenticatedMixin, models.Model),
        ),
    ]
