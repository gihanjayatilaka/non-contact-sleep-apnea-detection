# Generated by Django 2.0 on 2018-05-21 04:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_auto_20180521_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='client_buffer_recv',
            name='device_id',
            field=models.CharField(default=datetime.datetime(2018, 5, 21, 4, 20, 46, 178094, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
    ]
