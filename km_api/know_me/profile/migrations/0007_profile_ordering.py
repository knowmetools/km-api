# Generated by Django 2.0.3 on 2018-04-03 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_listentry'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='profile',
            order_with_respect_to='km_user',
        ),
    ]
