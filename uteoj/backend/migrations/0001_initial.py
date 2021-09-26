# Generated by Django 3.2 on 2021-09-26 15:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportUserFileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, unique=True)),
                ('token', models.CharField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='LanguageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=128, null=True, unique=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('ext', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('compile_command', models.CharField(blank=True, max_length=255)),
                ('run_command', models.CharField(max_length=255, null=True)),
                ('execute_name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OJSettingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProblemCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProblemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_date', models.DateTimeField(default=datetime.datetime(2021, 9, 26, 15, 51, 57, 659947, tzinfo=utc))),
                ('shortname', models.CharField(max_length=32, unique=True)),
                ('fullname', models.CharField(max_length=255)),
                ('problem_type', models.IntegerField(choices=[(0, 'ACM'), (1, 'OI')], default=0)),
                ('difficult', models.IntegerField(choices=[(-10, 'Dễ'), (0, 'Trung bình'), (10, 'Khó')], default=-10)),
                ('hash_problem', models.CharField(blank=True, max_length=255)),
                ('points_per_test', models.FloatField(default=1.0)),
                ('total_points', models.FloatField(default=0.0)),
                ('statement', models.CharField(max_length=2048)),
                ('submission_visible_mode', models.IntegerField(choices=[(0, 'Ai cũng có thể xem được'), (1, 'Chỉ những người giải được'), (2, 'Chỉ mình tôi')], default=0)),
                ('input_filename', models.CharField(max_length=32)),
                ('output_filename', models.CharField(max_length=32)),
                ('use_stdin', models.BooleanField(default=True)),
                ('use_stdout', models.BooleanField(default=True)),
                ('time_limit', models.IntegerField(default=1000)),
                ('memory_limit', models.IntegerField(default=65536)),
                ('use_checker', models.BooleanField(default=False)),
                ('checker', models.TextField(blank=True, default='')),
                ('solvedCount', models.IntegerField(default=0)),
                ('totalSubmission', models.IntegerField(default=0)),
                ('waCount', models.IntegerField(default=0)),
                ('tleCount', models.IntegerField(default=0)),
                ('rteCount', models.IntegerField(default=0)),
                ('mleCount', models.IntegerField(default=0)),
                ('ceCount', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(blank=True, to='backend.ProblemCategoryModel')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemTestCaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(blank=True, max_length=255, null=True)),
                ('time_limit', models.IntegerField(default=1000)),
                ('memory_limit', models.IntegerField(default=65536)),
                ('points', models.FloatField(default=1.0)),
                ('name', models.CharField(max_length=255, null=True)),
                ('is_sample', models.BooleanField(default=False)),
                ('input_file', models.CharField(max_length=255, null=True)),
                ('output_file', models.CharField(max_length=255, null=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.problemmodel')),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_code', models.TextField()),
                ('submission_date', models.DateTimeField()),
                ('submission_judge_date', models.DateTimeField(blank=True, null=True)),
                ('compile_message', models.TextField(blank=True, null=True)),
                ('executed_time', models.IntegerField(blank=True, null=True)),
                ('memory_usage', models.IntegerField(blank=True, null=True)),
                ('points', models.FloatField(blank=True, default=0.0, null=True)),
                ('result', models.IntegerField(blank=True, choices=[(7, 'Dịch lỗi'), (0, 'Được chấp nhận'), (1, 'Kết quả sai'), (2, 'Chạy quá thời gian'), (3, 'Vượt quá bộ nhớ'), (4, 'Lỗi thực thi')], null=True)),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Đang đợi'), (1, 'Đang biên dịch'), (2, 'Đang chấm'), (3, 'Chấm xong')], null=True)),
                ('lastest_test', models.IntegerField(blank=True, default=1, null=True)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.languagemodel')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.problemmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_user_profile', models.CharField(blank=True, max_length=255, null=True)),
                ('public_key', models.CharField(blank=True, max_length=255, null=True)),
                ('avatar', models.CharField(blank=True, max_length=255)),
                ('job', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProblemStatisticsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalSubmission', models.IntegerField(default=0)),
                ('solvedCount', models.IntegerField(default=0)),
                ('waCount', models.IntegerField(default=0)),
                ('tleCount', models.IntegerField(default=0)),
                ('rteCount', models.IntegerField(default=0)),
                ('mleCount', models.IntegerField(default=0)),
                ('ceCount', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionTestcaseResultModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('executed_time', models.IntegerField()),
                ('memory_usage', models.IntegerField()),
                ('points', models.FloatField()),
                ('checker_message', models.TextField(blank=True)),
                ('result', models.IntegerField(blank=True, choices=[(7, 'Dịch lỗi'), (0, 'Được chấp nhận'), (1, 'Kết quả sai'), (2, 'Chạy quá thời gian'), (3, 'Vượt quá bộ nhớ'), (4, 'Lỗi thực thi')], null=True)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.submissionmodel')),
                ('testcase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.problemtestcasemodel')),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=4096)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
