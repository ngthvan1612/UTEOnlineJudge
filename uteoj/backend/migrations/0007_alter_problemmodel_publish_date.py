# Generated by Django 3.2 on 2021-09-28 04:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_problemmodel_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemmodel',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 4, 49, 26, 821158, tzinfo=utc)),
        ),
    ]
