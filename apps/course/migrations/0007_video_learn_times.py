# Generated by Django 2.0.1 on 2018-08-13 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20180813_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长'),
        ),
    ]
