# Generated by Django 3.2 on 2021-07-22 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0039_problemmodel_categories_str'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemmodel',
            name='use_checker',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='problemmodel',
            name='checker',
            field=models.TextField(blank=True, null=True),
        ),
    ]
