# Generated by Django 3.2 on 2021-06-29 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_alter_submissionmodel_submission_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionmodel',
            name='points',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
