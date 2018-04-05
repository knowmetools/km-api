# Generated by Django 2.0.3 on 2018-04-05 17:21

from django.db import migrations, models
import permission_utils.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        ('know_me', '0002_kmuseraccessor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_app_version_ios', models.CharField(blank=True, help_text='The minimum version of the iOS app that is usable without a required update.', max_length=31)),
            ],
            options={
                'verbose_name': 'config',
            },
            bases=(permission_utils.model_mixins.IsAuthenticatedMixin, models.Model),
        ),
    ]