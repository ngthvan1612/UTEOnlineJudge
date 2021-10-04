# Generated by Django 3.2 on 2021-10-02 14:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_merge_20210930_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='problemmodel',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 2, 14, 0, 2, 128243, tzinfo=utc)),
        ),
    ]