# Generated by Django 2.2 on 2019-04-17 19:07

from django.db import migrations, models


def populate_latest_receipt_data(apps, _):
    """
    Populate the latest receipt data with the original receipt data.
    """
    SubscriptionAppleData = apps.get_model("know_me", "SubscriptionAppleData")

    for receipt in SubscriptionAppleData.objects.all():
        receipt.latest_receipt_data = receipt.receipt_data
        receipt.latest_receipt_data_hash = receipt.receipt_data_hash
        receipt.save()


class Migration(migrations.Migration):

    dependencies = [
        ("know_me", "0009_subscriptionappledata_receipt_data_hash")
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptionappledata",
            name="latest_receipt_data",
            field=models.TextField(
                help_text="The latest base64 encoded data for the receipt.",
                null=True,
                verbose_name="latest receipt data",
            ),
        ),
        migrations.AddField(
            model_name="subscriptionappledata",
            name="latest_receipt_data_hash",
            field=models.CharField(
                help_text="The SHA256 hash of the latest receipt data.",
                max_length=64,
                null=True,
                verbose_name="latest receipt data hash",
            ),
        ),
        migrations.AlterField(
            model_name="subscriptionappledata",
            name="receipt_data",
            field=models.TextField(
                help_text="The base64 encoded receipt data that was originally uploaded.",
                verbose_name="receipt data",
            ),
        ),
        migrations.AlterField(
            model_name="subscriptionappledata",
            name="receipt_data_hash",
            field=models.CharField(
                help_text="The SHA256 hash of the original receipt data.",
                max_length=64,
                unique=True,
                verbose_name="receipt data hash",
            ),
        ),
        # Populate initial values for latest data
        migrations.RunPython(
            populate_latest_receipt_data,
            reverse_code=migrations.RunPython.noop,
        ),
        # Now we can make the fields non-nullable since they have been
        # populated.
        migrations.AlterField(
            model_name="subscriptionappledata",
            name="latest_receipt_data",
            field=models.TextField(
                help_text="The latest base64 encoded data for the receipt.",
                verbose_name="latest receipt data",
            ),
        ),
        migrations.AlterField(
            model_name="subscriptionappledata",
            name="latest_receipt_data_hash",
            field=models.CharField(
                help_text="The SHA256 hash of the latest receipt data.",
                max_length=64,
                unique=True,
                verbose_name="latest receipt data hash",
            ),
        ),
    ]