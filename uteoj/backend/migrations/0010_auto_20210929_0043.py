# Generated by Django 3.2 on 2021-09-28 17:43

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20210928_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='importuserfilemodel',
            name='contest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.contestmodel'),
        ),
        migrations.AlterField(
            model_name='problemmodel',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 17, 43, 20, 501637, tzinfo=utc)),
        ),
    ]
