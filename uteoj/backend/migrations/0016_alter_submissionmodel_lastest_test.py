# Generated by Django 3.2 on 2021-09-12 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_alter_submissionmodel_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionmodel',
            name='lastest_test',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]