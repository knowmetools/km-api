# Generated by Django 2.2 on 2019-05-01 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("know_me", "0011_applereceipt")]

    operations = [
        migrations.AlterField(
            model_name="applereceipt",
            name="transaction_id",
            field=models.CharField(
                help_text="The ID of the original transaction from the receipt.",
                max_length=64,
                unique=True,
                verbose_name="original transaction ID",
            ),
        )
    ]
