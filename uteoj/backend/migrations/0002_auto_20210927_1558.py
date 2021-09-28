# Generated by Django 3.2 on 2021-09-27 08:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemmodel',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 27, 8, 58, 33, 428736, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='ContestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2048)),
                ('description', models.TextField()),
                ('startTime', models.DateField()),
                ('endTime', models.DateField()),
                ('problems', models.ManyToManyField(to='backend.ProblemModel')),
            ],
        ),
    ]
