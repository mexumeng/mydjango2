# Generated by Django 2.0.1 on 2018-08-14 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_course_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=500, verbose_name='视频地址'),
        ),
    ]
