# Generated by Django 2.0.3 on 2018-05-04 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0004_legacyuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='kmuser',
            name='is_legacy_user',
            field=models.BooleanField(default=False, help_text='A boolean indicating if the user used a prior version of Know Me.', verbose_name='is legacy user'),
        ),
    ]