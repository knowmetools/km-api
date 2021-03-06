# Generated by Django 2.0.6 on 2018-10-20 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import permission_utils.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("know_me", "0005_kmuser_is_legacy_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscription",
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
                    "is_active",
                    models.BooleanField(
                        help_text="A boolean indicating if the subscription is active.",
                        verbose_name="is active",
                    ),
                ),
                (
                    "time_created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The time that the subscription instance was created.",
                        verbose_name="creation time",
                    ),
                ),
                (
                    "time_updated",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The time of the subscription's last update.",
                        verbose_name="last update time",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        help_text="The user who has a Know Me subscription",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="know_me_subscription",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Know Me subscription",
                "verbose_name_plural": "Know Me subscriptions",
                "ordering": ("time_created",),
            },
            bases=(
                permission_utils.model_mixins.IsAuthenticatedMixin,
                models.Model,
            ),
        )
    ]
