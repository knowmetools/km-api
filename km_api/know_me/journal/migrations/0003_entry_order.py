# Generated by Django 2.0.3 on 2018-04-23 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("journal", "0002_entrycomment")]

    operations = [
        migrations.AlterModelOptions(
            name="entry",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "journal entry",
                "verbose_name_plural": "journal entries",
            },
        )
    ]
