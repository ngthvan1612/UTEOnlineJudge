# Generated by Django 3.2 on 2021-07-17 05:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0030_alter_problemmodel_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemmodel',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 17, 5, 43, 42, 725362)),
        ),
    ]
