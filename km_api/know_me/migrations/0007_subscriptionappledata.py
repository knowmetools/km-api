# Generated by Django 2.0.6 on 2018-10-20 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0006_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionAppleData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_data', models.TextField(help_text='The receipt data that is base 64 encoded.', verbose_name='receipt data')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time that the Apple subscription was initially recorded.', verbose_name='creation time')),
                ('time_updated', models.DateTimeField(auto_now=True, help_text="The time of the subscription's last update.", verbose_name='last update time')),
                ('subscription', models.OneToOneField(help_text='The Know Me subscription the data belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='apple_data', to='know_me.Subscription', verbose_name='subscription')),
            ],
            options={
                'verbose_name': 'Apple subscription',
                'verbose_name_plural': 'Apple subscriptions',
                'ordering': ('time_created',),
            },
        ),
    ]
