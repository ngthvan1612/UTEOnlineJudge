# Generated by Django 3.2 on 2021-07-12 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_userfilemanager_usersetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='job',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='usersetting',
            name='avatar',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]