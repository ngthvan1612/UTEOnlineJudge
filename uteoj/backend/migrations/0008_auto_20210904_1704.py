# Generated by Django 3.2 on 2021-09-04 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20210904_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problemstatisticsmodel',
            name='submitCount',
        ),
        migrations.AddField(
            model_name='problemstatisticsmodel',
            name='mleCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problemstatisticsmodel',
            name='rteCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problemstatisticsmodel',
            name='tleCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problemstatisticsmodel',
            name='totalSubmission',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problemstatisticsmodel',
            name='waCount',
            field=models.IntegerField(default=0),
        ),
    ]