# Generated by Django 2.2b1 on 2019-02-28 00:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("know_me", "0007_subscriptionappledata")]

    operations = [
        migrations.AddField(
            model_name="subscriptionappledata",
            name="expiration_time",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text="The expiration time of the most recent transaction associated with the receipt.",
                verbose_name="expiration time",
            ),
        )
    ]
