# Generated by Django 3.0.8 on 2020-08-21 22:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [("know_me", "0017_reminderemaillog")]

    operations = [
        migrations.AddField(
            model_name="reminderemailsubscriber",
            name="schedule_frequency",
            field=models.CharField(
                default="Weekly",
                help_text="The frequency in which the reminder emails are scheduled to send.",
                max_length=10,
                verbose_name="schedule frequency",
            ),
        ),
        migrations.AlterField(
            model_name="reminderemaillog",
            name="schedule_frequency",
            field=models.CharField(
                default="Weekly",
                help_text="The frequency in which the reminder emails are sheduled to send.",
                max_length=10,
                verbose_name="schedule frequency",
            ),
        ),
        migrations.AlterField(
            model_name="reminderemailsubscriber",
            name="subscription_uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                verbose_name="subscription uuid",
            ),
        ),
    ]
