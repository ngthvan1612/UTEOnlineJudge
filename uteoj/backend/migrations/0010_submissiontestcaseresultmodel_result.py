# Generated by Django 3.2 on 2021-09-07 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20210904_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissiontestcaseresultmodel',
            name='result',
            field=models.IntegerField(blank=True, choices=[(7, 'Dịch lỗi'), (0, 'Được chấp nhận'), (1, 'Kết quả sai'), (2, 'Chạy quá thời gian'), (3, 'Vượt quá bộ nhớ'), (4, 'Lỗi thực thi')], null=True),
        ),
    ]
