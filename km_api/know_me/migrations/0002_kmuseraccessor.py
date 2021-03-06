# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-11 03:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import permission_utils.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("know_me", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="KMUserAccessor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The time that the accessor was created.",
                        verbose_name="created at",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="The email address used to invite the user.",
                        max_length=254,
                        verbose_name="email",
                    ),
                ),
                (
                    "is_accepted",
                    models.BooleanField(
                        default=False,
                        help_text="The KMUser has accepted the access.",
                        verbose_name="is accepted",
                    ),
                ),
                (
                    "is_admin",
                    models.BooleanField(
                        default=False,
                        help_text="A boolean indicating if the user has admin access.",
                        verbose_name="is admin",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The time that the accessor was last updated.",
                        verbose_name="updated at",
                    ),
                ),
                (
                    "km_user",
                    models.ForeignKey(
                        help_text="The Know Me user this accessor grants access to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="km_user_accessors",
                        related_query_name="km_user_accessor",
                        to="know_me.KMUser",
                        verbose_name="Know Me user",
                    ),
                ),
                (
                    "user_with_access",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="km_user_accessors",
                        related_query_name="km_user_accessor",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Know Me user accessor",
                "verbose_name_plural": "Know Me user accessors",
            },
            bases=(
                permission_utils.model_mixins.IsAuthenticatedMixin,
                models.Model,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="kmuseraccessor",
            unique_together=set([("km_user", "user_with_access")]),
        ),
    ]
